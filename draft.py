from random import shuffle
import requests

class yugioh_modes:
    players = ["Guylain", "Maxime"]
    all_cards = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php").json()["data"]

    def __init__(self, player):
        self.player_turn = 1
        self.player = player
        self.Guylain = []
        self.Maxime = []

    def str_cards(self,start, attribute):
        def justificateur(string, width):
            string2 = string.replace("\n", "\n" + " "*width)
            toreturn = ""
            start = 0
            for longueur in range(60, len(string2), 60):
                toreturn += f"{' ' * width}{string2[start:longueur].ljust(10)}\n"
                start = longueur
            toreturn += f"{' ' * width}{string2[start:]}"
            return toreturn



        string = f'{start}'

        for carte in requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" + "|".join(self[attribute])).json()["data"]:
            string += f'\n    {carte["name"]}'
            if "Monster" in carte["type"]:
                string += f' ({carte["type"]})\n        {carte["race"]} - {carte["attribute"]} - level: {carte["level"]}, ATK:{carte["atk"]}, DEF:{carte["def"]}'
            elif "Spell" in carte["type"] or "Trap" in carte["type"]:
                string += f' ({carte["race"]} {carte["type"]})'

            if carte["type"] != "Normal Monster":
                string += f'\n{justificateur(carte["desc"], 12)}'
        return string

    def __str__(self):
        head = f"Player: {self.player}\nTour de {self.players[self.player_turn]}"
        line = "\n" + "-"*73 + "\n"




        return line.join([  head,
                            self.str_cards("My cards:", self.player),
                            self.str_cards("His cards (For debugging)", self.players[self.players.index(self.player) -1])
                        ])

    def __getitem__(self, name):
        return self.__dict__[name]



    def save(self):
        towrite = f"#[2005.4 GOAT]\n!TEST\n#Cards after TG5\n"
        for card in self.all_cards:
            if card["name"] not in self[self.player]:
                towrite += f'{card["id"]} -1 \n'
            else:
                towrite += f'{card["id"]} 3 \n'
        with open("testing_flist.txt", "w") as file:
            file.write(towrite)


class Draft_manager(yugioh_modes):
    def __init__(self, cards_qty, player):
        super().__init__(player)
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
        string = super().__str__()
        return string

test = yugioh_modes("Guylain")
test.Guylain.append(test.all_cards[5]["name"])
test.save()