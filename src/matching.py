import cv2
import numpy as np
import pyautogui
import os

baseImageFull = "../matching/card/full"
baseImageFullChris = "../matching/card/full_chris"
baseImageC = "../matching/card/c"
baseImageBack = "../matching/card/back"

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
    elif baseImage == baseImageFullChris:
        largeur_base=101
        hauteur_base=153
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

matching('../matching/screens/flop/f1.png', baseImageFullChris)
matching('../matching/screens/flop/f2.png', baseImageFullChris)
matching('../matching/screens/flop/f3.png', baseImageFullChris)
matching('../matching/screens/turn/t.png', baseImageFullChris)
matching('../matching/screens/river/r.png', baseImageFullChris)

# matching('../matching/screens/c/1C.png', baseImageC)
# matching('../matching/screens/c/2C.png', baseImageC)
# matching('../matching/screens/c/3C.png', baseImageC)
# matching('../matching/screens/c/4C.png', baseImageC)
# matching('../matching/screens/c/5C.png', baseImageC)
# matching('../matching/screens/c/6C.png', baseImageC)
# matching('../matching/screens/c/7C.png', baseImageC)
# matching('../matching/screens/c/8C.png', baseImageC)
# matching('../matching/screens/c/9C.png', baseImageC)
# matching('../matching/screens/c/10C.png',baseImageC)
# matching('../matching/screens/c/JC.png', baseImageC)
# matching('../matching/screens/c/QC.png', baseImageC)
# matching('../matching/screens/c/KC.png', baseImageC)

# matching('../matching/screens/c/1H.png', baseImageC)
# matching('../matching/screens/c/2H.png', baseImageC)
# matching('../matching/screens/c/3H.png', baseImageC)
# matching('../matching/screens/c/4H.png', baseImageC)
# matching('../matching/screens/c/5H.png', baseImageC)
# matching('../matching/screens/c/6H.png', baseImageC)
# matching('../matching/screens/c/7H.png', baseImageC)
# matching('../matching/screens/c/8H.png', baseImageC)
# matching('../matching/screens/c/9H.png', baseImageC)
# matching('../matching/screens/c/10H.png', baseImageC)
# matching('../matching/screens/c/JH.png', baseImageC)
# matching('../matching/screens/c/QH.png', baseImageC)
# matching('../matching/screens/c/KH.png', baseImageC)

# matching('../matching/screens/flop/1D.png', baseImageFull)
# matching('../matching/screens/flop/2D.png', baseImageFull)
# matching('../matching/screens/flop/3D.png', baseImageFull)
# matching('../matching/screens/flop/4D.png', baseImageFull)
# matching('../matching/screens/flop/5D.png', baseImageFull)
# matching('../matching/screens/flop/6D.png', baseImageFull)
# matching('../matching/screens/flop/7D.png', baseImageFull)
# matching('../matching/screens/flop/8D.png', baseImageFull)
# matching('../matching/screens/flop/9D.png', baseImageFull)
# matching('../matching/screens/flop/10D.png',baseImageFull)
# matching('../matching/screens/flop/JD.png', baseImageFull)
# matching('../matching/screens/flop/QD.png', baseImageFull)
# matching('../matching/screens/flop/KD.png', baseImageFull)

# matching('../matching/screens/flop/1S.png', baseImageFull)
# matching('../matching/screens/flop/2S.png', baseImageFull)
# matching('../matching/screens/flop/3S.png', baseImageFull)
# matching('../matching/screens/flop/4S.png', baseImageFull)
# matching('../matching/screens/flop/5S.png', baseImageFull)
# matching('../matching/screens/flop/6S.png', baseImageFull)
# matching('../matching/screens/flop/7S.png', baseImageFull)
# matching('../matching/screens/flop/8S.png', baseImageFull)
# matching('../matching/screens/flop/9S.png', baseImageFull)
# matching('../matching/screens/flop/10S.png',baseImageFull)
# matching('../matching/screens/flop/JS.png', baseImageFull)
# matching('../matching/screens/flop/QS.png', baseImageFull)
# matching('../matching/screens/flop/KS.png', baseImageFull)

