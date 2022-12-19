import tkinter as tk
import functools as ft


class setup_frame:


    def __init__(self, parent):

        self.setup_frame = tk.Frame(parent, bg="#830da3")
        self.setup_frame.grid(row=0, column=0, sticky="news")

        self.num_players = tk.StringVar(self.setup_frame,"")
        self.player_name = tk.StringVar(self.setup_frame,"")
        self.player_name_2 = tk.StringVar(self.setup_frame, "")
        self.player_name_3 = tk.StringVar(self.setup_frame, "")
        self.player_name_4 = tk.StringVar(self.setup_frame, "")
        self.player_name_5 = tk.StringVar(self.setup_frame, "")
        self.player_name_6 = tk.StringVar(self.setup_frame, "")
        self.player_name_7 = tk.StringVar(self.setup_frame, "")
        self.player_name_8 = tk.StringVar(self.setup_frame, "")


        parent.rowconfigure(0,weight = 1)
        parent.columnconfigure(0, weight = 1)

        self.bg_label = tk.Label(self.setup_frame, relief=tk.SUNKEN, bg="light grey")
        self.bg_label.grid(row=1, column=10, sticky="news", columnspan=10, rowspan=20)

        self.num_players_label = tk.Label(self.setup_frame, text="Num of players:")
        self.num_players_label.grid(row=2, column=2, columnspan=2)
        self.num_players_entry = tk.Entry(self.setup_frame, textvariable = self.num_players)
        self.num_players_entry.grid(row=2, column=5, columnspan=2)
        self.num_players_confirm = tk.Button(self.setup_frame, text="confirm", command=self.num_players_setup)
        self.num_players_confirm.grid(row=2, column=7)

        for i in range(1, 20):
            self.setup_frame.rowconfigure(i, weight=1)
            self.setup_frame.columnconfigure(i, weight=1)

    def num_players_setup(self):
        num = int(self.num_players_entry.get())

        for i in range(1, num + 1):

            player_label = tk.Label(self.setup_frame, relief=tk.RAISED, bg="light blue")
            player_name = tk.Label(self.setup_frame, text=self.player_name.get())

            player_name_label = tk.Label(self.setup_frame, text=f"Player {i} name:")
            player_name_label.grid(row=2 + i, column=2, columnspan=2)
            player_name_entry = tk.Entry(self.setup_frame, textvariable=self.player_name)
            player_name_entry.grid(row=2 + i, column=5, columnspan=2)
            player_name_confirm = tk.Button(self.setup_frame, text="confirm", command=ft.partial(self.player_name_fn,i, player_name_entry))
            player_name_confirm.grid(row=2 + i, column=7)

            if i % 2 == 0:
                column = 15
            else:
                column = 10

            if i <= 2:
                row = 5
            elif i <= 4:
                row = 8
            elif i <= 6:
                row = 12
            elif i <= 8:
                row = 16

            player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=4)
            player_name.grid(row=row, column=column, rowspan=2)

    def player_name_fn(self, i,entry_box):
        print(f"You pressed button {i} and the name was {entry_box.get()}")







def main():
    root = tk.Tk()
    root.geometry("900x800")
    frame1 = setup_frame(root)
    root.mainloop()

main()