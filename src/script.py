from numpy import var
#import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
from openai import OpenAI
import time
import re
import pyperclip
import numpy as np
import os
from ewmh import EWMH
from mss import mss
    
import pytesseract
from PIL import Image


nomPage = "Playground"
nomPage2="ChatGPT - Google Chrome"
screenshot_path = "../assets/capture.png"
screenshot_path2 = "../assets/capture2.png"
screenshot_cartes_path_flop="../matching/screens/flop"
screenshot_cartes_path_turn="../matching/screens/turn"
screenshot_cartes_path_river="../matching/screens/river"
screenshot_cartes_path_c="../matching/screens/c"
screenshot_cartes_path_back="../matching/screens/back"
path_base = '..//assets//'
regex = r'[^a-zA-Z0-9,:]'
regexBlindes =r'[^0-9,€-]'
nomPageChatGPT = "ChatGPT - Google Chrome"

baseImageFull = "../matching/card/full"
baseImageC = "../matching/card/c"
baseImageBack = "../matching/card/back"
baseImageFullChris = "../matching/card/full_chris"

varImageIncr = 1

#print(gw.getAllTitles())


ewmh = EWMH()

# Récupérer la liste des fenêtres actives
active_windows = ewmh.getClientList()

# Afficher les noms des fenêtres
window_titles = [ewmh.getWmName(window) for window in active_windows]
print(window_titles)



def preprocess_image(image):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou gaussien pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # Seuil adaptatif pour obtenir une image binaire
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Trouver les contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours sur un fond noir
    contour_image = cv2.drawContours(np.zeros_like(binary), contours, -1, (255), thickness=1)

    return contour_image

def get_dominant_color(image):
    # Convertir en RGB (OpenCV utilise BGR par défaut)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Redimensionner pour réduire le nombre de pixels
    resized_image = cv2.resize(image, (1, 1))

    # Obtenir la couleur dominante
    dominant_color = resized_image[0][0]

    # Déterminer la couleur principale
    if np.all(dominant_color < [50, 50, 50]):  # Noir si toutes les valeurs sont basses
        return 'S'  # Pique
    elif dominant_color[0] > dominant_color[1] and dominant_color[0] > dominant_color[2]:  # Rouge dominant
        return 'H'  # Coeur
    elif dominant_color[2] > dominant_color[0] and dominant_color[2] > dominant_color[1]:  # Bleu dominant
        return 'D'  # Carreau
    else:  # Vert ou autre
        return 'C'  # Trèfle
      
def matching(carte_path, baseImage, largeur_base=200, hauteur_base=500, method=cv2.TM_CCOEFF_NORMED):

    if baseImage == baseImageFull:
        largeur_base=16
        hauteur_base=25
    elif baseImage == baseImageC:
        largeur_base=20
        hauteur_base=40
    elif baseImage == baseImageBack:
        largeur_base=200
        hauteur_base=500

    if not os.path.exists(carte_path):
        print("Erreur : chemin de la carte non trouvé.")
        return None

    carte_capturee = cv2.imread(carte_path)
    if carte_capturee is None:
        print("Erreur : impossible de lire l'image de la carte.")
        return None
    
    couleur_dominante = get_dominant_color(carte_capturee)
    if baseImage == baseImageBack:
      couleur_dominante="B"
    
    carte_capturee = cv2.resize(carte_capturee, (largeur_base, hauteur_base))
    carte_capturee_preprocessed = preprocess_image(carte_capturee)

    meilleure_correspondance, meilleure_score = None, -1

    for image_nom in os.listdir(baseImage):
        if couleur_dominante in image_nom:  # Filtrer selon la couleur dominante:
            carte_base = cv2.imread(f"{baseImage}/{image_nom}")
            if carte_base is None:
                continue  # Ignorer les fichiers qui ne sont pas des images valides

            carte_base = cv2.resize(carte_base, (largeur_base, hauteur_base))
            carte_base_preprocessed = preprocess_image(carte_base)

            res = cv2.matchTemplate(carte_capturee_preprocessed, carte_base_preprocessed, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # Calcul du score en fonction de la méthode utilisée
            score = max_val if method not in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] else 1 - min_val
            seuil_correspondance = 0.5  # Augmentation du seuil pour une correspondance plus précise

            if score > seuil_correspondance and score > meilleure_score:
                meilleure_correspondance = image_nom
                meilleure_score = score

    nom_carte = meilleure_correspondance.split('.')[0] if meilleure_correspondance else "Aucune correspondance trouvée"
    print("La carte capturée est :", nom_carte)
    print("Score de correspondance :", meilleure_score)
    return nom_carte
  
