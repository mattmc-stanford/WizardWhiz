import numpy as np
from main import play_trick, play_round, check_winner
from GameState import GameState


def play_15_tricks(ranking):
    GS = GameState()  # Initialize the round (deal and place bids)

    # Loop through tricks
    for t in range(15):
        # for each agent in order, play card according to policy (call play_trick)
        winner = play_trick(GS)
        #ranking[winner] += 1
    return ranking

"""
deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        'NN', 'WW']

ranking = dict()
for c in deck:
    ranking[c] = 0

num_rounds = 10
for k in range(num_rounds):
    ranking = play_15_tricks(ranking)
    print("======================================================")

count = 0
for c in deck:
    ranking[c] = ranking[c] / (num_rounds*15)

cards = list(ranking.keys())
scores = list(ranking.values())
idx = np.argsort(scores)
scores = [scores[i] for i in idx]
cards = [cards[i] for i in idx]
print('Done')
"""

num_rounds = 5000
playerwins = np.zeros(4)
pleadtotal = np.zeros(4)
for k in range(num_rounds):
    winner, plead = play_round()
    playerwins[winner] += 1
    pleadtotal += plead
    #print("======================================================")
print(playerwins)
print(pleadtotal)



