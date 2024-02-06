from deuces import Card, Evaluator

def simulate_intelligent_player(player_cards, community_cards, num_simulations=10000):
    # Convertir les cartes au format attendu par la bibliothèque deuces
    player_hand = [Card.new(card[0] + card[1].lower()) for card in player_cards]
    community_hand = [Card.new(card[0] + card[1].lower()) for card in community_cards]

    # Ajouter les cartes communautaires à la main du joueur
    all_cards = player_hand + community_hand

    # Créer une instance de l'évaluateur
    evaluator = Evaluator()

    # Calculer le score du joueur
    player_score = evaluator.evaluate([], all_cards)

    # Simuler les mains des adversaires avec des mains aléatoires
    opponent_hands = [[Card.new("2s"), Card.new("3h")] for _ in range(5)]  # Exemple : tous les adversaires ont des mains aléatoires

    # Ajouter les cartes communautaires aux mains des adversaires
    all_opponent_hands = [hand + community_hand for hand in opponent_hands]

    # Calculer les scores des adversaires
    opponent_scores = [evaluator.evaluate([], opponent_hand) for opponent_hand in all_opponent_hands]

    # Compter le nombre d'opposants battus
    beats = sum(1 for score in opponent_scores if player_score > score)

    # Calculer la probabilité de victoire en pourcentage
    win_probability = (beats + 1) / (1 + len(opponent_hands)) * 100

    return win_probability

# Exemple d'utilisation
player_cards = ["Th", "Js"]  # Vos cartes (utilisez "Th" pour 10)
community_cards = ["5d", "7s", "8c", "Tc", "Ad"]  # Cartes communautaires

win_probability = simulate_intelligent_player(player_cards, community_cards)
print(f"La probabilité de victoire est : {win_probability:.2f}%")