def reconnaitreCartes(screenshot_cartes_path,baseImage, x1,y1,x2,y2,nomCrop="test"): 
  image = Image.open(screenshot_path)
  image_cropped_path=f"{screenshot_cartes_path}/{nomCrop}.png"
  cropped_image = image.crop((x1, y1, x2, y2))
  cropped_image.save(image_cropped_path)
  carte = matching(image_cropped_path,baseImage)
  return carte

def reconnaitreFlop():
  flop=[]
  flop1 = reconnaitreCartes(screenshot_cartes_path_flop,baseImageFullChris,566,368,566+99,368+153,"f1")
  flop2 = reconnaitreCartes(screenshot_cartes_path_flop,baseImageFullChris,678,368,678+99,368+153,"f2")
  flop3 = reconnaitreCartes(screenshot_cartes_path_flop,baseImageFullChris,790,368,790+99,368+153,"f3")
  flop.append(flop1)
  flop.append(flop2)
  flop.append(flop3)
  return flop

def reconnaitreTurn():
  turn = reconnaitreCartes(screenshot_cartes_path_turn,baseImageFullChris,898,368,898+101,368+153,"t")
  return turn 

def reconnaitreRiver():
  river = reconnaitreCartes(screenshot_cartes_path_river,baseImageFullChris,1010,368,1010+101,368+153,"r")
  return river

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

def screenshotLinux(nomPage, screenshot_path):
    ewmh = EWMH()
    
        # Récupérer la liste des fenêtres actives
    active_windows = ewmh.getClientList()

    for window in active_windows:
        window_name = ewmh.getWmName(window)
        if window_name and nomPage.lower() in window_name.lower():
            ewmh.setActiveWindow(window)
            
            # Mettre la fenêtre en plein écran (ou maximisée)
            ewmh.requestState(window, 1)  # 1 corresponds à l'état "Maximized"
            time.sleep(0.5)
            
            # Capturer l'écran
            with mss() as sct:
                screenshot = sct.shot(output=screenshot_path)

            print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
            
            # Minimiser la fenêtre
            ewmh.requestState(window, 2)  # 2 corresponds à l'état "Minimized"
            break
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
  image = Image.open(screenshot_path)

  cropped_image = image.crop((x1, y1, x2, y2))
  if nomCrop!="blindes":
    cropped_image = binarize_image(cropped_image)
  
  cropped_image.save(f"../assets/{nomCrop}.png")
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

def reconnaitrePotsWindows11_6():
  dicPots = {}
  pots= reconnaitreTexteCoordonees(screenshot_path,760,530,1009,602,"pots")
  #pots = re.sub(r'.*Po', 'Po', pots)
  pots = re.sub(regex, " ", pots)
  dicPots = {"Pots" : pots}
  return dicPots

def reconnaitrePotsWindows10_6():
  dicPots = {}
  pots= reconnaitreTexteCoordonees(screenshot_path,760,530,1009,602,"pots")
  #pots = re.sub(r'.*Po', 'Po', pots)
  pots = re.sub(regex, " ", pots)
  dicPots = {"Pots" : pots}
  return dicPots
  
# def reconnaitreMesDonneesWindows11_6():
#   p1c1=""
#   p1c2=""
#   dicP1 = {}
#   nomP1 =  reconnaitreTexteCoordonees(screenshot_path,774,764,1050,795,"nomP1")
#   miseActuelleP1 =  reconnaitreTexteCoordonees(screenshot_path,780,648,949,685,"miseActuelleP1")
#   stackP1 =  reconnaitreTexteCoordonees(screenshot_path,771,798,940,859,"stackP1")
  
#   p1c1 = reconnaitreCartes(screenshot_cartes_path_c,baseImageC,808,695,883,777,"p1c1") 
#   #p1c2 = reconnaitreCartes(screenshot_cartes_path_c,baseImageC,1,1,1,1,"p1c2") 
#   #reconnaitre status si il n'y a aucune carte 
  
#   nomP1 =  re.sub(regex, "", nomP1)
#   miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
#   stackP1 =  re.sub(regex, "", stackP1)
#   stackP1 =  re.sub("BB.*", "BB", stackP1)
  
#   dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
#   return dicP1

# def reconnaitreP2Windows11_6():
#   p2c1=""
#   p2c2=""
#   dicP2 = {}
#   nomP2 =  reconnaitreTexteCoordonees(screenshot_path,290,694,485,719,"nomP2")
#   miseActuelleP2 =  reconnaitreTexteCoordonees(screenshot_path,498,630,595,676,"miseActuelleP2")
#   stackP2 =  reconnaitreTexteCoordonees(screenshot_path,296,724,481,773,"stackP2")
  
#   # p2c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c1") 
#   # p2c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c2") 
#   #reconnaitre status si il n'y a aucune carte 
  
#   nomP2 =  re.sub(regex, "", nomP2)
#   miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
#   stackP2 =  re.sub(regex, "", stackP2)
  
