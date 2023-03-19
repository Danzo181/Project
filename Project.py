import random
import tkinter as tk
import functools as ft
from PIL import ImageTk, Image

class Card():
    suits = {"C": "Clubs", "S": "Spades", "H": "Hearts", "D": "Diamonds"}
    values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 11, "Queen": 12, "King": 13,
              "Ace": 14}

    def __init__(self, name, suit):
        self.name = name
        if suit in self.suits:
            self.suit = suit
        else:
            raise ValueError("Invalid suit")
        self.value = self.values[self.name]

    def __repr__(self):
        return f"{self.name} of {self.suits[self.suit]}"

    def __eq__(self, other):
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
                current_card = Card(value, suit)
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

    def __init__(self, hands_num,player_lst,player_keys, bank_amount=1500):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.hands_num = hands_num
        self.player_lst = player_lst
        self.player_keys = player_keys
        self.bank_amount = bank_amount


        for i in range(self.hands_num):
            hand = []
            for i in range(2):
                hand.append(self.deck.deal_hand())
            self.hands.append(hand)


    def show_hand(self, player_num):
        return self.hands[player_num]


class Game():
    def __init__(self, players, blinds, player_lst, player_keys,parent,chip_count):
        self.table = Table(players,player_lst,player_keys)
        self.blinds = blinds
        self.pot_amount = 0
        self.current_raise = blinds
        self.current_player = 1
        self.passes = 0
        self.dealer = 0
        self.current_player_lst = self.table.player_lst.copy()
        self.current_player_keys = self.table.player_keys.copy()
        self.current_play = 0
        self.current_raise_player = self.dealer + 1
        self.game = game_frame(parent, self.blinds, chip_count, self.table.player_lst,
                            self.table.player_keys)
        self.single_round()


    def change_item(self, player):
        self.table.player_lst[player] = self.current_player_lst[player]

    def money_exchange(self, amount, player_name):
        self.current_player_lst[player_name] -= amount
        self.pot_amount += amount

    def Raise(self, player_num):


        self.game.Raise()
        self.game.parent.wait_variable(self.game.raise_confirm)
        self.current_raise = self.game.raise_amount.get()
        self.current_raise_player = player_num

    def Fold(self, player_num):
        del self.current_player_lst[self.current_player_keys[player_num]]
        self.current_player_keys.pop(player_num)
        self.table.hands.pop(player_num)

        if self.current_player <= self.current_raise_player:
            self.current_raise_player -= 1
        self.current_player -= 1

    def All_in(self, player_num):
        self.current_raise= self.current_player_lst[self.current_player_keys[player_num]]
        self.current_raise_player = player_num

    def betting(self,play):


        if play == "r":
            self.Raise(self.current_player)
        elif play == "f":
            self.Fold(self.current_player)
        elif play =="a":
            self.All_in(self.current_player)
        elif play == "c":
            pass
        else:
            raise ValueError("Invalid input")

    def end_round(self):

        self.dealer += 1
        if self.dealer + 1 <= len(self.table.player_lst):
            self.dealer += 1
        else:
            self.dealer = 0

        print(f"The dealer is now {self.dealer}")

    def round(self):

        while self.current_player != self.current_raise_player or self.passes <= 0:
            print(self.current_player)
            print(self.current_raise_player)
            print(self.passes)
            print(self.current_player_lst)
            print(self.table.show_hand(self.current_player))
            print(self.table.deck.table_hand)

            self.game.update_current_player(self.current_player,self.table.hands[self.current_player],self.current_player_lst,self.current_player_keys)

            self.game.parent.wait_variable(self.game.action)

            self.betting(self.game.action.get())

            self.current_player += 1

            if self.current_player + 1 > len(self.current_player_lst):
                self.current_player = 0
                self.passes += 1

            if len(self.current_player_lst) <= 1:
                break

        for i in self.current_player_lst:
            self.money_exchange(self.current_raise, i)
            self.change_item(i)

        self.game.update_players(self.pot_amount)

        print(self.table.player_lst)

        self.current_play += 1
        if self.current_play > 0:
            self.blinds = 0

        self.current_raise = 0
        if self.dealer + 1 <= len(self.current_player_lst):
            self.current_raise_player = self.dealer + 1
            self.current_player = self.dealer + 1
        else:
            self.current_raise_player = 0
            self.current_player = 0

        self.passes = 0


    def single_round(self):
        while len(self.current_player_lst) > 1:

            if self.current_play == 0:
                self.round()
            elif self.current_play == 1:
                self.table.deck.deal_flop()
                self.game.deal_flop(self.table.deck.table_hand)
                self.round()
            elif self.current_play == 2:
                self.table.deck.deal_turn()
                self.game.deal_turn(self.table.deck.table_hand)
                self.round()
            elif self.current_play == 3:
                self.table.deck.deal_river()
                self.game.deal_river(self.table.deck.table_hand)
                self.round()

        self.end_round()




