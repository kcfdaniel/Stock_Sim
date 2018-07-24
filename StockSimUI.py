# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StockSimUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RecordTransactionWindow(object):
    def setupUi(self, RecordTransactionWindow):
        RecordTransactionWindow.setObjectName("RecordTransactionWindow")
        RecordTransactionWindow.resize(198, 189)
        self.centralwidget = QtWidgets.QWidget(RecordTransactionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 18, 161, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditMoney = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditMoney.setObjectName("lineEditMoney")
        self.gridLayout.addWidget(self.lineEditMoney, 1, 1, 1, 1)
        self.comboBoxStock = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxStock.setObjectName("comboBoxStock")
        self.gridLayout.addWidget(self.comboBoxStock, 0, 1, 1, 1)
        self.comboBoxAction = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxAction.setObjectName("comboBoxAction")
        self.comboBoxAction.addItem("")
        self.comboBoxAction.addItem("")
        self.gridLayout.addWidget(self.comboBoxAction, 2, 1, 1, 1)
        self.labelMoney = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelMoney.setObjectName("labelMoney")
        self.gridLayout.addWidget(self.labelMoney, 1, 0, 1, 1)
        self.labelAction = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelAction.setObjectName("labelAction")
        self.gridLayout.addWidget(self.labelAction, 2, 0, 1, 1)
        self.labelStock = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelStock.setObjectName("labelStock")
        self.gridLayout.addWidget(self.labelStock, 0, 0, 1, 1)
        self.pushButtonSubmit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSubmit.setGeometry(QtCore.QRect(40, 140, 113, 32))
        self.pushButtonSubmit.setObjectName("pushButtonSubmit")
        RecordTransactionWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RecordTransactionWindow)
        QtCore.QMetaObject.connectSlotsByName(RecordTransactionWindow)

    def retranslateUi(self, RecordTransactionWindow):
        _translate = QtCore.QCoreApplication.translate
        RecordTransactionWindow.setWindowTitle(_translate("RecordTransactionWindow", "Record Transaction"))
        self.comboBoxAction.setItemText(0, _translate("RecordTransactionWindow", "Buy"))
        self.comboBoxAction.setItemText(1, _translate("RecordTransactionWindow", "Sell"))
        self.labelMoney.setText(_translate("RecordTransactionWindow", "Money"))
        self.labelAction.setText(_translate("RecordTransactionWindow", "Action"))
        self.labelStock.setText(_translate("RecordTransactionWindow", "Stock"))
        self.pushButtonSubmit.setText(_translate("RecordTransactionWindow", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RecordTransactionWindow = QtWidgets.QMainWindow()
    ui = Ui_RecordTransactionWindow()
    ui.setupUi(RecordTransactionWindow)
    RecordTransactionWindow.show()
    sys.exit(app.exec_())

