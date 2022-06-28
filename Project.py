class card():

    suits = {"C": "Clubs", "S": "Spades", "H": "Hearts", "D": "Diamonds"}
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13,
              "A": 14}

    def __init__(self, name, suit, value=None):
        self.name = name
        if suit in self.suits:
            self.suit = suit
        else:
            raise ValueError("Invalid suit")
        self.value = self.values[self.name]

    def __repr__(self):
        return f"Card: {self.name} of {self.suits[self.suit]} with value of {self.value}"

    def same_suit(self, other):
        return self.suit == other.suit

    def __lt__(self, other):
        return self.value < other.value


card_KH = card("K","H")
card_2S = card("2","S")
print(card_2S)