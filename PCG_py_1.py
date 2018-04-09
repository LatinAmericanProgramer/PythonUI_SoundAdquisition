# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 10:46:31 2018

@author: Maine
"""
import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph import GraphicsLayoutWidget
from collections import deque
from PyQt5 import QtWidgets, QtCore, QtGui

import scipy.io.wavfile as wf 

import winsound as ws
from time import time
import numpy as np


class mainWindow(QMainWindow):
    def __init__(self):
        #Inicia el objeto QMainWindow
        QMainWindow.__init__(self)
        # Loads an .ui file & configure UI
        loadUi("PCG_ui_1.ui",self)
        # Variables
        self.fs = None
        self.data = None
        self.duration = None
        self.file_path = str
        self.plot_colors = ['#0072bd', '#d95319', '#bd0000']
        # Initial sub-functions
        self._configure_plot()
        self.buttons()
        
    
    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        """
        self.duration = np.size(self.data) * (1/self.fs)
        vectortime = np.linspace(0, self.duration, np.size(self.data))

        pcg = self.vec_nor(self.data)

        self._plt1.clear()
        self._plt1.plot(x=list(vectortime), y=list(pcg), pen=self.plot_colors[0])
        
    
    def open(self):
        """
        open a box to browse the audio file. Then converts the file into list 
        to properly read the path of the audio file 
        """
        self.file_path = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        self.file_path = list(self.file_path)         
        self.file_path = str(self.file_path[0])
        # NOTE: add an error box to saying "the audio format file most be WAV"
        self.fs, self.data = wf.read(self.file_path)
        # plots the signal loaded
        self._update_plot()
    
    def play(self):
        """
        play the audio file 
        """
        ws.PlaySound(self.file_path, ws.SND_FILENAME)
    
    def vec_nor(self, x):
        """
        Normalize the amplitude of a vector from -1 to 1
        """
        lenght=np.size(x)				# Get the length of the vector	
        xMax=max(x);					   # Get the maximun value of the vector
        nVec=np.zeros(lenght);		   # Initializate derivate vector
        nVec = np.divide(x, xMax)
        nVec=nVec-np.mean(nVec);
        nVec=np.divide(nVec,np.max(nVec));
        
        return nVec
        
    
    def buttons(self):
        """
        Configures the connections between signals and UI elements.
        """
        self.openButton.clicked.connect(self.open)
        self.playButton.clicked.connect(self.play)
    
    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        self.plt1.setBackground(background=None)
        self.plt1.setAntialiasing(True)
        self._plt1 = self.plt1.addPlot(row=1, col=1)
        self._plt1.setLabel('bottom', "Tiempo", "s")
        self._plt1.setLabel('left', "Amplitud", "Volt")
        self._plt1.showGrid(x=False, y=True)


#Instancia para iniciar una aplicacion en windows
app = QApplication(sys.argv)
#debemos crear un objeto para la clase creada arriba
_mainWindow = mainWindow()
    #muestra la ventana
_mainWindow.show()
    #ejecutar la aplicacion
app.exec_()