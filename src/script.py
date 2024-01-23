from numpy import var
import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
from openai import OpenAI
import time
import re
    
import pytesseract
from PIL import Image

nomPage = "Playground"
nomPage2="Gestionnaire des tâches"
screenshot_path = "../assets/capture.png"
screenshot_path2 = "../assets/capture2.png"
path_base = '..//assets//'
regex = r'[^a-zA-Z0-9,:]'
regexBlindes =r'[^0-9,€-]'

varImageIncr = 0

#print(gw.getAllTitles())

def screenshot(nomPage, screenshot_path):
      fenetre = gw.getWindowsWithTitle(nomPage)
      if len(fenetre) > 0:
        left, top, width, height = fenetre[0].left, fenetre[0].top, fenetre[0].width, fenetre[0].height
        fenetre[0].activate() 
          # Mettre la fenêtre en plein écran (ou maximisée)
        fenetre[0].maximize()
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
        # Minimiser la fenêtre
        fenetre[0].minimize()
      else:
        print(f"L'onglet '{nomPage}' n'a pas été trouvé. Réessai en cours...")


      

def afficherImage(imageName, titre=""):
    plt.figure()
    image = cv2.imread(path_base + imageName)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertir de BGR (format OpenCV) à RGB
    plt.imshow(image_rgb)
    plt.title(titre)
    plt.show()
    
def binarize_image(image, threshold=128):
    # Convertir l'image en niveaux de gris
    image = image.convert("L")

    # Binariser l'image en utilisant un seuil
    image = image.point(lambda p: p > threshold and 255)

    return image

def reconnaitreTexteCoordonees(screenshot_path, x1,y1,x2,y2,nomCrop="test"):
  global varImageIncr 
  
  image = Image.open(screenshot_path)

  cropped_image = image.crop((x1, y1, x2, y2))
  if nomCrop!="blindes":
    cropped_image = binarize_image(cropped_image)
  
  cropped_image.save(f"../assets/{nomCrop}.png")
  varImageIncr=varImageIncr+1
  text = pytesseract.image_to_string(cropped_image)
  return text.replace("\n"," ").strip()

def reconnaitreBlindesCashGame():
  dicBlindes = {}
  blindes= reconnaitreTexteCoordonees(screenshot_path,119,23,405,58,"blindes")
  blindes = re.sub(regexBlindes, "", blindes)
  blindes = re.sub(r'€.*', '€', blindes)
  dicBlindes = {"Blindes" :blindes}
  return dicBlindes


def reconnaitreBlindesTournoi():
  dicBlindes = {}
  blindes= reconnaitreTexteCoordonees(screenshot_path,119,23,405,58,"blindes")
  blindes = re.sub(regexBlindes, "", blindes)
  blindes = re.sub(r'€.*', '€', blindes)
  dicBlindes = {"Blindes" :blindes}
  return dicBlindes

def reconnaitrePots():
  dicPots = {}
  pots= reconnaitreTexteCoordonees(screenshot_path,760,530,1009,602,"pots")
  #pots = re.sub(r'.*Po', 'Po', pots)
  pots = re.sub(regex, " ", pots)
  dicPots = {"Pots" : pots}
  return dicPots
  
def reconnaitreMesDonnees():
  dicP1 = {}
  nomP1 =  reconnaitreTexteCoordonees(screenshot_path,774,764,1050,795,"nomP1")
  miseActuelleP1 =  reconnaitreTexteCoordonees(screenshot_path,780,648,949,685,"miseActuelleP1")
  stackP1 =  reconnaitreTexteCoordonees(screenshot_path,771,798,940,859,"stackP1")
  #reconnaitre cartes 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":["",""], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
  return dicP1

def reconnaitreP2():
  dicP2 = {}
  nomP2 =  reconnaitreTexteCoordonees(screenshot_path,290,694,485,719,"nomP2")
  miseActuelleP2 =  reconnaitreTexteCoordonees(screenshot_path,498,630,595,676,"miseActuelleP2")
  stackP2 =  reconnaitreTexteCoordonees(screenshot_path,296,724,481,773,"stackP2")
  #reconnaitre cartes 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP2 =  re.sub(regex, "", nomP2)
  miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
  stackP2 =  re.sub(regex, "", stackP2)
  
  dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":["",""], "MiseActuelle": miseActuelleP2, "Statut": "En jeu"}
  return dicP2


#screenshot(nomPage,screenshot_path)

print(reconnaitrePots())
print(reconnaitreMesDonnees())
print(reconnaitreP2())

#reconnaitresDonneesAutres(screenshot_path)

#afficherImage("capture.png")
    






def remplirJSON():
  requestFINALE : {
    "Titre": "Nom de la Partie",
    "Joueurs": [
      {
        "Nom": "Joueur 1",
        "Stack": 40, 
        "Cartes": ["", ""],
        "MiseActuelle": 0,
        "Statut": "En jeu"
      },
      {
        "Nom": "Joueur 2",
        "Stack": 60,
        "Cartes": ["", ""],
        "MiseActuelle": 0,
        "Statut": "En jeu"
      },
      {
        "Nom": "Joueur 3",
        "Stack": 30,
        "Cartes": [],
        "MiseActuelle": 0,
        "Statut": "Se couche"
      },
      {
        "Nom": "Joueur 4",
        "Stack": 50,
        "Cartes": ["", ""],
        "MiseActuelle": 0,
        "Statut": "En jeu"
      },
      {
        "Nom": "Votre Nom",
        "Stack": 37.5,
        "Cartes": ["Dame de cœur", "Roi de carreau"],
        "MiseActuelle": 0,
        "Statut": "À jouer"
      }
    ],
    "MiseEnPlace": {
      "JeuDeCartes": "Jeu de 52 cartes",
      "TypeDePoker": "Texas Hold'em",
      "NiveauBlindes": "Petites blindes 10, grandes blindes 20"
    },
    "ProchainJoueur": "Votre Nom",
    "PhaseEnCours": "Flop",
    "CartesCommunes": ["As de pique", "Dix de pique", "Quatre de cœur"],
    "PotTotal": 250,
    "MiseCourante": 20
  }