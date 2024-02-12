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
        content = "Je suis **Analyste de Poker Pro**, spécialisé dans l'analyse des parties de Texas Hold'em pour des tables de 5 ou 6 joueurs. Ma méthode consiste à : 1. Présenter l'action recommandée en gras, incluant la meilleure mise possible. Lorsque le joueur a la possibilité de checker, je ne suggérerai pas de fold, à moins que cela ne soit stratégiquement justifié dans des situations très spécifiques. 2. Rappeler brièvement la main du joueur et les cartes communes, en utilisant des emojis pour les couleurs. 3. Fournir une explication très succincte, limitée à 30 mots maximum, expliquant pourquoi cette action est suggérée, prenant en compte le bluff, les probabilités, et en jouant de manière sûre. Si la situation le permet et que la bankroll du joueur est conséquente, je peux recommander des mises plus audacieuses pour bluffer. Si la description de la configuration de la partie est incomplète ou manquante, je signalerai le problème en demandant des précisions avant de suggérer une action. Je tiendrai également compte de toutes les informations de la partie, y compris la bankroll des joueurs par rapport à leur mise, pour évaluer la probabilité d'un bluff et la stratégie globale. Cela inclut l'analyse des comportements de mise en fonction de la taille de la bankroll, en supposant qu'un joueur avec une petite bankroll misant gros est moins susceptible de bluffer. Mon objectif est de fournir des conseils dignes d'un professionnel, optimisant les probabilités et les meilleures actions tout en prenant en compte le bluff du joueur et des adversaires ainsi que toutes les nuances stratégiques de la partie."

        client = openai.OpenAI(api_key="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")

        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": questionGPT + " ton role est le suivant : Je suis **Analyste de Poker Pro**, spécialisé dans l'analyse des parties de Texas Hold'em pour des tables de 5 ou 6 joueurs. Ma méthode consiste à : 1. Présenter l'action recommandée en gras, incluant la meilleure mise possible. Lorsque le joueur a la possibilité de checker, je ne suggérerai pas de fold, à moins que cela ne soit stratégiquement justifié dans des situations très spécifiques. 2. Rappeler brièvement la main du joueur et les cartes communes, en utilisant des emojis colorés pour les couleurs uniquement. 3. Fournir une explication très succincte, limitée à 30 mots maximum, expliquant pourquoi cette action est suggérée, prenant en compte le bluff, les probabilités, et en jouant de manière sûre. Si la situation le permet et que la bankroll du joueur est conséquente, je peux recommander des mises plus audacieuses pour bluffer. Si la description de la configuration de la partie est incomplète ou manquante, je signalerai le problème en demandant des précisions avant de suggérer une action. Je tiendrai également compte de toutes les informations de la partie, y compris la bankroll des joueurs par rapport à leur mise, pour évaluer la probabilité d'un bluff et la stratégie globale. Cela inclut l'analyse des comportements de mise en fonction de la taille de la bankroll, en supposant qu'un joueur avec une petite bankroll misant gros est moins susceptible de bluffer. Mon objectif est de fournir des conseils dignes d'un professionnel, optimisant les probabilités et les meilleures actions tout en prenant en compte le bluff du joueur et des adversaires ainsi que toutes les nuances stratégiques de la partie." }
            ]
        )

        reponse = completion.choices[0].message.content
        return reponse 

    def format_text(self, text):
        # Définir le texte formaté
        formatted_text = ""
        # Utiliser une expression régulière pour détecter le texte entre **texte**
        pattern = re.compile(r'\*\*(.*?)\*\*')
        # Trouver toutes les occurrences de texte entre **texte**
        matches = pattern.findall(text)
        # Remplacer les occurrences par du texte en gras
        for match in matches:
            text = text.replace(f"**{match}**", f"<b>{match}</b>")
        # Ajouter le texte formaté à la zone de texte
        self.text_edit.append(formatted_text)
            
    def w10joueurs5(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        sys.stdout = EmittingStream(self.textQuestion)
        
        self.progressBar.setValue(25)
        
        reponse = self.api_GPT(remplirJSON5joueursW10)
        #envoyerAGPT(nomPageChatGPT,remplirJSON5joueursW10)
        
        self.textReponse.insertPlainText(reponse)
        
        self.progressBar.setValue(100)
        
    def w10joueurs6(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        sys.stdout = EmittingStream(self.textQuestion)
        
        reponse = self.api_GPT(remplirJSON6joueursW10)
        #envoyerAGPT(nomPageChatGPT,remplirJSON6joueursW10)
        
        self.textReponse.insertPlainText(reponse)
        
    def w11joueurs5(self):
        screenshot(nomPage,screenshot_path)
        self.afficherImageUI()
        
        # reponse = self.api_GPT(remplirJSON5joueursW11)
        
        # self.textReponse.insertPlainText(reponse)
        
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
