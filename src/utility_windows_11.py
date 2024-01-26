from script import *


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
  stackP2 =  reconnaitreBB(screenshot_path,285,735,496,794,"stackP2")

  reconnaitreCartes(screenshot_cartes_path_back,302,622,302+45+75,622+45,"b2") 
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
  miseActuelleP6 =  reconnaitreBB(screenshot_path,1211,735,1420,792,"miseActuelleP6") # a faire plus tard !!!!!!!!!!!
  stackP6 =  reconnaitreBB(screenshot_path,1211,735,1420,792,"stackP6") 
  
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
  
  p1c1 = reconnaitreCartes(screenshot_cartes_path_c,771,698,771+38,696+43,"p1c1")  
  p1c2 = reconnaitreCartes(screenshot_cartes_path_c,808,695,808+75,695+45,"p1c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
  return dicP1


def reconnaitreActionsPossible():
  actionPossible = [] 
  actionPossible.append(reconnaitreTxt(screenshot_path,440,970,440+200,970+60,"fold"))
  actionPossible.append(reconnaitreTxt(screenshot_path,709,970,709+200,970+60,"call"))
  actionPossible.append(reconnaitreTxt(screenshot_path,977,970,977+200,970+60,"raise"))
  
  return actionPossible