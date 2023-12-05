# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
from GameState import GameState
from Card import Card


def play_round():
    GS = GameState()  # Initialize the round (deal and place bids)
    plead = np.zeros(4)
    #plead[GS.placement[0]] += 1
    # Loop through tricks
    for t in range(15):
        # for each agent in order, play card according to policy (call play_trick)
        #plead[GS.placement[0]] += 1
        play_trick(GS)

    # Report results
    best = -np.inf
    bestplayer = -1
    for k, P in enumerate(GS.players):
        if P.bid == P.ntricks:
            score = 20 + P.bid * 10
        else:
            score = -10 * np.abs(P.bid - P.ntricks)
        #print("Player", k, " bid ", P.bid, " and took ", P.ntricks, ". SCORE: ", score)
        if score > best:
            best = score
            bestplayer = P

    #print('The winner is: Player ', bestplayer)
    #print(plead)
    return bestplayer.number, plead


def play_trick(GS):
    trick = []  # Should be part of GS?
    for P in GS.players:
        trick.append(P.play_policy())
        if GS.lead is None and not trick[-1].name == 'NN':
            GS.set_lead(trick[-1].suit)
    GS.card_played(trick)
    twinner = check_winner(GS, trick)
    tricknames = []
    for c in trick: tricknames += [c.name]
    #print("Trick: ", tricknames, "    Lead: ", GS.lead, "    Winner: ", twinner + 1)
    #winner = GS.placement[twinner]
    #GS.players[winner].ntricks += 1
    GS.players[twinner].ntricks += 1
    GS.set_lead(None)
    GS.set_placement(twinner)
    return trick[twinner]
    
    
def check_winner(GS, trick):
    best = 0
    for idx, c in enumerate(trick):
        if c.suit == 'W':  # first player to play wizard
            return idx
        elif GS.lead is not None and c.suit == GS.lead:  # highest card of lead suit
            if c.value > trick[best].value:
                best = idx
    return best
    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play_round()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
