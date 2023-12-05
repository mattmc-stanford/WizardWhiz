# Defines non-RL Players and super Player class from which others inherit

import numpy as np
import torch
import torch.nn as nn
from Card import Card

class Player:
    def __init__(self, number, hand=[]):
        self.number = number
        self.hand = hand
        self.bid = []
        self.ntricks = 0
        self.placement = []
        self.lead = None
        self.sorted_hand = {'C': [],
                            'D': [],
                            'H': [],
                            'S': [],
                            'W': [],
                            'N': [],
                            None: []}
        for c in self.hand:
            self.sorted_hand[c.suit].append(c)
        for s in self.sorted_hand.keys():
            self.sorted_hand[s].sort(key=lambda x: x.index)

    def set_hand(self, hand):
        self.hand = hand

    def set_placement(self, placement):
        self.placement = placement
    
    def set_lead(self, lead):
        self.lead = lead


class RandomAgent(Player):
    def __init__(self, number, hand=[]):
        super().__init__(number, hand)

    def bid_policy(self, illegal=[]):
        if np.any(illegal):
            self.bid = illegal
            while self.bid == illegal:
                self.bid = np.random.randint(0, 15)
        else:
            self.bid = np.random.randint(0, 15)
        return self.bid

    def play_policy(self):
        if not self.lead == 'W' and self.sorted_hand[self.lead]:  # random play from legal actions
            action = np.random.choice(self.sorted_hand[self.lead] + self.sorted_hand['W'] + self.sorted_hand['N'])
        else:  # random play
            action = np.random.choice(self.hand)
        self.sorted_hand[action.suit].remove(action)
        self.hand = sum(list(self.sorted_hand.values()), [])
        return action


class ExpertAgent(Player):
    def __init__(self, number, hand=[], deck=[]):
        super().__init__(number, hand)
        self.deck = deck
        self.ranked_hand = []
        for c in self.hand: self.ranked_hand.append(c.index)
        self.hand = [x for _, x in sorted(zip(self.ranked_hand, self.hand))]
        self.ranked_hand.sort()
        self.ranked_hand = np.asarray(self.ranked_hand, int)
        self.risk = 0.8
        self.high = 0
        self.update_scores()

    def update_scores(self):
        cutoff = self.deck[len(self.deck) // 4 - 1].index
        self.high = np.argmax(self.ranked_hand > cutoff)  # sets high to index of first "low" card

    def bid_policy(self, illegal):
        if np.any(illegal):
            self.bid = int(self.risk * self.high)
            if self.bid == illegal:
                self.bid += np.random.choice([-1, 1])
        else:
            self.bid = int(self.risk * self.high)
        return self.bid

    def play_policy(self):
        self.update_scores()
        if self.ntricks >= self.bid:  # no longer want tricks
            if not self.lead == 'W' and self.sorted_hand[self.lead]:  # have to follow suit
                options = self.sorted_hand['W'] + self.sorted_hand[self.lead] + self.sorted_hand['N']  # ordered by rank
                i = 0
                while i < len(options) and options[i].index < self.hand[self.high].index:
                    i += 1
                if i == len(options):
                    action = options[-1]
                else:
                    action = np.random.choice(options[i:])
            else:  # can play anything
                action = np.random.choice(self.hand[self.high:])

        else:  # want the trick
            if not self.lead == 'W' and self.sorted_hand[self.lead]:  # have to follow suit
                options = self.sorted_hand['W'] + self.sorted_hand[self.lead] + self.sorted_hand['N']  # ordered by rank
                i = 0
                while i < len(options) and options[i].index < self.hand[self.high].index:
                    i += 1
                if i == 0:
                    action = options[0]
                else:
                    action = np.random.choice(options[:i])
            else:  # can play anything
                if self.high > 0:
                    action = np.random.choice(self.hand[:self.high])
                else:
                    action = self.hand[0]
        try:
            self.sorted_hand[action.suit].remove(action)
            idx = self.hand.index(action)
            self.hand.pop(idx)
            self.ranked_hand = np.delete(self.ranked_hand, idx)
        except:
            print("An exception occurred")
        return action


class WizardAgent(Player):
    def __init__(self, number, hand=[], deck=[]):
        super.__init__(number, hand)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        input_size = 60 + 4 + 16*3
        output_size = 16
        hidden_sizes = [200, 100, 100]
        self.bid_state = np.zeros(input_size)  # hand, position, previous player bids
        for c in self.hand:
            self.bid_state[c.index] = 1
        self.bid_state[self.number + 60] = 1
        self.bid_net = nn.Sequential(
                        nn.Linear(input_size, hidden_sizes[0]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[0], hidden_sizes[1]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[1], hidden_sizes[2]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[2], output_size),
                        nn.ReLU()
                       )

        input_size = (3 * 60) + 4 + (16 * 8) + 6 # cards in hand, play, highest on table, position, bids and tricks of each player
        output_size = 60
        hidden_sizes = [200, 100, 100]
        self.state = np.zeros(input_size)
        self.state[:60] = self.bid_state[:60].copy()
        self.state[60:120] = 1
        self.state[180 + number] = 1
        self.play_net = nn.Sequential(
                        nn.Linear(input_size, hidden_sizes[0]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[0], hidden_sizes[1]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[1], hidden_sizes[2]),
                        nn.ReLU(),
                        nn.Linear(hidden_sizes[2], output_size),
                        nn.ReLU()
                       )

    def bid_policy(self, bids):
        for i, bid in enumerate(bids):
            self.bid_state[60 + 4 + (i*16) + bid] = 1
        bid = np.argmax(self.bid_net(self.bid_state))  # add mask for illegal bids
        return bid

    def play_policy(self):
        return None