import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtWidgets,QtCore
from PyQt5.uic import loadUi
import json
import time # para delays
import threading

class VentanaPrincipal(QMainWindow):
    def __init__(self):
            super(VentanaPrincipal,self).__init__()
            loadUi('test.ui',self)  # Uso el diseño sin necesitar el codigo
            # Arranca con la pantalla de consignas
            self.stackedWidget.setCurrentWidget(self.consigna) 
            # Conexion de Botones
            self.bt_start.clicked.connect(lambda: self.recordWords())
            self.bt_start.hide()
            # Muestra instrucciones
            self.instructions()

    def instructions(self):
        with open('Instrucciones.txt') as inst:
            text = inst.read()
        self.inst_labels = text.split('#')
        self.lb_consigna.setText(self.inst_labels[0])
        self.idx_labels = 1
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateInstructions)
        self.timer.start(2*1000)

    def updateInstructions(self):
        if self.idx_labels >= len(self.inst_labels):
            self.bt_start.show()
            self.timer.stop()
        else:
            self.lb_consigna.setText(self.inst_labels[self.idx_labels])
            self.idx_labels += 1

    def recordWords(self):
        self.stackedWidget.setCurrentWidget(self.palabra)
        with open("data.json","r") as f:
           data = json.load(f)
        self.word_labels = data['palabra']
        self.lb_palabra.setText(self.word_labels[0])
        self.idx_words = 1
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateWords)
        self.timer.start(4*1000)

    def updateWords(self):
        if self.idx_words >= len(self.word_labels):
            self.timer.stop()
        else:
            self.lb_palabra.setText(self.word_labels[self.idx_words])
            self.idx_words += 1

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