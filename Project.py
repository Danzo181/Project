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

    def __eq__(self,other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

class Deck():
    def __init__(self):
        self.deck = []
        self.table_hand = []
        for suit in Card.suits:
            for value in Card.values:
                current_card= Card(value,suit)
                self.deck.append(current_card)

    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_hand(self):
        return self.deck.pop(0)

    def deal_flop(self):
        for i in range(3):
            self.table_hand.append(self.deck.pop(0))
        return self.table_hand

    def deal_turn(self):
        self.table_hand.append(self.deck.pop(0))
        return self.table_hand

    def deal_river(self):
        self.table_hand.append(self.deck.pop(0))
        return self.table_hand

class Table():
    def __init__(self,hands_num,bank_amount=1500):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.hands_num = hands_num
        self.player_lst = {}
        self.bank_amount = bank_amount

        for i in range(hands_num):
            hand =[]
            for i in range(2):
                hand.append(self.deck.deal_hand())
            self.hands.append(hand)
        print(self.hands)

    def players_assign(self):
        for i in range(self.hands_num):
            p_name = input("enter player name: ")
            self.player_lst[p_name] = self.bank_amount
        return self.player_lst


class Game():
    def __init__(self,rounds,blinds = 20):
        self.table = Table(5)
        self.num_rounds = rounds
        self.blinds = blinds
        self.pot_amount = 0
        self.current_raise = 0
        self.current_player = 0

    def Check(self,player_name):
        self.table.player_lst[player_name] -= self.blinds
        self.pot_amount += self.blinds
        return "check"

    def Raise(self,player_name):
        self.current_raise = input("Enter amount to raise by: ")
        self.table.player_lst[player_name] -= self.current_raise
        self.pot_amount += self.current_raise

    def Fold(self):
        return "Fold"

    def betting(self):
        for i in range(len(self.table.player_lst)):
            play = input("Enter play c/r/f: ")
            if play == "c":
                self.Check(self.table.player_lst[self.current_player])
            elif play == "r":
                self.Raise(self.table.player_lst[self.current_player])
            elif play == "f":
                self.Fold()
            else:
                raise ValueError("Invalid input")


tab = Table(3)
#card_KH = Card("K","H")
#card_2S = Card("2","S")
#deck = Deck()