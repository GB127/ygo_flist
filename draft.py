from random import shuffle

def pooler(amount):
    with open("cards_list.txt", "r") as file:
        all_cartes = file.read().split("\n")
    shuffle(all_cartes)
    return all_cartes[:amount]
class yugioh_modes:
    players = ["Guylain", "Maxime"]
    def __init__(self, player):
        self.player_turn = 1
        self.player = player
        self.Guylain = []
        self.Maxime = []

    def __getitem__(self, name):
        return self.__dict__[name]


class Draft_manager:
    def __init__(self, cards, player):
        super().__init__(player)
        self.all_cards = cards
        self.todraft = []
        self.discarded = []

        
    def __call__(self):
        for _ in range(3):
            self.deal()
            self.select()
            self.player_turn = abs(self.player_turn) - 1
        print(self)
            #print(self["Guylain"])

    def select(self):
        if self.player == self.players[self.player_turn]:
            #command = input(f"Which card do you want? [1 - {len(self.todraft)}]")
            command = 1
        elif self.player != self.players[self.player_turn]:
            command = 1
            #command = input(f"Which card did he want? [1 - {len(self.todraft)}]")
        self[self.players[self.player_turn]].append(self.todraft[int(command)])
        self.todraft.pop(command)

    def deal(self):
        self.discarded += self.todraft
        self.todraft = self.all_cards[:5]
        if not self.todraft:
            self.all_cards, self.discarded = self.discarded, []
            self.todraft = self.all_cards[:5]
        for _ in range(min(len(self.all_cards), 5)):
            self.all_cards.pop(0)

    def __str__(self):
        string = f"{self.players[self.player_turn]}\n"
        string += "-" * 40 + "\n"
        string += f"Cards in the draft pool ({len(self.all_cards)} in deck):\n"
        if self.player != self.players[self.player_turn]:
            pass
        else:
            for card in self.todraft:
                string += f'     {card[:card.index("|")]}\n'
        string += "-" * 40 + "\nMy cards\n"
        for card in self[self.player]:
            string += f'     {card[:card.index("|")]}\n'
        string += "-" * 40 + "\nHis cards (for debugging)\n"
        for card in self[self.players[self.players.index(self.player) -1]]:
            string += f'     {card[:card.index("|")]}\n'
        return string



test = Draft_manager(pooler(40), "Guylain")

test()