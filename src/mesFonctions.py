from numpy import var
import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
from openai import OpenAI
import time
import re
import pyperclip
import numpy as np
import os
from PIL import Image

import io
from PIL import Image
import win32clipboard
from io import BytesIO

from pywinauto.application import Application
import pyautogui
    
import pytesseract

from pywinauto import Desktop

from concurrent.futures import ThreadPoolExecutor

from sklearn.cluster import KMeans

import gc 

nomPage = "Playground"

screenshot_path = "../assets/capture.png"
screenshot_pathGPT = "../assets/capture2.png"


screenshot_cartes_path_flop="../matching/screens/flop"
screenshot_cartes_path_turn="../matching/screens/turn"
screenshot_cartes_path_river="../matching/screens/river"
screenshot_cartes_path_c="../matching/screens/c"
screenshot_cartes_path_back="../matching/screens/back"

path_base = '..//assets//'
regex = r'[^a-zA-Z0-9,:]'
regexBlindes =r'[^0-9,€-]'

nomPageBard = "Bard - Google Chrome"
nomPageConseilDePokerEnDirect ="Conseils de Poker en Direct - Google Chrome"
nomPageVSCODE = "script.py - poker - Visual Studio Code"

baseImageBack = "../matching/card/back"
baseImageVide = "../matching/card/vide"


#print(gw.getAllTitles())

def get_hwnd(title):
    windows = Desktop(backend="uia").windows()
    for w in windows:
        if title in w.window_text():
            return w.handle
    return None

