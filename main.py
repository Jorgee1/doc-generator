import sys
import threading
import time

from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import (QCoreApplication, Qt, QEvent)
from mainUI import Ui_MainWindow
from format_generator import generate_formats

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.generate)

    def generate(self):
        generate_formats("DataSet/Enlaces.xlsx")


app = QApplication(sys.argv)
w = AppWindow()
w.show()

sys.exit(app.exec_())
w.end()
