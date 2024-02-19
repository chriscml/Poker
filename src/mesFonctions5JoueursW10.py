from utility import *

def reconnaitreBlindesTournoi():
  dicBlindes = {}
  blindes= reconnaitreTxt(screenshot_path,119,23,405,58,"blindes")
  blindes = re.sub(regexBlindes, "", blindes)
  blindes = re.sub(r'€.*', '€', blindes)
  dicBlindes = {"Blindes" :blindes}
  return dicBlindes

def reconnaitrePotsWindows10_6():
    dicPots = {}
    pots = reconnaitreTxt(screenshot_path, 750, 530, 1009, 602, "pots")
    
    # Use regular expression to remove everything before the first occurrence of 'Pot'
    pots_cleaned = re.sub(r'^.*?Pot', 'Pot', pots)
    
    dicPots = {"Pots": pots_cleaned}
    return dicPots


def reconnaitreP2Windows10_6():
  dicP2 = {}
  nomP2 =  reconnaitreTxt(screenshot_path,240,617,240+200,617+30,"nomP2")
  miseActuelleP2 =  reconnaitreBB(screenshot_path,448,583,603+140,583+50,"miseActuelleP2") # a faire plus tard !!!!!!!!!!!
  stackP2 =  reconnaitreBB(screenshot_path,244,650,244+210,650+55,"stackP2")

  reconnaitreCartes(screenshot_cartes_path_back,268,534,268+45+75,534+45,"b2") 
  b2 = matchingBack(f"{screenshot_cartes_path_back}/b2.png")
   
  if b2=="fold":
    Statut="fold"
  else:
    Statut = "In game"
    
  
  nomP2 =  re.sub(regex, "", nomP2)
  miseActuelleP2 =  re.sub(regex, "", miseActuelleP2)
  stackP2 =  re.sub(regex, "", stackP2)
  stackP2 =  re.sub("BB.*", "BB", stackP2)
  
  
  dicP2 = {"Nom" : nomP2, "Stack": stackP2, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP2, "Statut": Statut}
  return dicP2

def reconnaitreP3Windows10_6():
  dicP3 = {}
  nomP3 =  reconnaitreTxt(screenshot_path,445,178,445+200,178+30,"nomP3")
  miseActuelleP3 =  reconnaitreBB(screenshot_path,572,334,572+140,334+50,"miseActuelleP3")
  stackP3 =  reconnaitreBB(screenshot_path,445,212,445+200,212+50,"stackP3")
  
  reconnaitreCartes(screenshot_cartes_path_back,460,98,460+45+75,98+45,"b3") 
  b3 = matchingBack(f"{screenshot_cartes_path_back}/b3.png")
   
  if b3=="fold":
    Statut="fold"
  else:
    Statut = "In game"
  
  nomP3 =  re.sub(regex, "", nomP3)
  miseActuelleP3 =  re.sub(regex, "", miseActuelleP3)
  stackP3 =  re.sub(regex, "", stackP3)
  stackP3 =  re.sub("BB.*", "BB", stackP3)
  
  
  dicP3 = {"Nom" : nomP3, "Stack": stackP3, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP3, "Statut": Statut}
  return dicP3

def reconnaitreP4Windows10_6():
  dicP4 = {}
  nomP4 =  reconnaitreTxt(screenshot_path,1045,178,1045+200,178+30,"nomP4")
  miseActuelleP4 =  reconnaitreBB(screenshot_path,960,335,960+140,335+50,"miseActuelleP4") # a faire plus tard !!!!!!!!!!!
  stackP4 =  reconnaitreBB(screenshot_path,1045,212,1045+200,212+50,"stackP4") 
  
  reconnaitreCartes(screenshot_cartes_path_back,1074,98,1074+45+75,98+45,"b4") 
  b4 = matchingBack(f"{screenshot_cartes_path_back}/b4.png")
   
  if b4=="fold":
    Statut="fold"
  else:
    Statut = "In game"
  
  nomP4 =  re.sub(regex, "", nomP4)
  miseActuelleP4 =  re.sub(regex, "", miseActuelleP4)
  stackP4 =  re.sub(regex, "", stackP4)
  stackP4 =  re.sub("BB.*", "BB", stackP4)
  
  
  dicP4 = {"Nom" : nomP4, "Stack": stackP4, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP4, "Statut": Statut}
  return dicP4

def reconnaitreP5Windows10_6():
  dicP5 = {}
  nomP5 =  reconnaitreTxt(screenshot_path,1238,616,1238+200,616+30,"nomP5")
  miseActuelleP5 =  reconnaitreBB(screenshot_path,1112,583,1112+140,583+50,"miseActuelleP5") # a faire plus tard !!!!!!!!!!!
  stackP5 =  reconnaitreBB(screenshot_path,1228,648,1230+208,648+50,"stackP5") 
  
  reconnaitreCartes(screenshot_cartes_path_back,1266,534,1266+45+75,534+45,"b5") 
  b5 = matchingBack(f"{screenshot_cartes_path_back}/b5.png")
   
  if b5=="fold":
    Statut="fold"
  else:
    Statut = "In game"
  
  nomP5 =  re.sub(regex, "", nomP5)
  miseActuelleP5 =  re.sub(regex, "", miseActuelleP5)
  stackP5 =  re.sub(regex, "", stackP5)
  stackP5 =  re.sub("BB.*", "BB", stackP5)
  
  
  dicP5 = {"Nom" : nomP5, "Stack": stackP5, "Cartes":["On ne sait pas"], "MiseActuelle": miseActuelleP5, "Statut": Statut}
  return dicP5