# Utilisez le titre de la fenêtre que vous cherchez
hwnd = get_hwnd("Conseils de poker en direct - Google Chrome")

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold instead of adaptive threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optional: Apply morphological operations here if there's noise

    # Scaling the image to improve recognition
    scale_percent = 150  # percent of original size
    width = int(binary.shape[1] * scale_percent / 100)
    height = int(binary.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(binary, dim, interpolation=cv2.INTER_AREA)

    return resized

def matchingBack(carte_path, largeur_base=200, hauteur_base=500, method=cv2.TM_CCOEFF_NORMED):
    if not os.path.exists(carte_path):
        print("Erreur : chemin de la carte non trouvé.")
        return None

    carte_capturee = cv2.imread(carte_path)
    if carte_capturee is None:
        print("Erreur : impossible de lire l'image de la carte.")
        return None
    

    carte_capturee = cv2.resize(carte_capturee, (largeur_base, hauteur_base))
    carte_capturee_preprocessed = preprocess_image(carte_capturee)

    meilleure_correspondance, meilleure_score = None, -1

    for image_nom in os.listdir(baseImageBack):
        carte_base = cv2.imread(f"{baseImageBack}/{image_nom}")
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

    nom_carte = meilleure_correspondance.split('.')[0] if meilleure_correspondance else "couché"
    #print("La carte capturée est :", nom_carte)
    return nom_carte
  
def matchingVide(carte_path, largeur_base=200, hauteur_base=500, method=cv2.TM_CCOEFF_NORMED):
    if not os.path.exists(carte_path):
        print("Erreur : chemin de la carte non trouvé.")
        return None

    carte_capturee = cv2.imread(carte_path)
    if carte_capturee is None:
        print("Erreur : impossible de lire l'image de la carte.")
        return None
    

    carte_capturee = cv2.resize(carte_capturee, (largeur_base, hauteur_base))
    carte_capturee_preprocessed = preprocess_image(carte_capturee)

    meilleure_correspondance, meilleure_score = None, -1

    for image_nom in os.listdir(baseImageVide):
        carte_base = cv2.imread(f"{baseImageVide}/{image_nom}")
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

    nom_carte = 'pas de carte' if meilleure_correspondance else "une carte"
    #print("La carte capturée est :", nom_carte)
    return nom_carte

def get_dominant_color(image, k=4):
    # Convert to RGB if it's not already
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to be a list of pixels
    pixels = image.reshape(-1, 3)

    # Use KMeans clustering to cluster the pixel intensities
    clt = KMeans(n_clusters=k)
    clt.fit(pixels)

    # Count the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # Normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # Sort the clusters according to the number of pixels in each cluster
    sorted_clusters = sorted(zip(hist, clt.cluster_centers_), key=lambda x: x[0], reverse=True)

    # The color of the largest cluster is the dominant color
    dominant_color = sorted_clusters[0][1].astype("int")

    # Define color ranges
    if np.all(dominant_color < [50, 50, 50]):  # Black if all values are low
        return ' de pique '  # Spades
    elif dominant_color[0] > dominant_color[1] and dominant_color[0] > dominant_color[2]:  # Red dominant
        return ' de coeur '  # Hearts
    elif dominant_color[2] > dominant_color[0] and dominant_color[2] > dominant_color[1]:  # Blue dominant
        return ' de carreaux'  # Diamonds
    elif dominant_color[1] > dominant_color[0] and dominant_color[1] > dominant_color[2]:  # Green dominant
        return ' de trefle'  # Clubs
    else:
        return "pas encore de carte"
      
def reconnaitreBB(screenshot_path, x1, y1, x2, y2, nomCrop="test"):
    image = Image.open(screenshot_path)

    cropped_image = image.crop((x1, y1, x2, y2))
    
    # Save the cropped image for debugging
    cropped_image.save(f"../assets/{nomCrop}.png")
    
    # Read the saved image using OpenCV
    cropped_image_cv = cv2.imread(f"../assets/{nomCrop}.png")
    
    # Preprocess the image for better OCR
    preprocessed_image = preprocess_image(cropped_image_cv)
    
    # Configure tesseract to recognize numbers, comma, and 'B'
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,BbALL-IN'
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    
    return text.replace("\n"," ").strip()
  

  
def reconnaitreTxt(screenshot_path, x1, y1, x2, y2, nomCrop="pseudo"):
    image = Image.open(screenshot_path)

    cropped_image = image.crop((x1, y1, x2, y2))
    
    # Save the cropped image for debugging
    cropped_image.save(f"../assets/{nomCrop}.png")
    
    # Read the saved image using OpenCV
    cropped_image_cv = cv2.imread(f"../assets/{nomCrop}.png")
    
    # Preprocess the image for better OCR
    preprocessed_image = preprocess_image(cropped_image_cv)
    
    # Configure tesseract to recognize a broad set of characters
    # Since usernames can be more complex, we're not using a whitelist here
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    
    return text.replace("\n"," ").strip()



def reconnaitreCartes(screenshot_cartes_path, x1, y1, x2, y2, nomCrop="test"):
    nomCarte = ""
  
    image = Image.open(screenshot_path)
    image_cropped_path = f"{screenshot_cartes_path}/{nomCrop}.png"
  
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image.save(image_cropped_path)
  
    cropped_image = cv2.imread(image_cropped_path)
    couleur_dominante = get_dominant_color(cropped_image)
    
    if couleur_dominante == 'pas encore de carte':
      return 'pas encore de carte'
  
    # Preprocess the image for better OCR
    preprocessed_image = preprocess_image(cropped_image)
    
    # Configure tesseract to do single character recognition
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789AJQK10Q9qajk'
    text = pytesseract.image_to_string(cropped_image, config=custom_config)
    
    if text.strip() == "1" or text.strip() == "11":
      text = "7"
      
    for caractere in text:
        if caractere.isalpha() or caractere.isdigit():
            text = caractere
            break
    
  
    nomCarte = text.strip() + couleur_dominante
    
    if text == "":
       nomCarte="pas de carte"
      
    return nomCarte

def reconnaitreFlop():
  flop=[]
  flop1 = reconnaitreCartes(screenshot_cartes_path_flop,566,368,566+99,368+45,"f1")
  f1 = matchingVide(f"{screenshot_cartes_path_flop}/f1.png")
  if f1 == "pas de carte":
    flop1 = f1
  
  flop2 = reconnaitreCartes(screenshot_cartes_path_flop,678,368,678+99,368+45,"f2")
  f2 = matchingVide(f"{screenshot_cartes_path_flop}/f2.png")
  if f2 == "pas de carte":
    flop2 = f2
  
  flop3 = reconnaitreCartes(screenshot_cartes_path_flop,790,368,790+99,368+45,"f3")
  f3 = matchingVide(f"{screenshot_cartes_path_flop}/f3.png")
  if f3 == "pas de carte":
    flop3 = f3
    
  flop.append(flop1)
  flop.append(flop2)
  flop.append(flop3)
  return flop

def reconnaitreTurn():
  turn = reconnaitreCartes(screenshot_cartes_path_turn,898,368,898+101,368+45,"t")
  t = matchingVide(f"{screenshot_cartes_path_turn}/t.png")
  if t == "pas de carte":
    turn = t
  return turn.strip()

def reconnaitreRiver():
  river = reconnaitreCartes(screenshot_cartes_path_river,1010,368,1010+101,368+45,"r")
  r = matchingVide(f"{screenshot_cartes_path_river}/r.png")
  if r == "pas de carte":
    river = r
  return river.strip()

def recognize_all_board_cards():
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_flop = executor.submit(reconnaitreFlop)
        future_turn = executor.submit(reconnaitreTurn)
        future_river = executor.submit(reconnaitreRiver)

        flop = future_flop.result()
        turn = future_turn.result()
        river = future_river.result()

    return flop, turn.strip(), river.strip()

def minimiserVSCode(nomPage):
  # Recherche de la fenêtre "Playground" par son titre
  fenetre = gw.getWindowsWithTitle(nomPage)
  if fenetre:
      fenetre = fenetre[0]
      fenetre.restore()
      time.sleep(0.2)
      fenetre.minimize()
  else:
      print(f"L'onglet '{nomPage}' n'a pas été trouvé.")
    
  gc.collect()


def screenshot(nomPage, screenshot_path):
  #minimiserVSCode(nomPageVSCODE)
  try:
      # Recherche de la fenêtre "Playground" par son titre
      fenetre = gw.getWindowsWithTitle(nomPage)
      if fenetre:
          fenetre = fenetre[0]
          fenetre.maximize()
          
          #left, top, width, height = fenetre.left, fenetre.top, fenetre.width, fenetre.height
          time.sleep(0.4)
          screenshot = pyautogui.screenshot() #region=(left, top, width+2, height+2) +2 pour windows 11 1938 1058
          screenshot.save(screenshot_path)
          print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
          # Minimise la fenêtre
          fenetre.minimize()
      else:
          print(f"L'onglet '{nomPage}' n'a pas été trouvé.")

  except Exception as e:
      print(f"Erreur lors de la capture d'écran : {e}") 
    
  gc.collect()

        
def screenshotWin(nomPage, screenshot_path):
    titre_page = ".*{}.*".format(nomPage)
    try:
        app = Application(backend="uia").connect(title_re=".*Playground.*", visible_only= False)
        fenetre = app.top_window()
        fenetre.set_focus()
        fenetre.maximize()
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
        fenetre.minimize()
        del screenshot
        del fenetre
        del app
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")
    
    gc.collect()


      

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





# def reconnaitreBlindesCashGame():
#   dicBlindes = {}
#   blindes= reconnaitreTexteCoordonees(screenshot_path,119,23,405,58,"blindes")
#   blindes = re.sub(regexBlindes, "", blindes)
#   blindes = re.sub(r'€.*', '€', blindes)
#   dicBlindes = {"Blindes" :blindes}
#   return dicBlindes


def reconnaitreBlindesTournoi():
  dicBlindes = {}
  blindes= reconnaitreTxt(screenshot_path,119,23,405,58,"blindes")
  blindes = re.sub(regexBlindes, "", blindes)
  blindes = re.sub(r'€.*', '€', blindes)
  dicBlindes = {"Blindes" :blindes}
  return dicBlindes

# def reconnaitrePotsWindows11_6():
#   dicPots = {}
#   pots= reconnaitreTxt(screenshot_path,760,530,1009,602,"pots")
#   #pots = re.sub(r'.*Po', 'Po', pots)
#   pots = re.sub(regex, " ", pots)
#   dicPots = {"Pots" : pots}
#   return dicPots

def reconnaitrePotsWindows10_6():
    dicPots = {}
    pots = reconnaitreTxt(screenshot_path, 760, 530, 1009, 602, "pots")
    
    # Use regular expression to remove everything before the first occurrence of 'Pot'
    pots_cleaned = re.sub(r'^.*?Pot', 'Pot', pots)
    
    dicPots = {"Pots": pots_cleaned}
    return dicPots

  

def reconnaitreActionPossibleWindows10():
  pass


def reconnaitreP2Windows10_6():
  dicP2 = {}
  nomP2 =  reconnaitreTxt(screenshot_path,302,703,446,736,"nomP2")
  miseActuelleP2 =  reconnaitreBB(screenshot_path,465,640,603,677,"miseActuelleP2") # a faire plus tard !!!!!!!!!!!
  stackP2 =  reconnaitreBB(screenshot_path,296,735,296+210,735+55,"stackP2")

  reconnaitreCartes(screenshot_cartes_path_back,345,624,345+45+75,624+45,"b2") 
  b2 = matchingBack(f"{screenshot_cartes_path_back}/b2.png")
   
  if b2=="couché":
    Statut="couché"
  else:
    Statut = "En jeu"
    
  
  nomP2 =  re.sub(regex, "", nomP2)
  miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
  stackP2 =  re.sub(regex, "", stackP2)
  stackP2 =  re.sub("BB.*", "BB", stackP2)
  
  
  dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP2, "Statut": Statut}
  return dicP2

