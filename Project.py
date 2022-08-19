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
        self.player_keys = []
        self.bank_amount = bank_amount


        for i in range(hands_num):
            hand =[]
            for i in range(2):
                hand.append(self.deck.deal_hand())
            self.hands.append(hand)


        for i in range(self.hands_num):
            p_name = input("enter player name: ")
            self.player_lst[p_name] = self.bank_amount

        self.player_keys = list(self.player_lst.keys())

    def show_hand(self, player_num):
        return self.hands[player_num]

class Game():
    def __init__(self,players = 5, rounds = 5,blinds = 20):
        self.table = Table(players)
        self.num_rounds = rounds
        self.blinds = blinds
        self.pot_amount = 0
        self.current_raise = 0
        self.current_player = 0
        self.current_player_lst = self.table.player_lst.copy()
        self.current_player_keys = self.table.player_keys.copy()
        self.current_play = 0
        self.current_raise_player = len(self.current_player_lst) + 1

    def change_item(self,player):
        self.table.player_lst[player] = self.current_player_lst[player]

    def money_exchange(self,amount,player_name):
        self.current_player_lst[player_name] -= amount
        self.pot_amount += amount


    def Raise(self, player_num):

        self.current_raise = int(input("Enter amount to raise by: "))
        self.current_raise_player = player_num

    def Fold(self,player_num):
        del self.current_player_lst[self.current_player_keys[player_num]]
        self.current_player_keys.pop(player_num)
        self.table.hands.pop(player_num)
        self.current_player -= 1

    def betting(self):

        play = input("Enter play c/r/f: ")

        if play == "r":
            self.Raise(self.current_player)
        elif play == "f":
            self.Fold(self.current_player)
        elif play == "c":
            pass
        else:
            raise ValueError("Invalid input")



def round(current_game):


    while current_game.current_raise_player != current_game.current_player:

        print(current_game.table.show_hand(current_game.current_player))
        print(current_game.table.deck.table_hand)

        current_game.betting()
        current_game.current_player += 1

        if current_game.current_player + 1 > len(current_game.current_player_lst):
            current_game.current_player = 0

    if current_game.current_play == 0:


    for i in current_game.current_player_lst:
        current_game.money_exchange(current_game.current_raise,i)
        current_game.change_item(i)

    print(current_game.table.player_lst)


    current_game.current_raise = 0
    current_game.current_raise_player = len(current_game.current_player_lst)
    current_game.current_player = 0
    current_game.blinds = 0

def main():
    num_players = int(input("players: "))

    current_game = Game(num_players)

    round(current_game)

    current_game.table.deck.deal_flop()

    round(current_game)

    current_game.table.deck.deal_turn()

    round(current_game)

    current_game.table.deck.deal_river()

    round(current_game)

#Game(1)
main()


#tab = Table(3)
#card_KH = Card("K","H")
#card_2S = Card("2","S")
#deck = Deck