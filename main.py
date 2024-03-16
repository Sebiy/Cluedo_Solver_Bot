import random

class CluedoBot:
    def __init__(self, suspects=None, weapons=None, rooms=None):
        self.suspects = suspects or ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
        self.weapons = weapons or ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        self.rooms = rooms or ["Hall", "Lounge", "Dining Room", "Kitchen", "Ballroom", "Conservatory", "Billiard Room", "Library", "Study"]
        self.notebook = {
            'suspects': {suspect: True for suspect in self.suspects},
            'weapons': {weapon: True for weapon in self.weapons},
            'rooms': {room: True for room in self.rooms}
        }
        self.player_cards = {}

    def update_notebook(self, suggestion, showed_card):
        if not showed_card:
            for key in suggestion:
                self.notebook[key][suggestion[key]] = False

    def make_accusation(self, accusation=None):
        if accusation:
            return accusation
        else:
            accusation = {}
            for key in self.notebook:
                for item, value in self.notebook[key].items():
                    if value:
                        accusation[key] = item
                        break
            return accusation

    def handle_player_accusation(self, accuser, accusation, correct):
        if correct:
            print(f"{accuser} made a correct accusation!")
        else:
            print(f"{accuser} made an incorrect accusation.")
            for key in accusation:
                self.notebook[key][accusation[key]] = False

    def update_player_cards(self, player, num_cards):
        self.player_cards[player] = num_cards

    def get_players(self):
        return list(self.player_cards.keys())

    def get_player_card_count(self, player):
        return self.player_cards[player]

    def reset_notebook(self):
        for key in self.notebook:
            for item in self.notebook[key]:
                self.notebook[key][item] = True

    def initialize_player_cards(self, player_cards):
        self.player_cards = player_cards

    def handle_card_shown(self, player):
        if player != 'No one':
            num_cards = self.player_cards[player]
            self.player_cards[player] = num_cards - 1

    def get_notebook_text(self):
        notebook_text = ""
        for key in self.notebook:
            notebook_text += f"{key.capitalize()}:\n"
            for item, value in self.notebook[key].items():
                notebook_text += f"  {item}: {'Possible' if value else 'Eliminated'}\n"
        return notebook_text

    def get_suspicion_text(self):
        suspicion = self.make_accusation()
        suspicion_text = "Bot's Suspicion:\n"
        for key, value in suspicion.items():
            suspicion_text += f"{key.capitalize()}: {value}\n"
        return suspicion_text


