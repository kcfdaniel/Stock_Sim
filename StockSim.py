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

comboBoxStock = None
ax1 = None
line = None

def path_to_temp(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        # base_path = os.path.abspath(".")
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class CustomMainWindow(QMainWindow):

    def __init__(self):

        super(CustomMainWindow, self).__init__()

        # Create Stock DataFrame
        try:
            data = pd.read_csv(path_to_temp('stocks.txt'), sep='\t', header=None)
        except:
            data = pd.DataFrame(columns=["name", "price", "number"])
        data.columns = ["name", "price", "number"]
        self.stockFrame = pd.DataFrame(data)

        # Define the geometry of the main window
        self.setGeometry(300, 300, 800, 700)
        self.setWindowTitle("Stock Sim")
        # self.setWindowTitle(path_to_temp(""))

        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(210,210,235,255).name())
        self.setCentralWidget(self.FRAME_A)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.FRAME_A.setLayout(self.horizontalLayout)

        # # Create FRAME_B
        self.LAYOUT_Left = QtWidgets.QVBoxLayout()
        self.horizontalLayout.addLayout(self.LAYOUT_Left)


        # # Place the zoom In button
        self.zoomInBtn = QPushButton(text = 'Zoom In')
        setCustomSize(self.zoomInBtn, 100, 50)
        self.zoomOutBtn = QPushButton(text = 'Zoom Out')
        setCustomSize(self.zoomOutBtn, 100, 50)
        self.zoomInBtn.clicked.connect(self.zoomInBtnAction)
        self.zoomOutBtn.clicked.connect(self.zoomOutBtnAction)
        self.LAYOUT_Left.addWidget(self.zoomInBtn)
        self.LAYOUT_Left.addWidget(self.zoomOutBtn)

        # # Place the matplotlib figure
        self.myFig = CustomFigCanvas(self.stockFrame)
        self.horizontalLayout.addWidget(self.myFig)

        # # Add other windows
        print("sdfg")
        self.transactionWindow = transactionWindow(self.stockFrame)
        self.stocksWindow = stocksWindow(self.stockFrame)

        # # Add menu bar
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)

        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")

        viewActionRecordTransaction = QAction("View Transaction", self, checkable = True)
        viewActionRecordTransaction.setStatusTip("View Transaction Window")
        viewActionRecordTransaction.setChecked(False)
        viewActionRecordTransaction.triggered.connect(self.toggleViewRecordTransaction)

        viewActionStocks = QAction("View Stocks", self, checkable = True)
        viewActionStocks.setStatusTip("View Stocks Window")
        viewActionStocks.setChecked(False)
        viewActionStocks.triggered.connect(self.toggleViewStocks)

        viewMenu.addAction(viewActionRecordTransaction)
        viewMenu.addAction(viewActionStocks)

        # Add status bar
        self.statusbar = self.statusBar()

        # Add the callbackfunc to ..
        myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (self.addData_callbackFunc,self.stockFrame,))
        myDataLoop.start()

        self.show()

    ''''''

    def toggleViewRecordTransaction(self, state):
        if state:
            self.transactionWindow.show()
            self.statusbar.showMessage("On")
        else:
            self.transactionWindow.hide()
            self.statusbar.showMessage("Off")

    ''''''

    def toggleViewStocks(self, state):
        if state:
            self.stocksWindow.show()
            self.statusbar.showMessage("On")
        else:
            self.stocksWindow.hide()
            self.statusbar.showMessage("Off")

    ''''''

    def zoomInBtnAction(self):
        # print("zoom in")
        self.myFig.zoomIn(5)

    ''''''


    def zoomOutBtnAction(self):
        # print("zoom out")
        self.myFig.zoomOut(5)

    ''''''
    def addData_callbackFunc(self, value):
        # print("Add data: " + str(value))
        self.myFig.addData(value)

''' End Class '''


class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    # def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
    #     self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)       
    #     self.items = self.items[:position] + self.items[position + rows:]
    #     self.endRemoveRows()

    #     return True

    # def insertRows(self, position, rows=1, index=QtCore.QModelIndex()):
    #     indexSelected=self.index(position, 0)
    #     itemSelected=indexSelected.data().toPyObject()

    #     self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
    #     for row in range(rows):
    #         self.items.insert(position + row,  "%s_%s"% (itemSelected, self.added))
    #         self.added+=1
    #     self.endInsertRows()
    #     return True

''''''

