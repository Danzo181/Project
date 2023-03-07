import tkinter as tk
import functools as ft
from PIL import ImageTk, Image


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
        print(self.player_keys)

        frame2 = game_frame(self.parent,self.blind_amount.get(),self.chip_count.get(),self.player_dict,self.player_keys)
        self.setup_frame.destroy()


class game_frame:
    def __init__(self, parent, blind_amount,chip_count,player_lst,player_keys):

        self.parent = parent

        self.blind_amount = blind_amount
        self.chip_count = chip_count
        self.player_lst = player_lst
        self.player_keys = player_keys

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
        self.check_btn = tk.Button(self.game_frame,text="Check",bg="#a9a9a9")
        self.check_btn.grid(row=6,column=14,columnspan=2,sticky="news")
        self.fold_btn = tk.Button(self.game_frame, text="Fold", bg="#a9a9a9")
        self.fold_btn.grid(row=8, column=14, columnspan=2, sticky="news")
        self.raise_btn = tk.Button(self.game_frame, text="raise", bg="#a9a9a9")
        self.raise_btn.grid(row=10, column=14, columnspan=2, sticky="news")
        self.call_btn = tk.Button(self.game_frame, text="call", bg="#a9a9a9")
        self.call_btn.grid(row=7, column=17, columnspan=2, sticky="news")
        self.all_in_btn = tk.Button(self.game_frame,text="All in",bg="#a9a9a9")
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

    def update_players(self):

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
            player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=4)
            player_name_title = tk.Label(self.game_frame, text="Name:", bg="#ef7359")
            player_name_title.grid(row=row, column=column)
            player_name = tk.Label(self.game_frame, text=f"{self.player_keys[i - 1]}", bg="#ef7359")
            player_name.grid(row=row, column=column + 2)
            player_chip_count_title = tk.Label(self.game_frame, text="Chip count:", bg="#ef7359")
            player_chip_count_title.grid(row=row + 2, column=column)
            player_chip_count = tk.Label(self.game_frame, text=f"{self.player_lst[self.player_keys[i - 1]]}",bg="#ef7359")
            player_chip_count.grid(row=row + 2, column=column + 2)

    def update_current_player(self,player,cards):
        current_player_bg = tk.Label(self.game_frame,relief=tk.RAISED,bg="#cccccc")
        current_player_bg.grid(row=6,column=1,columnspan=9,rowspan=5,sticky="news")
        current_player_title = tk.Label(self.game_frame,text="Name:",bg="#ef7359")
        current_player_title.grid(row=7,column=2,sticky="news")
        current_player_name = tk.Label(self.game_frame,text=f"{self.player_keys[player]}",bg="#ef7359")
        current_player_name.grid(row=7,column=3,sticky="news")
        current_player_chip_count_title = tk.Label(self.game_frame,text="Chip count:",bg="#ef7359")
        current_player_chip_count_title.grid(row=9,column=2,sticky="news")
        current_player_chip_count= tk.Label(self.game_frame,text=f"{self.player_lst[self.player_keys[player]]}",bg="#ef7359")
        current_player_chip_count.grid(row=9,column=3,sticky="news")

        card1 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[0]}.png")).resize((90, 140), Image.Resampling.LANCZOS))
        card2 = ImageTk.PhotoImage(Image.open(str(f"cards\{cards[1]}.png")).resize((90, 140), Image.Resampling.LANCZOS))


        current_card1 = tk.Label(self.game_frame, image=card1, bg="#cccccc")
        current_card1.image = card1
        current_card1.grid(row=7, column=5, sticky="news", rowspan=3, columnspan=2)
        current_card2 = tk.Label(self.game_frame, image=card2, bg="#cccccc")
        current_card2.image = card2
        current_card2.grid(row=7, column=7, sticky="news", rowspan=3, columnspan=2)



def main():
    root = tk.Tk()
    root.geometry("1000x1000")
    #frame1 = setup_frame(root)
    frame2 = game_frame(root,10,1500,{"dan":1500,"seb":1500,"sean":1500,"zack":1500,"joe":1500,"tal":1500,"jack":1500,"jas":1500},["dan","seb","sean","zack","joe","tal","jack","jas"])
    frame2.deal_flop(["Ace of Clubs","Ace of Diamonds","Ace of Hearts"])
    frame2.update_current_player(0,["King of Clubs","King of Diamonds"])
    root.mainloop()

main()