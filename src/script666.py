from mesFonctions import *

import sys
import io
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

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

        # Zone de texte pour la question
        self.text_edit = QTextEdit(self)
        self.text_edit2 = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit2.setReadOnly(True)
        font = QFont()
        font.setPointSize(16)  # Taille de la police pour QTextEdit
        self.text_edit.setFont(font)
        self.text_edit2.setFont(font)

        # Rediriger stdout vers la zone de texte
        sys.stdout = EmittingStream(self.text_edit)

        # Layout horizontal pour les zones de texte
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(self.text_edit2)

        # Layout vertical pour le bouton en haut et les zones de texte côte à côte en dessous
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.button)
        main_layout.addLayout(text_layout)
        self.setLayout(main_layout)

    def adjustSizeAndPosition(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            window_width, window_height = 1300, 800
            self.setGeometry(geometry.x() + 400, geometry.y() + 100, window_width, window_height)
        else:
            self.setGeometry(100, 100, 300, 200)

    @pyqtSlot()
    def execute_functions(self):
        self.text_edit.clear()
        self.text_edit2.clear()
        
        #screenshot(nomPage, screenshot_path)
        
        self.button.setStyleSheet("QPushButton {background-color: blue; font-size: 20px;}")
        QTimer.singleShot(500, self.reset_button_color)  # Définir un délai de 2 secondes (2000 ms)
        question, reponse = api_GPT()
        
        # Rétablir la couleur d'origine du bouton
        self.button.setStyleSheet("QPushButton {background-color: red; font-size: 20px;}")

        self.text_edit2.insertPlainText(reponse)

# Exécution de l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PokerHelperApp()
    ex.show()
    sys.exit(app.exec_())