class transactionWindow(QMainWindow):
    def __init__(self, stockFrame):
        super(transactionWindow, self).__init__()
        loadUi(path_to_temp('transactionUI.ui'), self)
        self.setGeometry(100,300, 564, 242)
        
        self.stockFrame = stockFrame

        self.comboBoxStock.clear()
        self.comboBoxStock.addItems(self.stockFrame['name'].astype(str))

        global comboBoxStock
        comboBoxStock = self.comboBoxStock

        self.pushButtonRecord.setShortcut("Return")        
        self.pushButtonRecord.clicked.connect(self.recordTransaction)

        try:
            self.data = pd.read_csv(path_to_temp('transactions.txt'), sep='\t', header=None)
        except:
            self.data = pd.DataFrame(columns=["Name", "Price", "Action"])
        self.data.columns = ["Name", "Price", "Action"]
        self.model = PandasModel(self.data)
        
        self.tableViewTransaction.setModel(self.model)
        
        self.execute = False
        self.change = False
        self.executeTransactionLoop = threading.Thread(name = 'executeTransactionLoop', target = self.executeTransaction, daemon = True, args = ())
        self.executeTransactionLoop.start()
        self.pushButtonExecute.clicked.connect(self.executeTransactionLoopStart)


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Delete or e.key() == QtCore.Qt.Key_Backspace:
            model = self.model
            indices = self.tableViewTransaction.selectionModel().selectedRows() 
            for i in indices:
                self.data.drop(i.row(), inplace = True)
            self.data.reset_index(drop = True, inplace = True)
        
            self.tableViewTransaction.model().layoutChanged.emit()
            self.data.to_csv(path_to_temp('transactions.txt'), sep='\t', index=False, header=False)

    def executeTransactionLoopStart(self):
        self.execute = True

    def recordTransaction(self):
        name = self.comboBoxStock.currentText()
        price = self.lineEditMoney.text()
        action = self.comboBoxAction.currentText()
        self.data.loc[len(self.data.index)] = [name, price, action]
        self.tableViewTransaction.model().layoutChanged.emit()
        self.data.to_csv(path_to_temp('transactions.txt'), sep='\t', index=False, header=False)

    def executeTransaction(self):
        while True:
            time.sleep(0.1)
            if self.execute == True:
                while len(self.data.index) > 0:
                    name = self.data.loc[0]["Name"]
                    price = self.data.loc[0]["Price"]
                    try:
                        price = float(price)
                    except:
                        price = 0
                    action = self.data.loc[0]["Action"]

                    if action == "Sell":
                        price = -price
                    if not self.stockFrame.loc[self.stockFrame['name'] == name, 'price'].empty:
                        self.stockFrame.loc[self.stockFrame['name'] == name, 'price'] = round(self.stockFrame.loc[self.stockFrame['name'] == name, 'price'] + price, 2)
                        for i in range(len(line)):
                            line[i].set_label(self.stockFrame["name"][i] + " " + str(self.stockFrame["price"][i]))
                    self.data.drop(0, inplace = True)
                    self.data.reset_index(drop = True, inplace = True)
                    time.sleep(0.3)
                    ax1.legend(handles = line, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=False, shadow=False)
                    self.data.to_csv(path_to_temp('transactions.txt'), sep='\t', index=False, header=False)
                    time.sleep(0.7)
                    # print("9")
                    self.change = True
                    # print("10")
                self.stockFrame.to_csv(path_to_temp('stocks.txt'), sep='\t', index=False, header=False)
                self.execute = False


class stocksWindow(QMainWindow):
    def __init__(self, stockFrame):
        super(stocksWindow, self).__init__()
        loadUi(path_to_temp('stocksUI.ui'), self)
        self.setGeometry(100,100, 331, 487)
        
        self.stockFrame = stockFrame
        self.model = PandasModel(self.stockFrame)
        self.tableViewStocks.setModel(self.model)

        self.addStockButton.setShortcut("Return")        
        self.addStockButton.clicked.connect(self.addStock)

    def addStock(self):
        name = self.stockNameLineEdit.text()
        price = self.stockPriceLineEdit.text()
        price = round(float(price),2)
        number = self.stockNumberLineEdit.text()
        self.stockFrame.loc[len(self.stockFrame.index)] = [name, price, number]
        self.tableViewStocks.model().layoutChanged.emit()
        
        self.stockFrame.to_csv(path_to_temp('stocks.txt'), sep='\t', index=False, header=False)
        comboBoxStock.clear()
        comboBoxStock.addItems(self.stockFrame['name'])


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Delete or e.key() == QtCore.Qt.Key_Backspace:
            model = self.model
            indices = self.tableViewStocks.selectionModel().selectedRows() 
            for i in indices:
                self.stockFrame.drop(i.row(), inplace = True)
            self.stockFrame.reset_index(drop = True, inplace = True)

            self.stockFrame.to_csv(path_to_temp('stocks.txt'), sep='\t', index=False, header=False)
            self.tableViewStocks.model().layoutChanged.emit()

            comboBoxStock.clear()
            comboBoxStock.addItems(self.stockFrame['name'])

