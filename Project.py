import random

class Card():

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
        return f"Card: {self.name} of {self.suits[self.suit]} "

    def same_suit(self, other):
        return self.suit == other.suit

    def __eq__(self,other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

class Deck():
    def __init__(self):
        self.deck = []
        for suit in Card.suits:
            for value in Card.values:
                current_card= Card(value,suit)
                self.deck.append(current_card)

    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_hand(self):
        return self.deck.pop(0)

class Table():
    def __init__(self,hands_num):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.hands_num = hands_num
        self.player_lst = []

        for i in range(hands_num):
            hand =[]
            for i in range(2):
                hand.append(self.deck.deal_hand())
            self.hands.append(hand)
        print(self.hands)

    def players_assign(self):
        for i in range(self.hands_num):
            p_name = input("enter player name: ")
            self.player_lst.append(p_name)
        return self.player_lst






class Player():
    def __init__(self,name,bank=1500):
        self.name = name
        self.bank = bank

    def hand(self):
        self.hand = []



tab = Table(3)
#card_KH = Card("K","H")
#card_2S = Card("2","S")
#deck = Deck()
