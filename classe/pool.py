from requests import get
from random import shuffle

from classe.card import Monster, Spell, Trap

class Pool:
    def __init__(self, size):
        def fetch_all_cards():
            cards = []
            with open("cards_list.txt", "r") as file:
                tempo = file.read().rstrip("\n").split("\n")
                for carte in get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php").json()["data"]:
                    if carte["name"] in tempo:
                        cards.append(carte)
            return cards

        def card_type_splitter(dicto):
            if "Monster" in dicto["type"]:
                return Monster(dicto)
            elif "Spell" in dicto["type"]:
                return Spell(dicto)
            elif "Trap" in dicto["type"]:
                return Trap(dicto)

        cards = []
        self.discard = []
        self.dependent = []

        for card in fetch_all_cards():
            tempo = card_type_splitter(card)
            if tempo:
                cards.append(tempo)
            else:
                self.dependent.append(tempo)

        shuffle(cards)
        self.pool = cards[:size]


    def __getitem__(self,id:int):
        return self.pool[id]

    def deal(self, qty:int)->list:
        toreturn = self.pool[:qty]
        for _ in range(qty):
            self.pool.pop(0)
        return toreturn

    def take_discard(self, cards:list):
        self.discard += cards

    def shuffle(self):
        shuffle(self.pool)


    def mix_discarded_pool(self):
        self.pool = self.pool + self.discard
        self.discard = []


    def __len__(self):
        return len(self.pool)