def reconnaitreMesDonneesWindows10_6():
  p1c1 =""
  p1c2 =""
  dicP1 = {}
  nomP1 =  reconnaitreTxt(screenshot_path,757,778,931,807,"nomP1")
  miseActuelleP1 =  reconnaitreBB(screenshot_path,763,660,949,695,"miseActuelleP1")
  stackP1 =  reconnaitreBB(screenshot_path,724,808,970,863,"stackP1")
  
  p1c1 = reconnaitreCartes(screenshot_cartes_path_c,758,685,758+58,685+55,"p1c1")  
  p1c2 = reconnaitreCartes(screenshot_cartes_path_c,808,685,808+75,685+55,"p1c2") 
  #reconnaitre status si il n'y a aucune carte 
  
  nomP1 =  re.sub(regex, "", nomP1)
  miseActuelleP1 =  re.sub(regex, "", miseActuelleP1)
  stackP1 =  re.sub(regex, "", stackP1)
  stackP1 =  re.sub("BB.*", "BB", stackP1)
  
  dicP1 = {"Nom" : nomP1, "Stack": stackP1, "Cartes":[p1c1,p1c2], "MiseActuelle": miseActuelleP1, "Statut": "In game"}
  return dicP1


def parallel_recognize_players_data():
    with ThreadPoolExecutor(max_workers=7) as executor:
        future_pots = executor.submit(reconnaitrePotsWindows10_6)
        future_p1 = executor.submit(reconnaitreMesDonneesWindows10_6)
        future_p2 = executor.submit(reconnaitreP2Windows10_6)
        future_p3 = executor.submit(reconnaitreP3Windows10_6)
        future_p4 = executor.submit(reconnaitreP4Windows10_6)
        future_p5 = executor.submit(reconnaitreP5Windows10_6)

        pots = future_pots.result()
        p1 = future_p1.result()
        p2 = future_p2.result()
        p3 = future_p3.result()
        p4 = future_p4.result()
        p5 = future_p5.result()

    return pots, p1, p2, p3, p4, p5



def reconnaitreActionsPossible():
  actionPossible = [] 
  actionPossible.append(reconnaitreTxt(screenshot_path,440,970,440+200,970+60,"fold"))
  actionPossible.append(reconnaitreTxt(screenshot_path,709,970,709+200,970+60,"call"))
  actionPossible.append(reconnaitreTxt(screenshot_path,977,970,977+200,970+60,"raise"))
  
  return actionPossible


  
def remplirJSON5joueursW10():
        # Redirigez les sorties print vers la zone de texte
        pots, p1, p2, p3, p4, p5 = parallel_recognize_players_data()

        # Effectuez les opérations nécessaires dans remplirJSON()
        print(f""" Joueurs:
            - My Name: {p1["Nom"]};
                Ma bankroll: {p1["Stack"]};
                My Cards: {p1["Cartes"]};
                My State: {p1["Statut"]};
            - name player2: {p2["Nom"]};
                bankroll: {p2["Stack"]};
                actual bet: {p2["MiseActuelle"]};
                State: {p2["Statut"]};
            - name player3: {p3["Nom"]};
                bankroll: {p3["Stack"]};
                actual bet: {p3["MiseActuelle"]};
                State: {p3["Statut"]};
            - name player4: {p4["Nom"]};
                bankroll: {p4["Stack"]};
                actual bet: {p4["MiseActuelle"]};
                State: {p4["Statut"]};
            - name player5: {p5["Nom"]};
                bankroll: {p5["Stack"]};
                actual bet: {p5["MiseActuelle"]};
                State: {p5["Statut"]};""") 
        flop, turn, river = recognize_all_board_cards()
        
        print(f"""Pot: {pots["Pots"]};\nCommunity Cards: flop: {flop};\n turn: {turn};\n river: {river};\n""")
        
        actionsPossible = reconnaitreActionsPossible()
        print(f"""Moves I can do: {actionsPossible}\n Money I can bet: 2.225BB, 2.5BB, 2.75BB, 3BB, 3.5BB, 4BB""")

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

            Pot: {pots["Pots"]}
            Community Cards: flop: {flop} turn: {turn} river: {river}
            
            
            Moves I can do: {actionsPossible}
        """
        
        return finalRequest
  
def remplirJSON5joueursW10VISION():
      # Redirigez les sorties print vers la zone de texte
      pots, p1, p2, p3, p4, p5 = parallel_recognize_players_data()
      
      finalRequest = f"""
          Joueurs:
          - My Name: {p1["Nom"]}
              My bankroll: {p1["Stack"]}
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

          Pot: {pots["Pots"]}
          
      """
      print(finalRequest)
      
      return finalRequest


    #fenetre[0].minimize()
    
def test():
  pots, p1, p2, p3, p4, p5 = parallel_recognize_players_data()
  print(pots)
  print(p1)
  print(p2)
  print(p3)
  print(p4)
  print(p5)
  
  flop, turn, river = recognize_all_board_cards() 
  print(flop)
  print(turn)
  print(river)

  print("flop : "+ str(flop))
  print("turn : "+ turn)
  print("river :"+ river)
  
  print(reconnaitreActionsPossible())
  afficherImage(screenshot_path)

