import sys
import io
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QFont
import openai  # Assurez-vous d'importer la bibliothèque openai
from mesFonctions6JoueursW10 import *

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
        self.timer = QTimer(self)  # Créez un QTimer pour gérer le délai
        # self.progress_bar = None  # Initialisez la barre de progression à None

    def initUI(self):
        self.setWindowTitle('Poker Helper')
        self.adjustSizeAndPosition()

        # Bouton pour exécuter les fonctions
        self.button = QPushButton('Exécuter', self)
        self.button.setStyleSheet("QPushButton {background-color: #222255; color: white; font-size: 30px; border-radius: 20px}"
                                   "QPushButton:hover {background-color: #A52A2A;}")
        self.button.clicked.connect(self.execute_functions)

        # Zone de texte pour la question
        self.text_edit = QTextEdit(self)
        self.text_edit2 = QTextEdit(self)
        
            # Utilisez une couleur légèrement plus foncée que le fond global
        text_background_color = QtGui.QColor(30, 30, 30)
        
        self.text_edit.setStyleSheet(f"QTextEdit {{ background-color: {text_background_color.name()}; color:white; border-radius: 30px}}")
        self.text_edit2.setStyleSheet(f"QTextEdit {{ background-color: {text_background_color.name()}; color:white; border-radius: 30px }}")
        
        self.text_edit.setReadOnly(True)
        self.text_edit2.setReadOnly(True)
        font = QFont()
        font.setPointSize(14)  # Taille de la police pour QTextEdit
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
        
        # self.progress_bar = QProgressBar(self)
        # self.progress_bar.setValue(0)
        # main_layout.addWidget(self.progress_bar) 

        # Appliquer un thème sombre
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

        self.setPalette(dark_palette)
        self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white}")

        
        # self.progress_bar = QProgressBar(self)
        # self.progress_bar.setValue(0)
        # main_layout.addWidget(self.progress_bar)
        

    def adjustSizeAndPosition(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            window_width, window_height = 1300, 800
            self.setGeometry(geometry.x() + 400, geometry.y() + 100, window_width, window_height)
        else:
            self.setGeometry(100, 100, 1300, 900)

    @pyqtSlot()
    def execute_functions(self):
        self.text_edit.clear()
        self.text_edit2.clear()

        # Créez la barre de progression ici
        self.progress_bar = QProgressBar(self)
        self.layout().addWidget(self.progress_bar)
        self.progress_bar.setValue(0)  # Ajoutez-la au layout
        self.progress_bar.setStyleSheet(f"QProgressBar{{border-radius: 3px}}")
        
        screenshot(nomPage,screenshot_path)
        self.button.setStyleSheet("QPushButton {background-color: green; font-size: 30px; border-radius: 20px;}"
                                   "QPushButton:hover {background-color: #A52A2A;color: white; font-size: 30px; border-radius: 20px;}")

        # Utilisez QTimer pour appeler remplirJSON de manière asynchrone
        self.timer.singleShot(10, self.api_GPT)

    def remplirJSON(self):
        # Redirigez les sorties print vers la zone de texte
        sys.stdout = EmittingStream(self.text_edit)

        pots, p1, p2, p3, p4, p5, p6 = parallel_recognize_players_data()

        # Effectuez les opérations nécessaires dans remplirJSON()
        print(f""" Joueurs:
            - My Name: {p1["Nom"]}
                Ma bankroll: {p1["Stack"]}
                My Cards: {p1["Cartes"]}
                My State: {p1["Statut"]}
            - name player2: {p2["Nom"]}
                bankroll: {p2["Stack"]}
                actual bet: {p2["MiseActuelle"]}
                State: {p2["Statut"]}
            - name player3: {p3["Nom"]}
                bankroll: {p3["Stack"]}
                actual bet: {p3["MiseActuelle"]}
                State: {p3["Statut"]}
            - name player4: {p4["Nom"]}
                bankroll: {p4["Stack"]}
                actual bet: {p4["MiseActuelle"]}
                State: {p4["Statut"]}
            - name player5: {p5["Nom"]}
                bankroll: {p5["Stack"]}
                actual bet: {p5["MiseActuelle"]}
                State: {p5["Statut"]}
            - name player5: {p6["Nom"]}
                bankroll: {p6["Stack"]}
                actual bet: {p6["MiseActuelle"]}
                State: {p6["Statut"]}""") 
        self.progress_bar.setValue(30)
        flop, turn, river = recognize_all_board_cards()
        
        print(f"""Pot: {pots["Pots"]}
            Community Cards: flop: {flop} turn: {turn} river: {river}""")
        self.progress_bar.setValue(40)
        
        actionsPossible = reconnaitreActionsPossible()
        print(f"""Moves I can do: {actionsPossible}
            Money I can bet: 2.225BB, 2.5BB, 2.75BB, 3BB, 3.5BB, 4BB""")
        self.progress_bar.setValue(50)

        finalRequest = f"""
            Joueurs:
            - My Name: {p1["Nom"]}
                My bankroll: {p1["Stack"]}
                My Cards: {p1["Cartes"]}
                My State: {p1["Statut"]}

            - name player2: {p2["Nom"]}
                bankroll: {p2["Stack"]}
                actual bet: {p2["MiseActuelle"]}
                State: {p2["Statut"]}

            - name player3: {p3["Nom"]}
                bankroll: {p3["Stack"]}
                actual bet: {p3["MiseActuelle"]}
                State: {p3["Statut"]}

            - name player4: {p4["Nom"]}
                bankroll: {p4["Stack"]}
                actual bet: {p4["MiseActuelle"]}
                State: {p4["Statut"]}

            - name player5: {p5["Nom"]}
                bankroll: {p5["Stack"]}
                actual bet: {p5["MiseActuelle"]}
                State: {p5["Statut"]}

            - name player5: {p6["Nom"]}
                bankroll: {p6["Stack"]}
                actual bet: {p6["MiseActuelle"]}
                State: {p6["Statut"]}
            Pot: {pots["Pots"]}
            Community Cards: flop: {flop} turn: {turn} river: {river}
            Moves I can do: {actionsPossible}
            Money I can bet: 2.225BB, 2.5BB, 2.75BB, 3BB, 3.5BB, 4BB
        """

        # Mettez à jour la barre de progression
        

        # Réinitialisez la couleur du bouton
        self.reset_button_color()

        return finalRequest

    def api_GPT(self):
        questionGPT = self.remplirJSON()

        client = openai.OpenAI(api_key="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")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional poker player, skilled in analyzing and calculating the perfect move to make every time it's your turn."},
                {"role": "user", "content": "Give me the move to do in BOLD and a small explanation for this poker configuration : " + questionGPT}
            ]
        )

        reponse = completion.choices[0].message.content

        # Réinitialisez la couleur du bouton après un autre délai de 2 secondes
        self.timer.singleShot(10, self.reset_button_color)
        self.text_edit2.insertPlainText(reponse)
        self.progress_bar.setValue(100)
        self.timer.singleShot(2000, self.reset_progress_bar)
        
    def reset_progress_bar(self):
        self.layout().removeWidget(self.progress_bar)  
        self.progress_bar.deleteLater()
        self.update()  

    # Fonction pour réinitialiser la couleur du bouton
    def reset_button_color(self):
        self.button.setStyleSheet("QPushButton {background-color: #222255; color: white; font-size: 30px; border-radius: 20px;}"
                                   "QPushButton:hover {background-color: #A52A2A; color: white; font-size: 30px; border-radius: 20px;}")



# Exécution de l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PokerHelperApp()
    ex.show()
    sys.exit(app.exec_())
