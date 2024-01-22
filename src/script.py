import pygetwindow as gw
import pyautogui
from matplotlib import pyplot as plt
import cv2
from openai import OpenAI

    
import pytesseract
from PIL import Image

nomPage = "Playground"
screenshot_path = "../assets/capture.png"
path_base = '..//assets//'


def screenshot(nomPage,screenshot_path):
  fenetre = gw.getWindowsWithTitle(nomPage)

  if len(fenetre) > 0:
      left, top, width, height = fenetre[0].left, fenetre[0].top, fenetre[0].width, fenetre[0].height
      fenetre[0].activate()  
      screenshot = pyautogui.screenshot(region=(left, top, width, height))
      screenshot.save(screenshot_path)
      print(f"Capture d'écran de l'onglet enregistrée sous : {screenshot_path}")
      
      
  else:
      print(f"L'onglet '{nomPage}' n'a pas été trouvé.")
      

def afficherImage(imageName, titre=""):
    image = cv2.imread(path_base + imageName)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertir de BGR (format OpenCV) à RGB
    plt.imshow(image_rgb)
    plt.title(titre)
    plt.show()
    

def reconnaitreTexteCoordonees():
  image = Image.open(screenshot_path)
  x1, y1, x2, y2 = 407, 553, 505, 597  

  cropped_image = image.crop((x1, y1, x2, y2))
  text = pytesseract.image_to_string(cropped_image)

  print(text)




      
#screenshot(nomPage,screenshot_path)
afficherImage("capture.png")
reconnaitreTexteCoordonees()

    

