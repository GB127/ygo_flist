from random import shuffle
from base import yugioh_modes, verify_int

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
        line = "\n" + "-"*73 + "\n"
        strings = super().__str__().split(line)
        strings.insert(1, self.str_cards("Cards pool", "todraft"))

        return line.join(strings)

test = Draft_manager(300, "Guylain")
test(1)
print(test)