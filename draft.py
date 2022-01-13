from random import shuffle, randint
import requests


def verify_int(fonc):
    def new_fonction(arg):
        while True:
            try:
                return fonc(arg)
            except ValueError: 
                print("Please enter a number")
    return new_fonction


class yugioh_modes:
    players = ["Guylain", "Maxime"]
    all_cards = []
    accepted_cards = []
    with open("cards_list.txt", "r") as file:
        tempo = file.read().rstrip("\n").split("\n")
        for carte in requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php").json()["data"]:
            all_cards.append(carte)
            if carte["name"] in tempo:
                accepted_cards.append(carte)
    del tempo


    def __init__(self, player):
        self.player_turn = randint(0,1)
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
        if not self[attribute]:
            return string

        for carte in self[attribute]:
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
        with open(f'cards_alt.txt') as file:
            for id in file.readlines():
                tempo = id.strip("\n")
                towrite += f'{tempo} -1 \n'
        for card in self.all_cards:
            if card["name"] not in self[self.player]:
                towrite += f'{card["id"]} -1 \n'
            else:
                towrite += f'{card["id"]} 3 \n'
        with open(f"testing_flist{self.player}.lflist.conf", "w") as file:
            file.write(towrite)


class Draft_manager(yugioh_modes):
    def __init__(self, cards_qty, player):
        super().__init__(player)
        shuffle(self.accepted_cards)
        self.pool = self.accepted_cards[:cards_qty]
        self.todraft = []
        self.discarded = []

    def __call__(self, max_draft):
        while any([len(self[x]) < max_draft for x in self.players]):
            self.deal()
            self.select()
            self.player_turn = abs(self.player_turn) - 1

        self.save()
    
    @verify_int
    def select(self):
        if self.player == self.players[self.player_turn]:
            #command = input(f"Which card do you want? [1 - {len(self.todraft)}] ")
            command = "1"
        elif self.player != self.players[self.player_turn]:
            command = "1"
            #command = input(f"Which card did he want? [1 - {len(self.todraft)}] ")
        self[self.players[self.player_turn]].append(self.todraft[int(command)])
        self.todraft.pop(int(command))

    def deal(self):
        self.discarded += self.todraft
        self.todraft = self.pool[:5]
        if not self.todraft:
            self.pool, self.discarded = self.discarded, []
            shuffle(self.pool)
            self.todraft = self.pool[:5]
        for _ in range(min(len(self.pool), 5)):
            self.pool.pop(0)

    def __str__(self):
        string = super().__str__()
        return string

test = Draft_manager(300, "Guylain")
test.save()