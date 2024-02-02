# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pokerHelper.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1076, 762)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(7, 7, 57);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.modes = QtWidgets.QWidget(self.centralwidget)
        self.modes.setStyleSheet("background-color: #222233;")
        self.modes.setObjectName("modes")
        self.gridLayout = QtWidgets.QGridLayout(self.modes)
        self.gridLayout.setObjectName("gridLayout")
        self.windows11 = QtWidgets.QPushButton(self.modes)
        self.windows11.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 0, 127);\n"
"color: rgb(216, 216, 216);\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"border-color: rgb(147, 147, 147);\n"
"font: 12pt \"MingLiU_HKSCS-ExtB\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgb(121, 121, 121); \n"
"color: white;\n"
"font-size: 20px;\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"}")
        self.windows11.setObjectName("windows11")
        self.gridLayout.addWidget(self.windows11, 4, 0, 1, 1)
        self.windows10 = QtWidgets.QPushButton(self.modes)
        self.windows10.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 0, 127);\n"
"color: rgb(216, 216, 216);\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"border-color: rgb(147, 147, 147);\n"
"font: 12pt \"MingLiU_HKSCS-ExtB\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgb(121, 121, 121); \n"
"color: white;\n"
"font-size: 20px;\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"}")
        self.windows10.setObjectName("windows10")
        self.gridLayout.addWidget(self.windows10, 2, 0, 1, 1)
        self.joueurs6 = QtWidgets.QPushButton(self.modes)
        self.joueurs6.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 0, 127);\n"
"color: rgb(216, 216, 216);\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"border-color: rgb(147, 147, 147);\n"
"font: 12pt \"MingLiU_HKSCS-ExtB\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgb(121, 121, 121); \n"
"color: white;\n"
"font-size: 20px;\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"}")
        self.joueurs6.setObjectName("joueurs6")
        self.gridLayout.addWidget(self.joueurs6, 4, 3, 1, 1)
        self.joueurs5 = QtWidgets.QPushButton(self.modes)
        self.joueurs5.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 0, 127);\n"
"color: rgb(216, 216, 216);\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"border-color: rgb(147, 147, 147);\n"
"font: 12pt \"MingLiU_HKSCS-ExtB\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgb(121, 121, 121); \n"
"color: white;\n"
"font-size: 20px;\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"}")
        self.joueurs5.setObjectName("joueurs5")
        self.gridLayout.addWidget(self.joueurs5, 2, 3, 1, 1)
        self.verticalLayout.addWidget(self.modes)
        self.go = QtWidgets.QWidget(self.centralwidget)
        self.go.setStyleSheet("background-color: #222233;\n"
"")
        self.go.setObjectName("go")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.go)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.boutonGo = QtWidgets.QPushButton(self.go)
        self.boutonGo.setStyleSheet("QPushButton {background-color: rgb(30, 30, 240);\n"
"color: rgb(240, 245, 253);\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"border-color: rgb(147, 147, 147);\n"
"font: 12pt \"Lucida Sans Unicode\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgb(250, 50, 50); \n"
"color: white;\n"
"font-size: 20px;\n"
"border: 2px solid white;\n"
"border-radius: 5px;\n"
"}")
        self.boutonGo.setObjectName("boutonGo")
        self.verticalLayout_2.addWidget(self.boutonGo)
        self.verticalLayout.addWidget(self.go)
        self.contenu = QtWidgets.QWidget(self.centralwidget)
        self.contenu.setStyleSheet("background-color: #222233;")
        self.contenu.setObjectName("contenu")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.contenu)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textQuestion = QtWidgets.QTextEdit(self.contenu)
        self.textQuestion.setStyleSheet("background-color: rgb(66, 66, 66);")
        self.textQuestion.setObjectName("textQuestion")
        self.horizontalLayout.addWidget(self.textQuestion)
        self.textReponse = QtWidgets.QPlainTextEdit(self.contenu)
        self.textReponse.setStyleSheet("background-color: rgb(66, 66, 66);")
        self.textReponse.setObjectName("textReponse")
        self.horizontalLayout.addWidget(self.textReponse)
        self.labelImage = QtWidgets.QLabel(self.contenu)
        self.labelImage.setObjectName("labelImage")
        self.horizontalLayout.addWidget(self.labelImage)
        self.verticalLayout.addWidget(self.contenu)
        self.log = QtWidgets.QWidget(self.centralwidget)
        self.log.setObjectName("log")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.log)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.log)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.log)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.windows11.setText(_translate("MainWindow", "Windows 11"))
        self.windows10.setText(_translate("MainWindow", "Windows 10"))
        self.joueurs6.setText(_translate("MainWindow", "6 Joueurs"))
        self.joueurs5.setText(_translate("MainWindow", "5 Joueurs"))
        self.boutonGo.setText(_translate("MainWindow", "GO !"))
        self.labelImage.setText(_translate("MainWindow", "IIMAGE"))
