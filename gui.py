import tkinter as tk
from tkinter import ttk
import main

class CluedoGUI:
    def __init__(self, cluedo_bot):
        self.cluedo_bot = cluedo_bot
        self.window = tk.Tk()
        self.window.title("Cluedo Bot")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_setup_tab()
        self.create_game_tab()

    def create_setup_tab(self):
        setup_tab = ttk.Frame(self.notebook)
        self.notebook.add(setup_tab, text="Setup")

        # Player Name Entry
        player_name_label = ttk.Label(setup_tab, text="Player Name:")
        player_name_label.pack()
        self.player_name_entry = ttk.Entry(setup_tab)
        self.player_name_entry.pack()

        # Player Cards Entry
        player_cards_label = ttk.Label(setup_tab, text="Player Cards (comma-separated):")
        player_cards_label.pack()
        self.player_cards_entry = ttk.Entry(setup_tab)
        self.player_cards_entry.pack()

        # Other Players Entry
        other_players_label = ttk.Label(setup_tab, text="Other Players (comma-separated):")
        other_players_label.pack()
        self.other_players_entry = ttk.Entry(setup_tab)
        self.other_players_entry.pack()

        # Other Player Card Counts Entry
        card_counts_label = ttk.Label(setup_tab, text="Other Player Card Counts (comma-separated):")
        card_counts_label.pack()
        self.card_counts_entry = ttk.Entry(setup_tab)
        self.card_counts_entry.pack()

        # Start Game Button
        start_button = ttk.Button(setup_tab, text="Start Game", command=self.start_game)
        start_button.pack()

    def create_game_tab(self):
        game_tab = ttk.Frame(self.notebook)
        self.notebook.add(game_tab, text="Game")

        # Player Suggestion Frame
        suggestion_frame = ttk.LabelFrame(game_tab, text="Player Suggestion")
        suggestion_frame.pack(pady=10)

        # Player Dropdown
        player_label = ttk.Label(suggestion_frame, text="Player:")
        player_label.grid(row=0, column=0, padx=5, pady=5)
        self.player_var = tk.StringVar()
        self.player_dropdown = ttk.Combobox(suggestion_frame, textvariable=self.player_var, state="readonly")
        self.player_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Suspect Dropdown
        suspect_label = ttk.Label(suggestion_frame, text="Suspect:")
        suspect_label.grid(row=1, column=0, padx=5, pady=5)
        self.suspect_var = tk.StringVar()
        self.suspect_dropdown = ttk.Combobox(suggestion_frame, textvariable=self.suspect_var, values=self.cluedo_bot.suspects, state="readonly")
        self.suspect_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Weapon Dropdown
        weapon_label = ttk.Label(suggestion_frame, text="Weapon:")
        weapon_label.grid(row=2, column=0, padx=5, pady=5)
        self.weapon_var = tk.StringVar()
        self.weapon_dropdown = ttk.Combobox(suggestion_frame, textvariable=self.weapon_var, values=self.cluedo_bot.weapons, state="readonly")
        self.weapon_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Room Dropdown
        room_label = ttk.Label(suggestion_frame, text="Room:")
        room_label.grid(row=3, column=0, padx=5, pady=5)
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(suggestion_frame, textvariable=self.room_var, values=self.cluedo_bot.rooms, state="readonly")
        self.room_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # Suggestion Buttons
        suggestion_button = ttk.Button(suggestion_frame, text="Make Suggestion", command=self.make_suggestion)
        suggestion_button.grid(row=4, column=0, padx=5, pady=5)
        accusation_button = ttk.Button(suggestion_frame, text="Make Accusation", command=self.make_accusation)
        accusation_button.grid(row=4, column=1, padx=5, pady=5)

        # Showed Card Dropdown
        showed_card_label = ttk.Label(game_tab, text="Player Who Showed Card:")
        showed_card_label.pack()
        self.showed_card_var = tk.StringVar()
        self.showed_card_dropdown = ttk.Combobox(game_tab, textvariable=self.showed_card_var, state="readonly")
        self.showed_card_dropdown.pack()

        # Confirm Showed Card Button
        confirm_button = ttk.Button(game_tab, text="Confirm", command=self.confirm_showed_card)
        confirm_button.pack()

        # Accusation Feedback Label
        self.accusation_feedback_label = ttk.Label(game_tab, text="")
        self.accusation_feedback_label.pack()

        # Bot's Notebook Display
        notebook_frame = ttk.LabelFrame(game_tab, text="Bot's Notebook")
        notebook_frame.pack(pady=10)
        self.notebook_text = tk.Text(notebook_frame, height=10, width=40)
        self.notebook_text.pack()

        # Bot's Suspicion Display
        suspicion_frame = ttk.LabelFrame(game_tab, text="Bot's Suspicion")
        suspicion_frame.pack(pady=10)
        self.suspicion_text = tk.Text(suspicion_frame, height=5, width=40)
        self.suspicion_text.pack()

    def start_game(self):
        player_name = self.player_name_entry.get()
        player_cards = [card.strip() for card in self.player_cards_entry.get().split(',')]
        other_players = [player.strip() for player in self.other_players_entry.get().split(',')]
        card_counts = [int(count.strip()) for count in self.card_counts_entry.get().split(',')]
        player_cards_dict = {player_name: player_cards}
        for player, count in zip(other_players, card_counts):
            player_cards_dict[player] = count
        self.cluedo_bot.initialize_player_cards(player_cards_dict)
        self.player_dropdown['values'] = self.cluedo_bot.get_players()
        self.showed_card_dropdown['values'] = self.cluedo_bot.get_players() + ['No one']
        self.notebook.select(1)  # Switch to the game tab
        self.update_notebook_display()
        self.update_suspicion_display()

    def make_suggestion(self):
        player = self.player_var.get()
        suspect = self.suspect_var.get()
        weapon = self.weapon_var.get()
        room = self.room_var.get()
        suggestion = {'suspects': suspect, 'weapons': weapon, 'rooms': room}
        self.cluedo_bot.update_notebook(suggestion, False)
        self.update_notebook_display()
        self.update_suspicion_display()

    def make_accusation(self):
        player = self.player_var.get()
        suspect = self.suspect_var.get()
        weapon = self.weapon_var.get()
        room = self.room_var.get()
        accusation = {'suspects': suspect, 'weapons': weapon, 'rooms': room}
        result = self.cluedo_bot.make_accusation(accusation)
        if result:
            self.accusation_feedback_label.config(text="Correct accusation! Game over.")
        else:
            self.accusation_feedback_label.config(text="Wrong accusation. Keep playing.")
        self.update_notebook_display()
        self.update_suspicion_display()

    def confirm_showed_card(self):
        player = self.showed_card_var.get()
        if player != 'No one':
            self.cluedo_bot.handle_card_shown(player)
        self.update_notebook_display()
        self.update_suspicion_display()

    def update_notebook_display(self):
        self.notebook_text.delete('1.0', tk.END)
        notebook_text = self.cluedo_bot.get_notebook_text()
        self.notebook_text.insert(tk.END, notebook_text)

    def update_suspicion_display(self):
        self.suspicion_text.delete('1.0', tk.END)
        suspicion_text = self.cluedo_bot.get_suspicion_text()
        self.suspicion_text.insert(tk.END, suspicion_text)

if __name__ == '__main__':
    cluedo_bot = main.CluedoBot()
    gui = CluedoGUI(cluedo_bot)
    gui.window.mainloop()