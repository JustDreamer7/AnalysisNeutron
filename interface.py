# Form implementation generated from reading ui file '.\interface.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 511)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        MainWindow.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
        MainWindow.setStyleSheet("background-color: rgb(42, 55, 127);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.runPassport = QtWidgets.QPushButton(self.centralwidget)
        self.runPassport.setGeometry(QtCore.QRect(40, 400, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.runPassport.setFont(font)
        self.runPassport.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.runPassport.setObjectName("runPassport")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(40, 191, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateEdit.setFont(font)
        self.dateEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(40, 240, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateEdit_2.setFont(font)
        self.dateEdit_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(40, 220, 131, 20))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 150, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.openDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.openDirectory.setGeometry(QtCore.QRect(310, 270, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.openDirectory.setFont(font)
        self.openDirectory.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        self.openDirectory.setAutoFillBackground(False)
        self.openDirectory.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.openDirectory.setAutoExclusive(True)
        self.openDirectory.setObjectName("openDirectory")
        self.openFileDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.openFileDirectory.setGeometry(QtCore.QRect(310, 200, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.openFileDirectory.setFont(font)
        self.openFileDirectory.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        self.openFileDirectory.setAutoFillBackground(False)
        self.openFileDirectory.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.openFileDirectory.setAutoExclusive(True)
        self.openFileDirectory.setObjectName("openFileDirectory")
        self.runPassport_2 = QtWidgets.QPushButton(self.centralwidget)
        self.runPassport_2.setGeometry(QtCore.QRect(40, 330, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.runPassport_2.setFont(font)
        self.runPassport_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.runPassport_2.setObjectName("runPassport_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(260, 410, 95, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(260, 440, 231, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 360, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Справка Нейтрон"))
        self.runPassport.setText(_translate("MainWindow", "Run \n"
" Passport"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Паспорт НЕЙТРОН</p><p><br/></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Выберите дату:"))
        self.openDirectory.setText(_translate("MainWindow", "Папка \n"
" сохранения"))
        self.openFileDirectory.setText(_translate("MainWindow", "Папка \n"
" файлов Нейтрон"))
        self.runPassport_2.setText(_translate("MainWindow", "Данные \n"
" без маски"))
        self.radioButton.setText(_translate("MainWindow", "993"))
        self.radioButton_2.setText(_translate("MainWindow", "Cреднее значение за период"))
        self.label_5.setText(_translate("MainWindow", "Выберите P0 для обработки:"))