#   dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":[p2c1,p2c2], "MiseActuelle": miseActuelleP2, "Statut": "En jeu"}
#   return dicP2


def reconnaitreActionPossibleWindows10():
  pass


def reconnaitreP2Windows10_6():
  p2c1=""
  p2c2=""
  dicP2 = {}
  nomP2 =  reconnaitreTexteCoordonees(screenshot_path,302,703,446,736,"nomP2")
  miseActuelleP2 =  reconnaitreTexteCoordonees(screenshot_path,465,640,603,677,"miseActuelleP2") # a faire plus tard !!!!!!!!!!!
  stackP2 =  reconnaitreTexteCoordonees(screenshot_path,285,735,496,794,"stackP2")
  
  # p2c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c1") 
  # p2c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP2 =  re.sub(regex, "", nomP2)
  miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
  stackP2 =  re.sub(regex, "", stackP2)
  
  dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":[p2c1,p2c2], "MiseActuelle": miseActuelleP2, "Statut": "En jeu"}
  return dicP2

def reconnaitreP3Windows10_6():
  p3c1=""
  p3c2=""
  dicP3 = {}
  nomP3 =  reconnaitreTexteCoordonees(screenshot_path,289,254,455,289,"nomP3")
  miseActuelleP3 =  reconnaitreTexteCoordonees(screenshot_path,443,359,603,395,"miseActuelleP3")
  stackP3 =  reconnaitreTexteCoordonees(screenshot_path,273,284,476,335,"stackP3")
  
  # p3c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p3c1") 
  # p3c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p3c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP3 =  re.sub(regex, "", nomP3)
  miseActuelleP3 =  re.sub(regex, "", miseActuelleP3)
  stackP3 =  re.sub(regex, "", stackP3)
  
  dicP3 = {"Nom" : nomP3, "Stack": stackP3, "Cartes":[p3c1,p3c2], "MiseActuelle": miseActuelleP3, "Statut": "En jeu"}
  return dicP3

def reconnaitreP4Windows10_6():
  p4c1=""
  p4c2=""
  dicP4 = {}
  nomP4 =  reconnaitreTexteCoordonees(screenshot_path,739,178,947,212,"nomP4")
  miseActuelleP4 =  reconnaitreTexteCoordonees(screenshot_path,760,333,940,368,"miseActuelleP4") # a faire plus tard !!!!!!!!!!!
  stackP4 =  reconnaitreTexteCoordonees(screenshot_path,737,210,984,263,"stackP4") 
  
  # p4c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p4c1") 
  # p4c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p4c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP4 =  re.sub(regex, "", nomP4)
  miseActuelleP4 =  re.sub(regex, "", miseActuelleP4)
  stackP4 =  re.sub(regex, "", stackP4)
  
  dicP4 = {"Nom" : nomP4, "Stack": stackP4, "Cartes":[p4c1,p4c2], "MiseActuelle": miseActuelleP4, "Statut": "En jeu"}
  return dicP4

def reconnaitreP5Windows10_6():
  p5c1=""
  p5c2=""
  dicP5 = {}
  nomP5 =  reconnaitreTexteCoordonees(screenshot_path,1203,256,1417,292,"nomP5")
  miseActuelleP5 =  reconnaitreTexteCoordonees(screenshot_path,1071,360,1230,400,"miseActuelleP5") # a faire plus tard !!!!!!!!!!!
  stackP5 =  reconnaitreTexteCoordonees(screenshot_path,1207,285,1404,340,"stackP5") 
  
  # p5c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p5c1") 
  # p5c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p5c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP5 =  re.sub(regex, "", nomP5)
  miseActuelleP5 =  re.sub(regex, "", miseActuelleP5)
  stackP5 =  re.sub(regex, "", stackP5)
  
  dicP5 = {"Nom" : nomP5, "Stack": stackP5, "Cartes":[p5c1,p5c2], "MiseActuelle": miseActuelleP5, "Statut": "En jeu"}
  return dicP5

def reconnaitreP6Windows10_6():
  p6c1=""
  p6c2=""
  dicP6 = {}
  nomP6 =  reconnaitreTexteCoordonees(screenshot_path,1198,703,1410,733,"nomP6")
  miseActuelleP6 =  reconnaitreTexteCoordonees(screenshot_path,1211,735,1420,792,"miseActuelleP6") # a faire plus tard !!!!!!!!!!!
  stackP6 =  reconnaitreTexteCoordonees(screenshot_path,1211,735,1420,792,"stackP6") 
  
  # p6c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p6c1") 
  # p6c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p6c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP6 =  re.sub(regex, "", nomP6)
  miseActuelleP6 =  re.sub(regex, "", miseActuelleP6)
  stackP6 =  re.sub(regex, "", stackP6)
  
  dicP6 = {"Nom" : nomP6, "Stack": stackP6, "Cartes":[p6c1,p6c2], "MiseActuelle": miseActuelleP6, "Statut": "En jeu"}
  return dicP6

