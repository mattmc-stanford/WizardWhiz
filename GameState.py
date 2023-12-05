import numpy as np
from Card import Card
from Players import RandomAgent, ExpertAgent


class GameState:
    def __init__(self):
        cardnames = ['WW', 'WW', 'WW', 'WW', 'AS', 'AC', 'AD', 'AH', 'KC', 'KS', 'KD', 'KH', 'QD', 'QC', 'QH', 'QS',
                     'JS', 'JH', 'JC', 'JD', 'TH', 'TC', 'TD', 'TS', '9S', '9H', '9C', '9D', '8D', '8C', '8S', '8H',
                     '7C', '7H', '7D', '7S', '6S', '6H', '6D', '6C', '5D', '5H', '5C', '5S', '4C', '4D', '4S', '4H',
                     '3D', '3C', '3S', '3H', '2H', '2S', '2C', '2D', 'NN', 'NN', 'NN', 'NN']
        self.deck = [None]*60
        for i, c in enumerate(cardnames):
            match c[0]:
                case 'T':
                    self.deck[i] = Card(c, 10, i)
                case 'J':
                    self.deck[i] = Card(c, 11, i)
                case 'Q':
                    self.deck[i] = Card(c, 12, i)
                case 'K':
                    self.deck[i] = Card(c, 13, i)
                case 'A':
                    self.deck[i] = Card(c, 14, i)
                case 'W':
                    self.deck[i] = Card(c, 1000, i)
                case 'N':
                    self.deck[i] = Card(c, 0, i)
                case _:
                    self.deck[i] = Card(c, int(c[0]), i)
                
        idx = np.random.permutation(self.deck)  # deal
        self.players = [RandomAgent(1, idx[:15]),  # players
                        RandomAgent(2, idx[15:30]),
                        RandomAgent(0, idx[30:45]),
                        RandomAgent(3, idx[45:])]

        #self.placement = np.random.permutation([0, 1, 2, 3])  # current order of play
        self.players = np.random.permutation(self.players)
        bid = 0
        illegal = []
        for i, P in enumerate(self.players):
            #self.players[p].set_placement(self.placement[p])
            #if p == self.placement[-1]:
            if i == 4:
                illegal = 15 - bid
            #bid += self.players[p].bid_policy(illegal)  # place bids
            bid += P.bid_policy(illegal)

        self.lead = None  # suit that was lead
        
    def set_lead(self, lead):
        self.lead = lead
        for P in self.players:
            P.set_lead(lead)
            
    def set_placement(self, winner):
        #idx = np.argwhere(self.placement == winner)[0][0]
        #self.placement = np.hstack((self.placement[idx:], self.placement[:idx]))
        temp = np.zeros(4)
        for i in range(4):
            temp[i] = self.players[i].number
        try:
            idx = np.argwhere(winner == temp)[0][0]
        except:
            print('FUck this')
        self.players = np.hstack((self.players[idx:], self.players[:idx]))

    def card_played(self, cards):
        for c in cards:
            self.deck.remove(c)

