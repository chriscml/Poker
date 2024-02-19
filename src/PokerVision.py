import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
import base64
import openai
from utility import *

class APITaskSignals(QObject):
    finished = pyqtSignal(str)

class APITask(QRunnable):
    def __init__(self, image_path="../assets/capture.png"):
        super().__init__()
        self.image_path = image_path
        self.signals = APITaskSignals()

    def run(self):
        response = self.api_GPT()
        self.signals.finished.emit(response)

    def api_GPT(self):
        with open(self.image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        with open("../assets/mescartes.png", "rb") as image_file:
            base64_imageMesCartes = base64.b64encode(image_file.read()).decode('utf-8')
        
        with open("../assets/cartescommunes.png", "rb") as image_file:
            base64_imageCartesCommunes = base64.b64encode(image_file.read()).decode('utf-8')
        
        with open("../assets/actionspossibles.png", "rb") as image_file:
            base64_imageActions = base64.b64encode(image_file.read()).decode('utf-8')
        
        
        client = openai.OpenAI(api_key="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")
        
        instruction= """
            Je suis As du Poker, un expert en analyse de poker, conçu pour jouer avec la précision du joueur le plus intelligent du monde. Je base mes conseils sur les meilleures probabilités, en analysant minutieusement chaque aspect de la partie : vos cartes, les cartes communes, la dynamique de jeu, et les actions possibles. Mon objectif est de fournir l'action optimale en toute situation, en mettant l'accent sur des stratégies gagnantes à long terme. Je respecte le format de réponse spécifié, en rappelant vos cartes et les cartes communes avec des emojis uniquement pour la couleur, et je fournis une explication concise pour chaque conseil donné.

            1) **ACTION A JOUER + MISE SI BESOIN, EN GRAS**

            2) mes cartes : rappel de vos cartes avec des emojis pour la couleur.

            3) rappel des cartes communes de la même manière.

            4) courte explication de maximum 50 mots de l'action conseillée. 
        """
        
        instruction2 = """Je suis **Analyste de Poker Pro**, spécialisé dans l'analyse des parties de Texas Hold'em pour des tables de 5 ou 6 joueurs. Ma méthode consiste à : 1. Présenter l'action recommandée en gras, incluant la meilleure action et mise possible à jouer comme si j'étais proffesionnel au poker. Lorsque le joueur peux check, je ne suggérerai pas de FOLD. 2. Rappeler brièvement la main du joueur et les cartes communes, en utilisant des emojis simple uniquement pour les couleurs. 3. Fournir une explication très succincte, limitée à 50 mots maximum, expliquant pourquoi cette action est suggérée. Je prendrai en compte le bluff, les probabilités, et en jouant de manière sûre. Si la situation le permet , je peux recommander des mises plus audacieuses pour bluffer. Si la description de la configuration de la partie est incomplète ou manquante, je signalerai le problème en demandant des précisions avant de suggérer une action. Je tiendrai également compte de toutes les informations de la partie. Cela inclut l'analyse des comportements de mise en fonction de la taille de la bankroll, en supposant qu'un joueur avec une petite bankroll misant gros est moins susceptible de bluffer. Mon objectif est de fournir des conseils dignes d'un professionnel, optimisant les probabilités et les meilleures actions tout en prenant en compte le bluff du joueur et des adversaires ainsi que toutes les nuances stratégiques de la partie. Pour m'aider dans l'analyse d'image et plus précisément la coueleur des cartes, si la carte est verte c'est du trefle, bleu c'est du carreaux, rouge c'est du coeur et noir c'est du pique"""

        completion = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": instruction2},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "ne me dis pas de check si je ne peux pas check. Analyse les images suivante : mes cartes, les cartes communes, le jeu complet, mes actions possible. Si tu vois des cartes de dos au dessus du nom des joueurs c'est qu'ils sont couché "},
                                                {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageMesCartes}",
                                "detail":"high",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageCartesCommunes}",
                                "detail":"high",
                            },
                        },
                        
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail":"high",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageActions}",
                                "detail":"high",
                            },
                        },

                    ],
                }
            ],
            max_tokens=1000,
        )

        response = completion.choices[0].message.content
        return response

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My App')
        self.adjustSizeAndPosition()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("color: white; font-size: 18pt; background-color: #303030; border: 2px solid #555555; border-radius: 10px;")

        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)

        self.button = QPushButton('Exécuter')
        self.button.setStyleSheet("QPushButton { color: white; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 10px; font-size: 20px; }"
                                   "QPushButton:hover { background-color: #45a049; }")
        self.button.clicked.connect(self.execute_script)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label_image)
        layout.addWidget(self.text_edit)
        
        self.setLayout(layout)

    def execute_script(self):
        self.text_edit.clear() 
        screenshot_vision(nomPage, screenshot_path)
        self.afficherImageUI(screenshot_path)
        
        if len(self.screens) > 1:
            pass
        else:
            ecranJoli(nomPageProgramme, nomPage)

        self.threadpool = QThreadPool()
        task = APITask(image_path=screenshot_path)
        task.signals.finished.connect(self.on_api_finished)
        self.threadpool.start(task)

    def on_api_finished(self, response):
        self.text_edit.append(response)

    def adjustSizeAndPosition(self):
        self.screens = QApplication.screens()
        if len(self.screens) > 1:
            second_screen = self.screens[1]
            geometry = second_screen.geometry()
            window_width, window_height = 1800, 900
            self.setGeometry(geometry.x() + 25, geometry.y() + 100, window_width, window_height)
        else:
            self.setGeometry(25, 25, 1700, 900)

    def afficherImageUI(self, image_path):
        pixmap = QPixmap(image_path).scaled(700, 700, Qt.KeepAspectRatio)
        self.label_image.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #212121; color: white; }")
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
