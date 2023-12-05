import torch
import torch.nn as nn

class BidNet(nn.Module):
    def __init__(self, input_size, hidden_sizes, num_actions):
        super(NeuralNet, self).__init__()
        self.layers = [None] * len(hidden_sizes) + 2
        self.layers[0] = nn.Linear(input_size, hidden_sizes[0])
        for l in range(len(hidden_sizes)-1):
                self.layers[l+1] = nn.Linear(hidden_sizes[l], hidden_sizes[l+1])
        self.layers[-1] = nn.Linear(hidden_sizes[-1], num_actions)

