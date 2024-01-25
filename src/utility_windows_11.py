def reconnaitreMesDonneesWindows11_6():
  p1c1=""
  p1c2=""
  dicP1 = {}
  nomP1 =  reconnaitreTexteCoordonees(screenshot_path,774,764,1050,795,"nomP1")
  miseActuelleP1 =  reconnaitreTexteCoordonees(screenshot_path,780,648,949,685,"miseActuelleP1")
  stackP1 =  reconnaitreTexteCoordonees(screenshot_path,771,798,940,859,"stackP1")
  
  p1c1 = reconnaitreCartes(screenshot_cartes_path_c,baseImageC,808,695,883,777,"p1c1") 
  #p1c2 = reconnaitreCartes(screenshot_cartes_path_c,baseImageC,1,1,1,1,"p1c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "En jeu"}
  return dicP1

def reconnaitreP2Windows11_6():
  p2c1=""
  p2c2=""
  dicP2 = {}
  nomP2 =  reconnaitreTexteCoordonees(screenshot_path,290,694,485,719,"nomP2")
  miseActuelleP2 =  reconnaitreTexteCoordonees(screenshot_path,498,630,595,676,"miseActuelleP2")
  stackP2 =  reconnaitreTexteCoordonees(screenshot_path,296,724,481,773,"stackP2")
  
  # p2c1 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c1") 
  # p2c2 = reconnaitreCartes(screenshot_cartes_path_back,baseImageBack,0,0,0,0,"p2c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP2 =  re.sub(regex, "", nomP2)
  miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
  stackP2 =  re.sub(regex, "", stackP2)
  
  dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":[p2c1,p2c2], "MiseActuelle": miseActuelleP2, "Statut": "En jeu"}
  return dicP2