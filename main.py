import sys
import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtWidgets,QtCore
from PyQt5.uic import loadUi
import json

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 4  # Duration of recording

class VentanaPrincipal(QMainWindow):
    def __init__(self):
            super(VentanaPrincipal,self).__init__()
            self.setWindowTitle("DreamTech")
            # self.setWindowIcon("")
            loadUi('test.ui',self)  # Uso el diseño sin necesitar el codigo
            self.stackedWidget.setCurrentWidget(self.login)
            self.userData()

    def userData(self):        
        self.bt_cont.clicked.connect(lambda: self.instructions())
        self.bt_cont.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def instructions(self):
        self.stackedWidget.setCurrentWidget(self.consigna)
        self.bt_start.clicked.connect(lambda: self.recordWords())
        self.bt_start.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_start.hide()
        with open('data/Instrucciones.txt') as inst:
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
        # self.btn_record.setIcon(QtGui.QIcon('mic.png'))
        # self.btn_record.setIconSize(QtCore.QSize(24,24))
        with open("data/data.json","r") as f:
           data = json.load(f)
        self.word_labels = data['palabra']
        self.idx_words = 0
        self.updateWords()
        self.btn_record.setText("R")
        self.btn_record.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_record.clicked.connect(lambda: self.recordAudio())

    def updateWords(self):
        if self.idx_words >= len(self.word_labels):
            self.stackedWidget.setCurrentWidget(self.final_exp)
        else:
            self.lb_palabra.setText(self.word_labels[self.idx_words])
            self.btn_record.setEnabled(True)

    def recordAudio(self):
        if self.idx_words < len(self.word_labels):
            self.btn_record.setEnabled(False)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            if not os.path.exists(f'out/{self.enter_name.text()}'):
                os.makedirs(f'out/{self.enter_name.text()}')
            write(f'out/{self.enter_name.text()}/{self.word_labels[self.idx_words]}.wav', fs, myrecording)  # Save as WAV file 
            self.idx_words += 1
            self.updateWords()

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