class setup_frame:


    def __init__(self, parent):

        self.parent = parent
        self.setup_frame = tk.Frame(self.parent, bg="#385c89")
        self.setup_frame.grid(row=0, column=0, sticky="news")

        self.num_players = tk.IntVar(self.setup_frame)
        self.current = 1
        self.player_name = tk.StringVar(self.setup_frame,"")
        self.chip_count = tk.IntVar(self.setup_frame)
        self.blind_amount = tk.IntVar(self.setup_frame)
        self.player_lst = []
        self.player_dict = {}

        self.parent.rowconfigure(0,weight = 1)
        self.parent.columnconfigure(0, weight = 1)

        self.bg_label = tk.Label(self.setup_frame, relief=tk.SUNKEN, bg="#cccccc")
        self.bg_label.grid(row=0, column=10, sticky="news", columnspan=10, rowspan=20)
        self.title_label = tk.Label(self.setup_frame,text = "Poker room - setup",bg = "#ef7359")
        self.title_label.grid(row = 0,column = 10,sticky = "news",columnspan = 10,rowspan = 2)

        self.num_players_label = tk.Label(self.setup_frame, text="Num of players:")
        self.num_players_label.grid(row=1, column=2, columnspan=2)
        self.num_players_entry = tk.Entry(self.setup_frame, textvariable = self.num_players)
        self.num_players_entry.grid(row=1, column=5, columnspan=2)
        self.num_players_confirm = tk.Button(self.setup_frame, text="confirm", command=self.num_players_setup)
        self.num_players_confirm.grid(row=1, column=7)

        self.chip_count_label = tk.Label(self.setup_frame,text = "Chip count")
        self.chip_count_label.grid(row=5, column=2, columnspan=2)
        self.chip_count_entry = tk.Entry(self.setup_frame,textvariable = self.chip_count)
        self.chip_count_entry.grid(row=5, column=5, columnspan=2)
        self.chip_count_button = tk.Button(self.setup_frame,text = "confirm",command = self.add_chip_counts)
        self.chip_count_button.grid(row=5, column=7)

        self.blind_count_label = tk.Label(self.setup_frame, text="Blind amount:")
        self.blind_count_label.grid(row=9, column=2, columnspan=2)
        self.blind_count_entry = tk.Entry(self.setup_frame, textvariable=self.blind_amount)
        self.blind_count_entry.grid(row=9, column=5, columnspan=2)
        self.blind_count_button = tk.Button(self.setup_frame, text="confirm", command=self.add_blind_amount)
        self.blind_count_button.grid(row=9, column=7)
        self.blind_label_title = tk.Label(self.setup_frame, text="Blind amounts:", bg="#ef7359")
        self.blind_label_title.grid(row=3, column=11, columnspan=3,sticky = "news")

        self.go_to_game_frame_button = tk.Button(self.setup_frame, text ="play", bg ="#ef7359", command = self.go_to_game_frame)
        self.go_to_game_frame_button.grid(row = 19,column = 8,rowspan = 2,columnspan = 2,sticky = "news")





        for i in range(0, 20):
            self.setup_frame.rowconfigure(i, weight=1)
            self.setup_frame.columnconfigure(i, weight=1)

    def num_players_setup(self):
        self.player_name = ""
        player_name_entry = tk.Entry(self.setup_frame, textvariable=self.player_name)
        player_name_entry.grid(row=3, column=5, columnspan=2)
        player_name_confirm = tk.Button(self.setup_frame, text="confirm",command=ft.partial(self.player_name_fn, self.current, player_name_entry))
        player_name_confirm.grid(row=3, column=7)

    def player_name_fn(self, i,entry):
        print(f"You pressed button {i} and the name was {entry.get()}")
        name = entry.get()
        self.player_lst.append(name)
        if i % 2 == 0:
            column = 15
        else:
            column = 10

        if i <= 2:
            row = 5
        elif i <= 4:
            row = 9
        elif i <= 6:
            row = 13
        elif i <= 8:
            row = 17

        player_label = tk.Label(self.setup_frame, relief=tk.RAISED, bg="#ef7359")
        player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=4)
        player_name_title = tk.Label(self.setup_frame, text = "Name:",bg = "#ef7359")
        player_name_title.grid(row = row,column = column)
        player_name = tk.Label(self.setup_frame, text=name, bg = "#ef7359")
        player_name.grid(row=row, column=column+2)

        self.current += 1

        if self.current <= self.num_players.get():
            self.num_players_setup()


    def add_chip_counts(self):
        for i in range(self.current):
            if i % 2 == 0:
                column = 15
            else:
                column = 10

            if i <= 2:
                row = 6
            elif i <= 4:
                row = 10
            elif i <= 6:
                row = 14
            elif i <= 8:
                row = 18


            chip_title = tk.Label(self.setup_frame,text = "Chip count:",bg = "#ef7359")
            chip_title.grid(row = row,column = column)
            chip_label = tk.Label(self.setup_frame, text=self.chip_count.get(),bg = "#ef7359")
            chip_label.grid(row=row, column=column+1)

    def add_blind_amount(self):
        blind_label = tk.Label(self.setup_frame,text = f"{self.blind_amount.get()}/{self.blind_amount.get()*2}",bg = "#ef7359")
        blind_label.grid(row = 3,column = 15,columnspan = 3,sticky = "news")


    def go_to_game_frame(self):

        for i in self.player_lst:
            self.player_dict[i] = int(self.chip_count.get())
        self.player_keys = list(self.player_dict.keys())
        print(self.player_keys,self.player_dict)


        game = Game(self.num_players.get(), self.blind_amount.get(), self.player_dict, self.player_keys, self.parent,self.chip_count)

        self.setup_frame.destroy()


