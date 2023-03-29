import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtWidgets,QtCore
from PyQt5.uic import loadUi
import json
import time    #para delays
import threading

class VentanaPrincipal(QMainWindow):
    def __init__(self):
            super(VentanaPrincipal,self).__init__()
            loadUi('test.ui',self)  #uso el diseño sin necesitar el codigo del diseño
            #arranca con la pantalla de consignas
            self.stackedWidget.setCurrentWidget(self.consigna) 
            self.bt_start.hide()
            
           #Funciones de Labels
            #self.instrucciones()
            #self.start()
            self.t = threading.Timer(0.5, self.instrucciones)
            self.t.start()
            #self.mostrar()
            self.t2 = threading.Timer(0.5, self.mostrar)
            self.t2.start()
            #Conexion de Botones
            self.bt_start.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.palabra))

    

    def instrucciones(self):
        with open('Instrucciones.txt') as inst:
            text = inst.read()
        labels = text.split('#')
        print(labels)
        self.lb_consigna.setText(str(labels[0]) )
        time.sleep(2)
        self.lb_consigna.setText(str(labels[1]) )
        time.sleep(2)
        self.lb_consigna.setText(str(labels[2]) )
        self.bt_start.show()

    def mostrar(self):
        with open("data.json","r") as f:
           data = json.load(f)

        for i in range (len(data['palabra'])):
            self.lb_palabra.setText(data['palabra'][i])
            time.sleep(2.5)

    '''
    def start(self):
        self.timerA = QtCore.QTimer()
        self.timerA.timeout.connect(self.instrucciones)
        #self.timerA.timeout.connect(self.pamitomi)
        self.timerA.start(10)
    '''

        


if __name__ == "__main__":
    app=QApplication(sys.argv)
    mi_app=VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())