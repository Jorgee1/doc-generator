import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

import csv
import pandas as pd
import json
import time
import os
from docxtpl import DocxTemplate
from threading import Thread
import time

#pyuic5 mainWindow.ui -o mainUI.py

class Task:

    def __init__(self):
        self.status = False
        self.task = False
        self.paths = []

    def start_thread(self):
        self.thread = Thread(target=self.cycle, daemon=True)
        self.status = True
        self.thread.start()

    def stop_thread(self):
        self.status = False
        self.task = False
        #self.t1.join()


    def start_task(self, paths):
        self.paths = paths
        self.task = True

    def stop_task(self):
        self.task = False


    def cycle(self):
        while self.status:
            if self.task:
                print("Generating....")

                try:
                    self.generate_formats()
                except Exception as e:
                    print(e)

                print("Done")
                self.stop_task()
            else:
                time.sleep(1)

    def generate_formats(self):

        PTH = "Out"
        temp_PTH = PTH
        if os.path.exists(PTH):
            index = 0
            while True:
                if os.path.exists(temp_PTH + '_' + str(index)):
                    index = index + 1
                else:
                    temp_PTH = temp_PTH + '_' + str(index)
                    break;
                print(temp_PTH + '_' + str(index))

        PTH = temp_PTH + "/"

        COL = ["ID","ENLACE","INICIO","FIN","T interr","DIRECCIÓN","BW","PROT"]
        jData = {
            "fecha_notificacion": time.strftime("%d/%m/%Y"),
            "ciudad": "Ciudad",
            "nodo": "Nodo",
            "fecha_hora": "dd/m/aaaa HH:mm",
            "duracion": "HH:mm",
            "col_labels": COL,
            "tbl_content": []
        }

        def guardar(data, name):
            file = open(name, "w+")
            json.dump(data, file, indent=4)
            file.close()

        if len(self.paths):
            for path_file in self.paths:
                file = pd.ExcelFile(path_file,encoding='latin-1')

                program = file.parse("Actividades")
                data = file.parse("Servicios") # This is RAWWWWWWW!
                company = data["OPERADOR"].unique().tolist()

                print("Inicio\n")

                for op in company:
                    # Ciclo de operadores

                    values = data.loc[ data["OPERADOR"] == op]
                    activity = values["ACTIVIDAD"].unique().tolist()

                    #Ciclo de mantenimientos
                    for act in activity:

                        info = program.loc[program["ACTIVIDAD"]==act]

                        jData["ciudad"] = info["Ciudad"].tolist()[0]
                        jData["nodo"] = info["Lugar"].tolist()[0]
                        jData["fecha_hora"] = str(info["Fecha Inicio"].tolist()[0].strftime("%d/%m/%Y")) + " " + str(info["Hora de Inicio"].tolist()[0])
                        jData["duracion"] = str(info["Duración"].tolist()[0])

                        jData["tbl_content"] = []


                        tempData = values.loc[values["ACTIVIDAD"]==act]
                        tempData = tempData[COL]

                        for i in tempData.index.tolist():
                            jData["tbl_content"].append({"cols" : [str(elm).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") for elm in tempData.loc[i].tolist()]})


                        if not os.path.exists(PTH+op):
                            os.makedirs(PTH+op)
                        # guardar(jData,PTH + op + "/" + op + "_" + act + ".json")
                        doc = DocxTemplate("Template/Template_Preventivo.docx")
                        doc.render(jData)
                        doc.save(PTH + op + "/" + op + "_" + act + "_" + jData["fecha_hora"].split(" ")[0].replace("/","-") + ".docx")
                        print(op)
        else:
            print("No file selected")



if __name__ == "__main__":
    SRC = "DataSet/"
    taskytask = Task()
    taskytask.generate_formats(SRC+"Enlaces.xlsx")