class game_frame:
    def __init__(self, parent, blind_amount,chip_count,player_lst,player_keys):

        self.parent = parent

        self.blind_amount = blind_amount
        self.chip_count = chip_count
        self.player_lst = player_lst
        self.player_keys = player_keys
        self.betting_complete = False
        self.action = tk.StringVar()
        self.raise_amount = tk.IntVar()
        self.raise_confirm = tk.IntVar()

        self.game_frame = tk.Frame(self.parent, bg="#385c89")
        self.game_frame.grid(row=0, column=0, sticky="news")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.bg = tk.Label(self.game_frame,bg = "#385c89")
        self.bg.grid(row = 0, column = 0, rowspan = 20, columnspan = 20,sticky = "news")

        self.community_cards_bg = tk.Label(self.game_frame,  relief=tk.SUNKEN, bg="#cccccc")
        self.community_cards_bg.grid(row = 0,column = 0,rowspan = 5,columnspan=20,sticky = "news")
        self.community_cards_header = tk.Label(self.game_frame,text = "Community cards:",bg = "#ef7359")
        self.community_cards_header.grid(row = 0,column = 0,rowspan = 2,columnspan = 4,sticky = "news")

        community = ImageTk.PhotoImage(Image.open(str("cards\default1.png")).resize((90, 140), Image.Resampling.LANCZOS))
        self.community_card0 = tk.Label(self.game_frame, image = community,bg = "#cccccc")
        self.community_card0.image = community
        self.community_card0.grid(row = 1,column = 5,sticky = "news",rowspan = 3,columnspan = 2)
        self.community_card1 = tk.Label(self.game_frame, image=community, bg="#cccccc")
        self.community_card1.image = community
        self.community_card1.grid(row=1, column=8,sticky="news", rowspan=3, columnspan=2)
        self.community_card2 = tk.Label(self.game_frame, image=community, bg="#cccccc")
        self.community_card2.image = community
        self.community_card2.grid(row=1, column=11, sticky="news", rowspan=3, columnspan=2)
        self.community_card3 = tk.Label(self.game_frame, image=community, bg="#cccccc")
        self.community_card3.image = community
        self.community_card3.grid(row=1, column=14, sticky="news", rowspan=3, columnspan=2)
        self.community_card4 = tk.Label(self.game_frame, image=community, bg="#cccccc")
        self.community_card4.image = community
        self.community_card4.grid(row=1, column=17, sticky="news", rowspan=3, columnspan=2)

        self.blind_title = tk.Label(self.game_frame,text=f"Blinds: {self.blind_amount}/{self.blind_amount*2}",bg="#ef7359")
        self.blind_title.grid(row =3,column =0,rowspan=2,columnspan=4,sticky="news")

        self.action_bg_label = tk.Label(self.game_frame,bg = "#cccccc")
        self.action_bg_label.grid(row = 6, column = 13, rowspan = 5, columnspan = 6,sticky = "news")
        self.action_title = tk.Label(self.game_frame,text="Actions:",bg = "#ef7359")
        self.action_title.grid(row =5,column=14,rowspan=1,columnspan=3,sticky="news")
        self.check_btn = tk.Button(self.game_frame,text="Check",bg="#a9a9a9",command = lambda: self.action.set("c"))
        self.check_btn.grid(row=6,column=14,columnspan=2,sticky="news")
        self.fold_btn = tk.Button(self.game_frame, text="Fold", bg="#a9a9a9",command = lambda: self.action.set("f"))
        self.fold_btn.grid(row=8, column=14, columnspan=2, sticky="news")
        self.raise_btn = tk.Button(self.game_frame, text="Raise", bg="#a9a9a9",command = lambda: self.action.set("r"))
        self.raise_btn.grid(row=10, column=14, columnspan=2, sticky="news")
        self.call_btn = tk.Button(self.game_frame, text="Call", bg="#a9a9a9",command = lambda: self.action.set("c"))
        self.call_btn.grid(row=7, column=17, columnspan=2, sticky="news")
        self.all_in_btn = tk.Button(self.game_frame,text="All in",bg="#a9a9a9",command = lambda: self.action.set("a"))
        self.all_in_btn.grid(row=9,column=17,columnspan=2,sticky="news")

        self.current_player_title = tk.Label(self.game_frame,text="Current player:",bg="#ef7359")
        self.current_player_title.grid(row = 5,column=1,columnspan=2,sticky = "news")

        for i in range(len(self.player_lst)+1):
            if i % 2 == 0:
                row = 16
            else:
                row = 12

            if i <= 2:
                column = 0
            elif i <= 4:
                column = 5
            elif i <= 6:
                column = 10
            elif i <= 8:
                column = 15

            self.player_label = tk.Label(self.game_frame, relief=tk.RAISED, bg="#ef7359")
            self.player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=4)
            self.player_name_title = tk.Label(self.game_frame, text="Name:", bg="#ef7359")
            self.player_name_title.grid(row=row, column=column)
            self.player_name = tk.Label(self.game_frame, text=f"{self.player_keys[i-1]}", bg="#ef7359")
            self.player_name.grid(row=row, column=column + 2)
            self.player_chip_count_title = tk.Label(self.game_frame,text="Chip count:",bg="#ef7359")
            self.player_chip_count_title.grid(row=row+2,column = column)
            self.player_chip_count = tk.Label(self.game_frame,text=f"{self.player_lst[self.player_keys[i-1]]}",bg="#ef7359")
            self.player_chip_count.grid(row=row+2,column=column+2)



        for i in range(0, 20):
            self.game_frame.rowconfigure(i, weight=1,minsize = 45)
            self.game_frame.columnconfigure(i, weight=1,minsize = 30)


    def Raise(self):
        raise_entry_box = tk.Entry(self.game_frame,textvariable=self.raise_amount)
        raise_entry_box.grid(row = 11,column = 14,sticky = "news")
        raise_entry_confirm = tk.Button(self.game_frame,text = "Confirm",bg="#a9a9a9",command=lambda: self.raise_confirm.set(1))
        raise_entry_confirm.grid(row = 11,column = 15,sticky = "news")



    def deal_flop(self,cards):
        card0 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[0]}.png")).resize((90, 140), Image.Resampling.LANCZOS))
        card1 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[1]}.png")).resize((90, 140), Image.Resampling.LANCZOS))
        card2 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[2]}.png")).resize((90, 140), Image.Resampling.LANCZOS))

        self.community_card0 = tk.Label(self.game_frame, image=card0, bg="#cccccc")
        self.community_card0.image = card0
        self.community_card0.grid(row=1, column=5, sticky="news", rowspan=3, columnspan=2)
        self.community_card1 = tk.Label(self.game_frame, image=card1, bg="#cccccc")
        self.community_card1.image = card1
        self.community_card1.grid(row=1, column=8, sticky="news", rowspan=3, columnspan=2)
        self.community_card2 = tk.Label(self.game_frame, image=card2, bg="#cccccc")
        self.community_card2.image = card2
        self.community_card2.grid(row=1, column=11, sticky="news", rowspan=3, columnspan=2)

    def deal_turn(self,cards):
        card3 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[3]}.png")).resize((90, 140), Image.Resampling.LANCZOS))

        self.community_card4 = tk.Label(self.game_frame, image=card3, bg="#cccccc")
        self.community_card4.image = card3
        self.community_card4.grid(row=1, column=14, sticky="news", rowspan=3, columnspan=2)

    def deal_river(self,cards):
        card4 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[4]}.png")).resize((90, 140), Image.Resampling.LANCZOS))

        self.community_card5 = tk.Label(self.game_frame, image=card4, bg="#cccccc")
        self.community_card5.image = card4
        self.community_card5.grid(row=1, column=17, sticky="news", rowspan=3, columnspan=2)

    def update_players(self,pot_amount):

        self.pot_amount_title = tk.Label(self.game_frame, text=f"Pot amount: {pot_amount}",bg = "#ef7359")
        self.pot_amount_title.grid(row = 6,column=10,sticky="news")

        for i in range(len(self.player_lst) + 1):
            if i % 2 == 0:
                row = 16
            else:
                row = 12

            if i <= 2:
                column = 0
            elif i <= 4:
                column = 5
            elif i <= 6:
                column = 10
            elif i <= 8:
                column = 15

            player_label = tk.Label(self.game_frame, relief=tk.RAISED, bg="#ef7359")
            player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=3)
            player_name_title = tk.Label(self.game_frame, text="Name:", bg="#ef7359")
            player_name_title.grid(row=row, column=column)
            player_name = tk.Label(self.game_frame, text=f"{self.player_keys[i - 1]}", bg="#ef7359")
            player_name.grid(row=row, column=column + 2)
            player_chip_count_title = tk.Label(self.game_frame, text="Chip count:", bg="#ef7359")
            player_chip_count_title.grid(row=row + 2, column=column)
            player_chip_count = tk.Label(self.game_frame, text=f"{self.player_lst[self.player_keys[i - 1]]}",bg="#ef7359")
            player_chip_count.grid(row=row + 2, column=column + 2)


    def update_current_player(self,player,cards,current_lst,current_keys):

        current_player_bg = tk.Label(self.game_frame,relief=tk.RAISED,bg="#cccccc")
        current_player_bg.grid(row=6,column=1,columnspan=9,rowspan=5,sticky="news")
        current_player_title = tk.Label(self.game_frame,text="Name:",bg="#ef7359")
        current_player_title.grid(row=7,column=2,sticky="news")
        current_player_name = tk.Label(self.game_frame,text=f"{current_keys[player]}",bg="#ef7359")
        current_player_name.grid(row=7,column=3,sticky="news")
        current_player_chip_count_title = tk.Label(self.game_frame,text="Chip count:",bg="#ef7359")
        current_player_chip_count_title.grid(row=9,column=2,sticky="news")
        current_player_chip_count= tk.Label(self.game_frame,text=f"{current_lst[current_keys[player]]}",bg="#ef7359")
        current_player_chip_count.grid(row=9,column=3,sticky="news")

        card1 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[0]}.png")).resize((90, 140), Image.Resampling.LANCZOS))
        card2 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[1]}.png")).resize((90, 140), Image.Resampling.LANCZOS))


        current_card1 = tk.Label(self.game_frame, image=card1, bg="#cccccc")
        current_card1.image = card1
        current_card1.grid(row=7, column=5, sticky="news", rowspan=3, columnspan=2)
        current_card2 = tk.Label(self.game_frame, image=card2, bg="#cccccc")
        current_card2.image = card2
        current_card2.grid(row=7, column=7, sticky="news", rowspan=3, columnspan=2)


def setup():
    root = tk.Tk()
    root.geometry("1000x1000")
    frame1 = setup_frame(root)
    root.mainloop()

setup()