import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtWidgets,QtCore
from PyQt5.uic import loadUi

import time    #para delays

class VentanaPrincipal(QMainWindow):
    def __init__(self):
            super(VentanaPrincipal,self).__init__()
            loadUi('test.ui',self)  #uso el diseño sin necesitar el codigo del diseño

            #Conexion de Botones
            self.bt_start.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.palabra))

           #Funciones de Labels
            self.instrucciones()

    def instrucciones(self):
        f = open('Instrucciones.txt','r')
        lines=f.readlines()
        [print(linea) for linea in f.readlines()]
        #self.lb_consigna.setText(str(lines[0]) )
        


if __name__ == "__main__":
    app=QApplication(sys.argv)
    mi_app=VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())