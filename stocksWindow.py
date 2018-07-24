###################################################################
#                                                                 #
#                     PLOTTING A LIVE GRAPH                       #
#                  ----------------------------                   #
#            EMBED A MATPLOTLIB ANIMATION INSIDE YOUR             #
#            OWN GUI!                                             #
#                                                                 #
###################################################################

# import pdb
# pdb.set_trace()

import sys
import os
import PyQt5.sip
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QMainWindow, QApplication, QStyleFactory, QFrame, QGridLayout, QPushButton, QSizePolicy, QAction, QMenu, QMenuBar, QStatusBar
from PyQt5.uic import loadUi

import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt5agg", force=True)
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading
import pandas as pd
import glob

def path_to_temp(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class stocksWindow(QMainWindow):
    def __init__(self, stockFrame):
        super(stocksWindow, self).__init__()
        # ui = open('resources/stocksUI.ui','r') 
        self.setGeometry(100,100, 331, 487)
        
        self.setWindowTitle(path_to_temp(""))

        self.show()



if __name__== '__main__':
    print(os.getcwd())
    app = QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create('Plastique'))

    try:
        data = pd.read_csv('stocks.txt', sep='\t', header=None)
    except:
        data = pd.DataFrame(columns=["name", "price", "number"])
    data.columns = ["name", "price", "number"]
    stockFrame = pd.DataFrame(data)

    myGUI = stocksWindow(stockFrame)


    sys.exit(app.exec_())

''''''