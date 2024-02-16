from numpy import var
import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
import openai 
import time
import re
import pyperclip
import numpy as np
import os
import win32gui as gw

from pywinauto.application import Application
import pyautogui
    
import pytesseract
from PIL import Image

from pywinauto import Desktop

from concurrent.futures import ThreadPoolExecutor

from sklearn.cluster import KMeans

import gc 


from numpy import var
import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
import openai 
import time
import re
import pyperclip
import numpy as np
import os

from pywinauto.application import Application
import pyautogui
    
import pytesseract
from PIL import Image

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

nomPageChatGPT = "ChatGPT - Google Chrome"
nomPageConseilDePokerEnDirect ="Conseils de poker en direct - Google Chrome"
nomPageVSCODE = "script.py - poker - Visual Studio Code"
nomPageProgramme="My App"

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
    scale_percent = 130  # percent of original size
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

    nom_carte = meilleure_correspondance.split('.')[0] if meilleure_correspondance else "fold"
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

    nom_carte = 'no card yet' if meilleure_correspondance else "a card"
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
        return ' of spades '  # Spades
    elif dominant_color[0] > dominant_color[1] and dominant_color[0] > dominant_color[2]:  # Red dominant
        return ' of hearts'  # Hearts
    elif dominant_color[2] > dominant_color[0] and dominant_color[2] > dominant_color[1]:  # Blue dominant
        return ' of diamonds'  # Diamonds
    elif dominant_color[1] > dominant_color[0] and dominant_color[1] > dominant_color[2]:  # Green dominant
        return ' of clover'  # Clubs
    else:
        return "no card yet"
      
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
    
    if couleur_dominante == 'no card yet':
      return 'no card yet'
  
    # Preprocess the image for better OCR
    preprocessed_image = preprocess_image(cropped_image)
    
    # Configure tesseract to do single character recognition
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789AJQK10Q9'
    text = pytesseract.image_to_string(cropped_image, config=custom_config)
    
    if text.strip() == "1" or text.strip() == "11":
      text = "7"
      
    if text.strip()!="10":
      for caractere in text:
          if caractere.isalpha() or caractere.isdigit():
              text = caractere
              break 
          
    if text.strip() == "K":
       text="King"
    if text.strip() == "Q":
       text="Queen"
    if text.strip() == "J":
       text="Jack"
    if text.strip() == "A":
       text="ACE"
    
  
    nomCarte = text.strip() + couleur_dominante
    
    if text == "":
       nomCarte="no card yet"
    
      
    return nomCarte

def reconnaitreFlop():
  flop=[]
  flop1 = reconnaitreCartes(screenshot_cartes_path_flop,566,353,566+99,358+55,"f1")
  f1 = matchingVide(f"{screenshot_cartes_path_flop}/f1.png")
  if f1 == "no card yet":
    flop1 = f1
  
  flop2 = reconnaitreCartes(screenshot_cartes_path_flop,678,353,678+99,358+55,"f2")
  f2 = matchingVide(f"{screenshot_cartes_path_flop}/f2.png")
  if f2 == "no card yet":
    flop2 = f2
  
  flop3 = reconnaitreCartes(screenshot_cartes_path_flop,785,353,785+103,358+55,"f3")
  f3 = matchingVide(f"{screenshot_cartes_path_flop}/f3.png")
  if f3 == "no card yet":
    flop3 = f3
    
  flop.append(flop1)
  flop.append(flop2)
  flop.append(flop3)
  return flop

def reconnaitreTurn():
  turn = reconnaitreCartes(screenshot_cartes_path_turn,898,358,898+101,368+45,"t")
  t = matchingVide(f"{screenshot_cartes_path_turn}/t.png")
  if t == "no card yet":
    turn = t
  return turn.strip()

def reconnaitreRiver():
  river = reconnaitreCartes(screenshot_cartes_path_river,1010,358,1010+101,368+45,"r")
  r = matchingVide(f"{screenshot_cartes_path_river}/r.png")
  if r == "no card yet":
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
          #fenetre.minimize()
      else:
          print(f"L'onglet '{nomPage}' n'a pas été trouvé.")

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

def envoyerAGPT(nomPage,fct):
    questionGPT = fct()
    #questionGPT = remplirJSONsimplifie()
    pyperclip.copy(str(questionGPT))
    try:
      fenetreGPT = gw.getWindowsWithTitle(nomPage)
      if fenetreGPT:
        fenetreGPT = fenetreGPT[0]
        fenetreGPT.restore()
        time.sleep(0.2)
        fenetreGPT.maximize()
        time.sleep(0.3)
        pyautogui.click(x=1400, y=965) #-40  # Coordonnées du champ d'entrée
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # Coller le contenu de questionGPT
        time.sleep(0.1)
        pyautogui.press('enter')  # Appuyer sur la touche Entrée
        del fenetreGPT
    except Exception as e:
        print(f"Erreur lors de l'activation de la fenêtre: {e}")
        return
    gc.collect()

def screenshot(nomPage, screenshot_path):
  #minimiserVSCode(nomPageVSCODE)
  try:
      # Recherche de la fenêtre "Playground" par son titre
      fenetre = gw.getWindowsWithTitle(nomPage)
      if fenetre:
          fenetre = fenetre[0]
          fenetre.restore()
          fenetre.maximize()
          
          left, top, width, height = fenetre.left, fenetre.top, fenetre.width, fenetre.height
          top = top + 115
          #width = width - 300
          height = height - 130
          # Attends un court instant pour que la fenêtre apparaisse
          time.sleep(1)

          # Prend une capture d'écran de la fenêtre maximisée
          screenshot = pyautogui.screenshot(region=(left, top, width+2, height+2)) #region=(left, top, width+2, height+2) +2 pour windows 11 1938 1058
          screenshot.save(screenshot_path)
          print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
          
          #fenetre.minimize()
          
          cropImage(screenshot_path,732,574,894,740,"mescartes")
          cropImage(screenshot_path,540,260,1104,428,"cartescommunes")
          cropImage(screenshot_path,421,761,1214,910,"actionspossibles")

          # Minimise la fenêtre
          # fenetre.minimize()
      else:
          print(f"L'onglet '{nomPage}' n'a pas été trouvé.")

  except Exception as e:
      print(f"Erreur lors de la capture d'écran : {e}") 
    
  gc.collect()


def cropImage(screenshot_path, x1, y1, x2, y2, nomCrop="pseudo"):
    image = Image.open(screenshot_path)

    cropped_image = image.crop((x1, y1, x2, y2))
    
    # Save the cropped image for debugging
    cropped_image.save(f"../assets/{nomCrop}.png")


def ecranJoli(nomPageProgramme, nomPage):
    # Récupérer les fenêtres par leur titre
    fenetre1 = gw.getWindowsWithTitle(nomPage)
    fenetre2 = gw.getWindowsWithTitle(nomPageProgramme)
    
    fenetre1 = fenetre1[0]
    fenetre2 = fenetre2[0]
    
    if fenetre1 and fenetre2:
        fenetre2.restore()
        fenetre2.maximize()
        pyautogui.hotkey('winleft', 'left')
        fenetre1.restore()
        fenetre1.maximize()
        pyautogui.hotkey('winleft', 'right')
        
def deplacerFenetre(nomPage,cote):
    # Récupérer les fenêtres par leur titre
    fenetre = gw.getWindowsWithTitle(nomPage)
    
    fenetre = fenetre[0]
    
    if fenetre:
        fenetre.restore()
        fenetre.maximize()
        pyautogui.hotkey('winleft', cote)
        