class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self, stockFrame):

        self.addedData = []
        self.yLine = []
        self.line = []
        self.line_head = []
        self.stockFrame = stockFrame
        # self.line_tail = []
        global line
        line = self.line
        
        # print(matplotlib.__version__)

        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)

        # The window
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        global ax1
        ax1 = self.ax1

        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('price')
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 10)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = False)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        # lines = [self.line[0], self.line_tail[0], self.line_head[0]]
        # lines = [self.line[0], self.line_head[0]]
        # for l in lines:
        #     l.set_data([], [])
        pass

    def addData(self, value):
        if len(self.addedData) == len(value):
            # print(value)
            [self.addedData[i].append(value[i]) for i in range(len(value))]
        else:
            # print(len(self.addedData))
            self.addedData = [[value[i]] for i in range(len(value))]

            if len(value) > len(self.line):
                for i in range(len(value) - len(self.line)):
                    # print("i: " + str(i))
                    # print(value[len(self.line) + i])
                    color = self.uniqueish_color()
                    # print(color)
                    self.yLine.append((self.n * 0.0) + (value[len(self.line)])) #initial value + initial offset_value
                    self.line.append(Line2D([], [], color=color, label = str(self.stockFrame["name"][len(self.line)]) + " " + str(self.stockFrame["price"][len(self.line)])))
                    # self.line_tail.append(Line2D([], [], color='red', linewidth=2))
                    self.line_head.append(Line2D([], [], color=color, marker='o', markeredgecolor=color))
                    self.ax1.add_line(self.line[-1])
                    # self.ax1.add_line(self.line_tail[-1])
                    self.ax1.add_line(self.line_head[-1])
                self.ax1.legend(handles = self.line, loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=False, shadow=False)
            else:
                for i in range(len(self.line)):
                    self.yLine.pop()
                    line = self.line.pop()
                    line_head = self.line_head.pop()
                    
                    line.remove()
                    line_head.remove()

                    del line
                    del line_head
                    

                for i in range(len(value) - len(self.line)):
                    # print("i: " + str(i))
                    # print(value[len(self.line) + i])
                    color = self.uniqueish_color()
                    # print(color)
                    self.yLine.append((self.n * 0.0) + (value[len(self.line)])) #initial value + initial offset_value
                    self.line.append(Line2D([], [], color=color, label = self.stockFrame["name"][len(self.line)] + " " + str(self.stockFrame["price"][len(self.line)])))
                    # self.line_tail.append(Line2D([], [], color='red', linewidth=2))
                    self.line_head.append(Line2D([], [], color=color, marker='o', markeredgecolor=color))
                    self.ax1.add_line(self.line[-1])
                    # self.ax1.add_line(self.line_tail[-1])
                    self.ax1.add_line(self.line_head[-1])

                # for i in range(len(self.line) - len(value)):
                #     self.yLine.pop()
                #     line = self.line.pop()
                #     line_head = self.line_head.pop()

                #     line.remove()
                #     line_head.remove()

                #     del line
                #     del line_head
                    
                self.ax1.legend(handles = self.line, loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=False, shadow=False)

        # for i in self.line:
        #     print(i)
        # self.ax1.add_line(self.line_head[0])
        # self.addedData.append(value)
    def uniqueish_color(self):
            """There're better ways to generate unique colors, but this isn't awful."""
            return matplotlib.cm.gist_ncar(np.random.random())

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        # bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()

    def zoomOut(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        # bottom -= value
        top += value
        self.ax1.set_ylim(bottom,top)
        self.draw()


    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            # print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        if len(self.addedData) > 0:
            for i in range(len(self.addedData)):
                # print("i: " + str(i))
                while(len(self.addedData[i]) > 0):
                    self.yLine[i] = np.roll(self.yLine[i], -1)
                    self.yLine[i][-1] = self.addedData[i][0]
                    del(self.addedData[i][0])


                self.line[i].set_data(self.n[ 0 : self.n.size - margin ], self.yLine[i][ 0 : self.n.size - margin ])
                # self.line_tail[i].set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.yLine[i][-10:-1 - margin], self.yLine[i][-1 - margin]))
                self.line_head[i].set_data(self.n[-1 - margin], self.yLine[i][-1 - margin])
                # self._drawn_artists = [self.line[i], self.line_tail[i], self.line_head[i]]
            self._drawn_artists = [self.line[i] for i in range(len(self.addedData))] + [self.line_head[i] for i in range(len(self.addedData))]
        # handles, labels = self.ax1.get_legend_handles_labels()
        # self.ax1.legend(handles, labels)
''' End Class '''


# # You need to setup a signal slot mechanism, to 
# # send data to your GUI in a thread-safe way.
# # Believe me, if you don't do this right, things
# # go very very wrong..
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(list)

# ''' End Class '''



def dataSendLoop(addData_callbackFunc,stockFrame):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)

    
    while(True):
        time.sleep(0.1)
        mySrc.data_signal.emit(stockFrame['price'].tolist()) # <- Here you emit a signal!
    ###
###

def setCustomSize(x, width, height):
    sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(x.sizePolicy().hasHeightForWidth())
    x.setSizePolicy(sizePolicy)
    x.setMinimumSize(QtCore.QSize(width, height))
    x.setMaximumSize(QtCore.QSize(width, height))

''''''



if __name__== '__main__':
    print(os.getcwd())
    app = QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow()


    sys.exit(app.exec_())

''''''