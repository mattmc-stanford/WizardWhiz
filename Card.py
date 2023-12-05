class Card:
    def __init__(self, name, value, index):
        self.name = name
        self.value = value
        self.suit = name[1]
        self.index = index
