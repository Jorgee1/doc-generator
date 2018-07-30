import threading
import time
import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLineEdit, QFileDialog, QListWidgetItem
from PyQt5.QtCore import (QCoreApplication, Qt, QEvent)
from mainUI import Ui_MainWindow
from format_generator import Task



class Qfile(QListWidgetItem):
    def __init__(self, path, parent=None):
        self.path = path
        self.filename = os.path.basename(self.path)
        super().__init__(self.filename)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.generate)
        self.ui.actionOpenFIle.triggered.connect(self.openFileNameDialog)

        self.task = Task()
        self.task.start_thread()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            QCoreApplication.quit()
        elif key == Qt.Key_Delete:
            self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Abrir Excel", "","Excel (*.xlsx)", options=options)
        if fileNames:
            #self.ui.listWidget.addItems([ntpath.basename(i) for i in fileNames])
            for i in fileNames:
                self.ui.listWidget.addItem(Qfile(i))


    def generate(self):

        if self.task.status and not self.task.task:
            file_paths = []
            for i in range(self.ui.listWidget.count()):
                file_paths.append(self.ui.listWidget.item(i).path)

            self.task.start_task(file_paths)

        if not self.task.status:
            self.task = Task()
            self.task.start_thread()



app = QApplication(sys.argv)
w = AppWindow()
w.show()

sys.exit(app.exec_())
w.end()
w.task.stop_thread()
