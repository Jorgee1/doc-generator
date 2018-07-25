print("Cargando....")
import csv
import pandas as pd
import json
import time
import os
from docxtpl import DocxTemplate

#pyuic5 mainWindow.ui -o mainUI.py

SRC = "DataSet/"
PTH = SRC + "Out/"
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

file = pd.ExcelFile(SRC+"Enlaces.xlsx",encoding='latin-1')

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

print("\nFIN")