def reconnaitreMesDonneesWindows10_6():
  p1c1 =""
  p1c2 =""
  dicP1 = {}
  nomP1 =  reconnaitreTexteCoordonees(screenshot_path,757,778,931,807,"nomP1")
  miseActuelleP1 =  reconnaitreTexteCoordonees(screenshot_path,763,660,949,695,"miseActuelleP1")
  stackP1 =  reconnaitreTexteCoordonees(screenshot_path,724,808,970,863,"stackP1")
  
  #p1c1 = reconnaitreCartes(screenshot_cartes_path_c,baseImageC,808,695,883,777,"p1c1")  
  p1c2 = reconnaitreCartes(screenshot_cartes_path_c,baseImageBack,808,695,883,777,"p1c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
  return dicP1


def reconnaitreActionPossibleWindows10():
  pass


def remplirJSON():
  Pots = reconnaitrePotsWindows10_6()
  p1 = reconnaitreMesDonneesWindows10_6()
  p2 = reconnaitreP2Windows10_6()
  p3 = reconnaitreP3Windows10_6()
  p4 = reconnaitreP4Windows10_6()
  p5 = reconnaitreP5Windows10_6()
  p6 = reconnaitreP6Windows10_6()
  flop = reconnaitreFlop()
  turn = reconnaitreTurn()
  river = reconnaitreRiver()
  
  finalRequest = {
    "Titre": "Nom de la Partie",
    "Joueurs": [
      {
        "Mon Nom": p1["Nom"],
        "Mon Stack": p1["Stack"], 
        "Mes Cartes": p1["Cartes"],
        "Ma MiseActuelle": p1["MiseActuelle"],
        "Mon Statut": p1["Statut"]
      },
      {
        "Nom": p2["Nom"],
        "Stack": p2["Stack"],
        "Cartes": p2["Cartes"],
        "MiseActuelle": p2["MiseActuelle"],
        "Statut": p2["Statut"]
      },
      {
        "Nom": p3["Nom"],
        "Stack": p3["Stack"],
        "Cartes": p3["Cartes"],
        "MiseActuelle": p3["MiseActuelle"],
        "Statut": p3["Statut"]
      },
      {
        "Nom": p4["Nom"],
        "Stack": p4["Stack"],
        "Cartes": p4["Cartes"],
        "MiseActuelle": p4["MiseActuelle"],
        "Statut": p4["Statut"]
      },
      {
        "Nom": p5["Nom"],
        "Stack": p5["Stack"],
        "Cartes": p5["Cartes"],
        "MiseActuelle": p5["MiseActuelle"],
        "Statut": p5["Statut"]
      }
    ],
    "MiseEnPlace": {
      "JeuDeCartes": "Jeu de 52 cartes",
      "TypeDePoker": "Texas Hold'em",
    },
    "ProchainJoueur": "Votre Nom",
    "PhaseEnCours": "Flop",
    "CartesCommunes": flop + turn + river,
    "Pot": Pots["Pots"]
  }
  
  return finalRequest


#screenshot(nomPage,screenshot_path)
screenshotLinux(nomPage,screenshot_path)
#afficherImage("capture.png")
#screenshot(nomPage2,screenshot_path2)

print(reconnaitrePotsWindows10_6())
print(reconnaitreMesDonneesWindows10_6())
print(reconnaitreP2Windows10_6())
print(reconnaitreP3Windows10_6())
print(reconnaitreP4Windows10_6())
print(reconnaitreP5Windows10_6())
print(reconnaitreP6Windows10_6())

print(reconnaitreFlop())
print(reconnaitreTurn())
print(reconnaitreRiver())


#reconnaitresDonneesAutres(screenshot_path)

#afficherImage("capture.png")
#afficherImage("capture2.png")


def envoyerAGPT():
  questionGPT = remplirJSON()
  fenetre = gw.getWindowsWithTitle(nomPageChatGPT)
  if len(fenetre) > 0:
    fenetre[0].maximize()
    fenetre[0].activate() 
    time.sleep(0.1)
    
   
    pyperclip.copy(str(questionGPT))
    pyautogui.click(x=804, y=983)  # Remplacez par les coordonnées du champ d'entrée
    pyautogui.hotkey('ctrl', 'v')  # Coller le contenu de questionGPT
    
    # Appuyer sur la touche Entrée
    pyautogui.press('enter')
    
    #fenetre[0].minimize()
  else:
    print(f"L'onglet '{nomPage}' n'a pas été trouvé. Réessai en cours...")
    
    
#envoyerAGPT()