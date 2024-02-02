from utility import *


def reconnaitrePotsWindows10_6():
    dicPots = {}
    pots = reconnaitreTxt(screenshot_path, 760, 530, 1009, 602, "pots")
    
    # Use regular expression to remove everything before the first occurrence of 'Pot'
    pots_cleaned = re.sub(r'^.*?Pot', 'Pot', pots)
    
    dicPots = {"Pots": pots_cleaned}
    return dicPots


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
  
  p1c1 = reconnaitreCartes(screenshot_cartes_path_c,768,694,761+55,696+45,"p1c1")  
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

def remplirJSON6joueursW10():
        # Redirigez les sorties print vers la zone de texte
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
        flop, turn, river = recognize_all_board_cards()
        
        print(f"""Pot: {pots["Pots"]}
            Community Cards: flop: {flop} turn: {turn} river: {river}""")
        
        actionsPossible = reconnaitreActionsPossible()
        print(f"""Moves I can do: {actionsPossible}
            Money I can bet: 2.225BB, 2.5BB, 2.75BB, 3BB, 3.5BB, 4BB""")

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

        return finalRequest

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

