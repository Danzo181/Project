import tkinter as tk
import functools as ft


class setup_frame:


    def __init__(self, parent):

        self.setup_frame = tk.Frame(parent, bg="#830da3")
        self.setup_frame.grid(row=0, column=0, sticky="news")

        self.num_players = tk.StringVar(self.setup_frame,"")
        self.current = 1
        self.player_name = tk.StringVar(self.setup_frame,"")
        self.chip_count = ""

        parent.rowconfigure(0,weight = 1)
        parent.columnconfigure(0, weight = 1)

        self.bg_label = tk.Label(self.setup_frame, relief=tk.SUNKEN, bg="light grey")
        self.bg_label.grid(row=0, column=10, sticky="news", columnspan=10, rowspan=20)

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

        player_label = tk.Label(self.setup_frame, relief=tk.RAISED, bg="light blue")
        player_label.grid(row=row, column=column, sticky="news", columnspan=5, rowspan=4)
        player_name = tk.Label(self.setup_frame, text=name)
        player_name.grid(row=row, column=column, rowspan=2)

        self.current += 1

        if self.current <= int(self.num_players.get()):
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

            chip_label = tk.Label(self.setup_frame, text=self.chip_count)
            chip_label.grid(row=row, column=column, rowspan=2)








def main():
    root = tk.Tk()
    root.geometry("900x800")
    frame1 = setup_frame(root)
    root.mainloop()

main()