def reconnaitreP3Windows10_6():
  dicP3 = {}
  nomP3 =  reconnaitreTxt(screenshot_path,289,254,455,289,"nomP3")
  miseActuelleP3 =  reconnaitreBB(screenshot_path,443,359,603,395,"miseActuelleP3")
  stackP3 =  reconnaitreBB(screenshot_path,273,284,476,335,"stackP3")
  
  reconnaitreCartes(screenshot_cartes_path_back,303,171,302+45+75,171+45,"b3") 
  b3 = matchingBack(f"{screenshot_cartes_path_back}/b3.png")
   
  if b3=="couché":
    Statut="couché"
  else:
    Statut = "En jeu"
  
  nomP3 =  re.sub(regex, "", nomP3)
  miseActuelleP3 =  re.sub(regex, "", miseActuelleP3)
  stackP3 =  re.sub(regex, "", stackP3)
  stackP3 =  re.sub("BB.*", "BB", stackP3)
  
  
  dicP3 = {"Nom" : nomP3, "Stack": stackP3, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP3, "Statut": Statut}
  return dicP3

def reconnaitreP4Windows10_6():
  dicP4 = {}
  nomP4 =  reconnaitreTxt(screenshot_path,739,178,947,212,"nomP4")
  miseActuelleP4 =  reconnaitreBB(screenshot_path,760,333,940,368,"miseActuelleP4") # a faire plus tard !!!!!!!!!!!
  stackP4 =  reconnaitreBB(screenshot_path,737,210,984,263,"stackP4") 
  
  reconnaitreCartes(screenshot_cartes_path_back,768,96,768+45+75,96+45,"b4") 
  b4 = matchingBack(f"{screenshot_cartes_path_back}/b4.png")
   
  if b4=="couché":
    Statut="couché"
  else:
    Statut = "En jeu"
  
  nomP4 =  re.sub(regex, "", nomP4)
  miseActuelleP4 =  re.sub(regex, "", miseActuelleP4)
  stackP4 =  re.sub(regex, "", stackP4)
  stackP4 =  re.sub("BB.*", "BB", stackP4)
  
  
  dicP4 = {"Nom" : nomP4, "Stack": stackP4, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP4, "Statut": Statut}
  return dicP4

