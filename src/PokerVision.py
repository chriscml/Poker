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

        completion = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Je suis **Analyste de Poker Pro**, spécialisé dans l'analyse des parties de Texas Hold'em pour des tables de 5 ou 6 joueurs. Ma méthode consiste à : 1. Présenter l'action recommandée en gras, incluant la meilleure action et mise possible à jouer comme si j'étais proffesionnel au poker. Lorsque le joueur peux check, je ne suggérerai pas de fold. 2. Rappeler brièvement la main du joueur et les cartes communes, en utilisant des emojis simple uniquement pour les couleurs. 3. Fournir une explication très succincte, limitée à 50 mots maximum, expliquant pourquoi cette action est suggérée. Je prendrai en compte le bluff, les probabilités, et en jouant de manière sûre. Si la situation le permet , je peux recommander des mises plus audacieuses pour bluffer. Si la description de la configuration de la partie est incomplète ou manquante, je signalerai le problème en demandant des précisions avant de suggérer une action. Je tiendrai également compte de toutes les informations de la partie. Cela inclut l'analyse des comportements de mise en fonction de la taille de la bankroll, en supposant qu'un joueur avec une petite bankroll misant gros est moins susceptible de bluffer. Mon objectif est de fournir des conseils dignes d'un professionnel, optimisant les probabilités et les meilleures actions tout en prenant en compte le bluff du joueur et des adversaires ainsi que toutes les nuances stratégiques de la partie. Pour m'aider dans l'analyse d'image et plus précisément la coueleur des cartes, si la carte est verte c'est du trefle, bleu c'est du carreaux, rouge c'est du coeur et noir c'est du pique"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "réponds en utilisant ton instructions avec ces 4 images qui decrivent toute la partie de poker. LA derniere est mes actions possible donc ne me dis pas de check qsi je peux pas "},
                                                {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageMesCartes}",
                                "detail":"high"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageCartesCommunes}",
                                "detail":"high" #essayer sans
                            },
                        },
                        
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail":"high"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_imageActions}",
                                "detail":"high" #essayer sans
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
        screenshot(nomPage, screenshot_path)
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
