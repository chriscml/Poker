from mesFonctions5joueur import *

import sys
import io
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont

class EmittingStream(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Insérer le message directement à la fin du QTextEdit
        self.text_widget.moveCursor(QtGui.QTextCursor.End)
        self.text_widget.insertPlainText(message)

class PokerHelperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Poker Helper')
        self.adjustSizeAndPosition()

        # Bouton pour exécuter les fonctions
        self.button = QPushButton('Exécuter', self)
        self.button.setStyleSheet("QPushButton {background-color: red; font-size: 20px;}")
        self.button.clicked.connect(self.execute_functions)

        # Zone de texte pour les messages de la console
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        font = QFont()
        font.setPointSize(16)  # Taille de la police pour QTextEdit
        self.text_edit.setFont(font)

        # Rediriger stdout vers la zone de texte
        sys.stdout = EmittingStream(self.text_edit)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def adjustSizeAndPosition(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            window_width, window_height = 1300, 800
            self.setGeometry(geometry.x() +400 , geometry.y() +100 , window_width, window_height)
        else:
            self.setGeometry(100, 100, 300, 200)


    @pyqtSlot()
    def execute_functions(self):
        self.text_edit.clear()

        screenshot(nomPage, screenshot_path)
        envoyerAGPT(nomPageConseilDePokerEnDirect)
       # test()

# Exécution de l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PokerHelperApp()
    ex.show()
    sys.exit(app.exec_())