def reconnaitreP5Windows10_6():
  dicP5 = {}
  nomP5 =  reconnaitreTxt(screenshot_path,1203,256,1417,292,"nomP5")
  miseActuelleP5 =  reconnaitreBB(screenshot_path,1071,360,1230,400,"miseActuelleP5") # a faire plus tard !!!!!!!!!!!
  stackP5 =  reconnaitreBB(screenshot_path,1207,285,1404,340,"stackP5") 
  
  reconnaitreCartes(screenshot_cartes_path_back,1231,172,1231+45+75,172+45,"b5") 
  b5 = matchingBack(f"{screenshot_cartes_path_back}/b5.png")
   
  if b5=="couché":
    Statut="couché"
  else:
    Statut = "En jeu"
  
  nomP5 =  re.sub(regex, "", nomP5)
  miseActuelleP5 =  re.sub(regex, "", miseActuelleP5)
  stackP5 =  re.sub(regex, "", stackP5)
  stackP5 =  re.sub("BB.*", "BB", stackP5)
  
  
  dicP5 = {"Nom" : nomP5, "Stack": stackP5, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP5, "Statut": Statut}
  return dicP5

def reconnaitreP6Windows10_6():
  dicP6 = {}
  nomP6 =  reconnaitreTxt(screenshot_path,1198,703,1410,733,"nomP6")
  miseActuelleP6 =  reconnaitreBB(screenshot_path,1100,635,1200,677,"miseActuelleP6") # a faire plus tard !!!!!!!!!!!
  stackP6 =  reconnaitreBB(screenshot_path,1211,640,1420,792,"stackP6") 
  
  reconnaitreCartes(screenshot_cartes_path_back,1231,621,1231+45+75,621+45,"b6") 
  b6 = matchingBack(f"{screenshot_cartes_path_back}/b6.png")
  
  if b6=="couché":
    Statut="couché"
  else:
    Statut = "En jeu"
  
  nomP6 =  re.sub(regex, "", nomP6)
  miseActuelleP6 =  re.sub(regex, "", miseActuelleP6)
  stackP6 =  re.sub(regex, "", stackP6)
  stackP6 =  re.sub("BB.*", "BB", stackP6)
  
  dicP6 = {"Nom" : nomP6, "Stack": stackP6, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP6, "Statut": Statut}
  return dicP6

