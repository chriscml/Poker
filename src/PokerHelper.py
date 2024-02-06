import sys
import io
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_pokerHelper import Ui_MainWindow  # Importez la classe générée
import openai  # Assurez-vous d'importer la bibliothèque openai
from utility import *
from mesFonctions5JoueursW11 import *
from mesFonctions5JoueursW10 import *
from mesFonctions6JoueursW10 import *
#from mesFonctions6JoueursW11 import *

class EmittingStream(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Insérer le message directement à la fin du QTextEdit
        self.text_widget.moveCursor(QtGui.QTextCursor.End)
        self.text_widget.insertPlainText(message)

class PokerHelperApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.adjustSizeAndPosition()
        self.initVar()
        self.clearAll()
        self.colorerBoutons()

        # Connectez vos signaux et slots ici
        self.joueurs5.clicked.connect(self.mode5Joueurs)
        self.joueurs6.clicked.connect(self.mode6Joueurs)
        self.windows10.clicked.connect(self.modeW10)
        self.windows11.clicked.connect(self.modeW11)
        self.boutonGo.clicked.connect(self.executerScript)
    
    def initVar(self):
        self.flag5joueurs = True
        self.flag6joueurs = False
        self.flagW10 = True
        self.flagW11 = False
    
    def executerScript(self):
        self.clearAll()
        if self.flag5joueurs:
            # Cas pour 5 joueurs
            if self.flagW10:
                # Cas pour Windows 10
                self.w10joueurs5()
            elif self.flagW11:
                # Cas pour Windows 11
                self.w11joueurs5()
                
        elif self.flag6joueurs:
            # Cas pour 6 joueurs
            if self.flagW10:
                # Cas pour Windows 10
                self.w10joueurs6()
            elif self.flagW11:
                # Cas pour Windows 11
                self.w11joueurs6()
                
    def clearAll(self):
        self.textQuestion.clear()  
        self.textReponse.clear()  
        self.progressBar.setValue(0)
    
    def afficherImageUI(self):
        image_path = '../assets/capture.png'
        pixmap = QPixmap(image_path).scaled(600, 600, QtCore.Qt.KeepAspectRatio)
        # Afficher l'image à droite des zones de texte
        self.labelImage.setPixmap(pixmap)
    
    def api_GPT(self, fct):
        questionGPT = fct()

        client = openai.OpenAI(api_key="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")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional poker player, skilled in analyzing the whole game and make the perfect move every time it's your turn."},
                {"role": "user", "content": questionGPT + "Give me the move to do in bold and give me an explanation in one line (less than 20 words) "}
            ]
        )

        reponse = completion.choices[0].message.content
        return reponse 
            
    def w10joueurs5(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        sys.stdout = EmittingStream(self.textQuestion)
        
        self.progressBar.setValue(25)
        
        reponse = self.api_GPT(remplirJSON5joueursW10)
        
        self.textReponse.insertPlainText(reponse)
        self.progressBar.setValue(100)
        
    def w10joueurs6(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        sys.stdout = EmittingStream(self.textQuestion)
        
        reponse = self.api_GPT(remplirJSON6joueursW10)
        
        self.textReponse.insertPlainText(reponse)
        
    def w11joueurs5(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        
        reponse = self.api_GPT(remplirJSON5joueursW11)
        
        self.textReponse.insertPlainText(reponse)
        
    def w11joueurs6(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
    
        

    def adjustSizeAndPosition(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            window_width, window_height = 1800, 900
            self.setGeometry(geometry.x() + 25, geometry.y() + 100, window_width, window_height)
        else:
            self.setGeometry(25, 25, 1700, 900)

    def mode5Joueurs(self):
        self.flag5joueurs = not self.flag5joueurs
        self.flag6joueurs = not self.flag6joueurs
        self.colorerBoutons()
            
    def mode6Joueurs(self):
        self.flag6joueurs = not self.flag6joueurs
        self.flag5joueurs = not self.flag5joueurs
        self.colorerBoutons()
        
    def modeW10(self):
        self.flagW10 = not self.flagW10
        self.flagW11 = not self.flagW11
        self.colorerBoutons()
        
    def modeW11(self):
        self.flagW11 = not self.flagW11
        self.flagW10 = not self.flagW10
        self.colorerBoutons()

    def colorerBoutons(self):
        self.afficherImageUI()
        
        style = "font-size: 16pt; font-weight: bold; color : white;"  # Modifiez la taille et le gras selon vos besoins
        self.textQuestion.setStyleSheet(style)
        self.textReponse.setStyleSheet(style)
        # Joueurs 5
        if self.flag5joueurs:
            self.joueurs5.setStyleSheet("""
                QPushButton {
                    background-color: rgb(50, 200, 50);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)
        else:
            self.joueurs5.setStyleSheet("""
                QPushButton {
                    background-color: rgb(25, 25, 127);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)

        # Joueurs 6
        if self.flag6joueurs:
            self.joueurs6.setStyleSheet("""
                QPushButton {
                    background-color: rgb(50, 200, 50);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)
        else:
            self.joueurs6.setStyleSheet("""
                QPushButton {
                    background-color: rgb(25, 25, 127);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)

        # Windows 10
        if self.flagW10:
            self.windows10.setStyleSheet("""
                QPushButton {
                    background-color: rgb(50, 200, 50);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)
        else:
            self.windows10.setStyleSheet("""
                QPushButton {
                    background-color: rgb(25, 25, 127);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)

        # Windows 11
        if self.flagW11:
            self.windows11.setStyleSheet("""
                QPushButton {
                    background-color: rgb(50, 200, 50);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)
        else:
            self.windows11.setStyleSheet("""
                QPushButton {
                    background-color: rgb(25, 25, 127);
                    color: rgb(216, 216, 216);
                    border: 2px solid white;
                    border-radius: 5px;
                    font: 12pt;
                }

                QPushButton:hover {
                    background-color: rgb(121, 121, 121); 
                    color: white;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
            """)

            
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = PokerHelperApp()
    mainWindow.show()
    sys.exit(app.exec_())
