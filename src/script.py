import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
from openai import OpenAI
import time

    
import pytesseract
from PIL import Image

nomPage = "Playground"
nomPage2="Gestionnaire des tâches"
screenshot_path = "../assets/capture.png"
screenshot_path2 = "../assets/capture2.png"
path_base = '..//assets//'

print(gw.getAllTitles())

def screenshot(nomPage, screenshot_path):
      fenetre = gw.getWindowsWithTitle(nomPage)
      if len(fenetre) > 0:
        left, top, width, height = fenetre[0].left, fenetre[0].top, fenetre[0].width, fenetre[0].height
        fenetre[0].activate() 
          # Mettre la fenêtre en plein écran (ou maximisée)
        fenetre[0].maximize()
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
        # Minimiser la fenêtre
        fenetre[0].minimize()
      else:
        print(f"L'onglet '{nomPage}' n'a pas été trouvé. Réessai en cours...")


      

def afficherImage(imageName, titre=""):
    image = cv2.imread(path_base + imageName)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertir de BGR (format OpenCV) à RGB
    plt.imshow(image_rgb)
    plt.title(titre)
    plt.show()
    

def reconnaitreTexteCoordonees(screenshot_path, x1,y1,x2,y2):
  image = Image.open(screenshot_path)

  cropped_image = image.crop((x1, y1, x2, y2))
  text = pytesseract.image_to_string(cropped_image)

  print(text)
  return text


def reconnaitrePotTotal(screenshot_path,x1,y1,x2,y2):
  potTotal= reconnaitreTexteCoordonees(screenshot_path, x1, y1, x2, y2)
  print("test")
  print(f"\n{potTotal}")
  return potTotal
  
def reconnaitreMesDonnees(screenshot_path,x1,y1,x2,y2):
  # pseudo = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)
  # mise = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)
  # mise = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)
  monRectangle = reconnaitreTexteCoordonees(screenshot_path,x1,y1,x2,y2)
  return monRectangle

# def reconnaitresDonneesAutres(screenshot_path, x1,y1,x2,y2):
#   pseudo = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)
#   mise = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)
#   mise = reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)


      

# screenshot(nomPage2,screenshot_path2)
# afficherImage("capture2.png")

#screenshot(nomPage,screenshot_path)
afficherImage("capture.png")

#reconnaitreTexteCoordonees(screenshot_path, 407, 553, 505, 597)

#reconnaitrePotTotal(screenshot_path, 756, 560, 1000, 590)
reconnaitreMesDonnees(screenshot_path, 716, 649, 912, 860)

    