def reconnaitreMesDonneesWindows10_6():
  p1c1 =""
  p1c2 =""
  dicP1 = {}
  nomP1 =  reconnaitreTxt(screenshot_path,757,778,931,807,"nomP1")
  miseActuelleP1 =  reconnaitreBB(screenshot_path,763,660,949,695,"miseActuelleP1")
  stackP1 =  reconnaitreBB(screenshot_path,724,808,970,863,"stackP1")
  
  p1c1 = reconnaitreCartes(screenshot_cartes_path_c,768,694,771+48,696+45,"p1c1")  
  p1c2 = reconnaitreCartes(screenshot_cartes_path_c,808,695,808+75,695+45,"p1c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
  return dicP1

def parallel_recognize_players_data():
    with ThreadPoolExecutor(max_workers=7) as executor:
        future_pots = executor.submit(reconnaitrePotsWindows10_6)
        future_p1 = executor.submit(reconnaitreMesDonneesWindows10_6)
        future_p2 = executor.submit(reconnaitreP2Windows10_6)
        future_p3 = executor.submit(reconnaitreP3Windows10_6)
        future_p4 = executor.submit(reconnaitreP4Windows10_6)
        future_p5 = executor.submit(reconnaitreP5Windows10_6)
        future_p6 = executor.submit(reconnaitreP6Windows10_6)

        pots = future_pots.result()
        p1 = future_p1.result()
        p2 = future_p2.result()
        p3 = future_p3.result()
        p4 = future_p4.result()
        p5 = future_p5.result()
        p6 = future_p6.result()

    return pots, p1, p2, p3, p4, p5, p6



def reconnaitreActionsPossible():
  actionPossible = [] 
  actionPossible.append(reconnaitreTxt(screenshot_path,440,970,440+200,970+60,"fold"))
  actionPossible.append(reconnaitreTxt(screenshot_path,709,970,709+200,970+60,"call"))
  actionPossible.append(reconnaitreTxt(screenshot_path,977,970,977+200,970+60,"raise"))
  
  return actionPossible

def remplirJSON():
    pots, p1, p2, p3, p4, p5, p6 = parallel_recognize_players_data()
  
    flop, turn, river = recognize_all_board_cards() 

    actionsPossible = reconnaitreActionsPossible()
    
    finalRequest = f"""
        Joueurs:
        - Mon Nom: {p1["Nom"]}
            Ma bankroll: {p1["Stack"]}
            Mes Cartes: {p1["Cartes"]}
            Ma Mise Actuelle: {p1["MiseActuelle"]}
            Mon Statut: {p1["Statut"]}

        - Nom: {p2["Nom"]}
            bankroll: {p2["Stack"]}
            Mise Actuelle: {p2["MiseActuelle"]}
            Statut: {p2["Statut"]}

        - Nom: {p3["Nom"]}
            bankroll: {p3["Stack"]}
            Mise Actuelle: {p3["MiseActuelle"]}
            Statut: {p3["Statut"]}

        - Nom: {p4["Nom"]}
            bankroll: {p4["Stack"]}
            Mise Actuelle: {p4["MiseActuelle"]}
            Statut: {p4["Statut"]}

        - Nom: {p5["Nom"]}
            bankroll: {p5["Stack"]}
            Mise Actuelle: {p5["MiseActuelle"]}
            Statut: {p5["Statut"]}
            
        - Nom: {p6["Nom"]}
            bankroll: {p6["Stack"]}
            Mise Actuelle: {p6["MiseActuelle"]}
            Statut: {p6["Statut"]}

        Pot: {pots["Pots"]}
        Cartes Communes: flop: {flop} turn: {turn} river: {river}
        Mes Actions possibles: {actionsPossible}
        Mes mises possibles: 2.225BB, 2.5BB, 2.75BB, 3BB, 3.5BB, x4BB
    """ 
    print(finalRequest)
    return finalRequest
  
  
def remplirJSONsimplifie():
    pots, p1, p2, p3, p4, p5, p6 = parallel_recognize_players_data()

  
    flop, turn, river = recognize_all_board_cards() 

    actionsPossible = reconnaitreActionsPossible()

    finalRequest = f"""
        Joueurs:
            Mon Stack: {p1["Stack"]}
            Mes Cartes: {p1["Cartes"]}
            Ma Mise Actuelle: {p1["MiseActuelle"]}
            Mon Statut: {p1["Statut"]}

        - Nom: {p2["Nom"]}
            Stack: {p2["Stack"]}
            Statut: {p2["Statut"]}

        - Nom: {p3["Nom"]}
            Stack: {p3["Stack"]}
            Statut: {p3["Statut"]}

        - Nom: {p4["Nom"]}
            Stack: {p4["Stack"]}
            Statut: {p4["Statut"]}

        - Nom: {p5["Nom"]}
            Stack: {p5["Stack"]}
            Statut: {p5["Statut"]}
            
        - Nom: {p6["Nom"]}
            Stack: {p6["Stack"]}
            Statut: {p6["Statut"]}

        Pot: {pots["Pots"]}
        Cartes Communes: {flop} {turn} {river}
        actions possible : {actionsPossible}
    """ 
    print(finalRequest)
    return finalRequest

def envoyerAGPT(nomPage):
    questionGPT = remplirJSON()
    #questionGPT = remplirJSONsimplifie()
    pyperclip.copy(str(questionGPT))
    try:
      fenetreGPT = gw.getWindowsWithTitle(nomPage)
      if fenetreGPT:
        fenetreGPT = fenetreGPT[0]
        pyautogui.click(x=1200, y=950) #-40  # Coordonnées du champ d'entrée
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # Coller le contenu de questionGPT
        time.sleep(0.1)
        pyautogui.press('enter')  # Appuyer sur la touche Entrée
        del fenetreGPT
    except Exception as e:
        print(f"Erreur lors de l'activation de la fenêtre: {e}")
        return
    gc.collect()
    #fenetre[0].minimize()
    
def envoyerABard(nomPage,screenshot):
    
    image = Image.open(screenshot_path)
    # Copier l'image dans le presse-papiers
    output = BytesIO()
    image.save(output, format='BMP')
    data = output.getvalue()[14:]  # Le format BMP contient un en-tête de 14 octets qu'il faut supprimer
    output.close()

    win32clipboard.OpenClipboard()  # Ouvrir le presse-papiers
    win32clipboard.EmptyClipboard()  # Vider le presse-papiers
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # Copier l'image
    win32clipboard.CloseClipboard()  # Fermer le presse-papiers
    try:
      fenetreGPT = gw.getWindowsWithTitle(nomPage)
      if fenetreGPT:
        fenetreGPT = fenetreGPT[0]
        pyautogui.click(x=1100, y=950) #-40  # Coordonnées du champ d'entrée
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # Coller le contenu de questionGPT
        time.sleep(2)
        requete = "Donne moi la meilleure action a jouer dans ce cas de figure"
        pyperclip.copy(str(requete))
        time.sleep(0.1)
        pyautogui.click(x=1100, y=875) #-40  # Coordonnées du champ d'entrée
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # Coller le contenu de questionGPT
        time.sleep(0.1)
        pyautogui.press('enter')  # Appuyer sur la touche Entrée
        del fenetreGPT
    except Exception as e:
        print(f"Erreur lors de l'activation de la fenêtre: {e}")
        return

    
   
    gc.collect()
    #fenetre[0].minimize()

#screenshot(nomPage,screenshot_path)
#afficherImage("capture.png")
#screenshot(nomPage2,screenshot_path2)

def test():
  pots, p1, p2, p3, p4, p5, p6 = parallel_recognize_players_data()
  print(pots)
  print(p1)
  print(p2)
  print(p3)
  print(p4)
  print(p5)
  print(p6)
  
  flop, turn, river = recognize_all_board_cards() 
  print(flop)
  print(turn)
  print(river)

  print("flop : "+ str(flop))
  print("turn : "+ turn)
  print("river :"+ river)
  
  print(reconnaitreActionsPossible())
  afficherImage(screenshot_path)

