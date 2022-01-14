from base import yugioh_modes, verify_int

class Draft(yugioh_modes):
    def __init__(self, cards_qty,*, player, debug=False):
        super().__init__(cards_qty, player, debug)
        self.todraft = []
        self.discarded = []

    def __call__(self,params):
        """Args:
            params = {
                        max_draft = total cards drafted
                        todeal = Total cards available
                        fill = fill as you select cards (for if you select more than 1 cards)
                    }
            """
        self.deal(params["todeal"])
        while any([len(self[x]) < params["max_draft"] for x in self.players]):
            print(self)
            for _ in range(params["select"]):
                self.select()
                if params["fill"]: self.deal(params["fill"])
            if not params["fill"]: self.deal(params["fill"])
            self.player_turn = abs(self.player_turn) - 1

        self.save()
    
    @verify_int
    def select(self):
        if self.debug:
            command = "0"
        elif self.player == self.players[self.player_turn]:
            command = input(f"Which card do you want? [1 - {len(self.todraft)}] ")
        elif self.player != self.players[self.player_turn]:
            command = input(f"Which card did he want? [1 - {len(self.todraft)}] ")
        self[self.players[self.player_turn]].append(self.todraft[int(command)])
        self.todraft.pop(int(command))

    def deal(self, todeal=5, reset=False):
        if reset:
            self.discarded += self.todraft
            self.todraft = []
        while len(self.todraft) < todeal:
            self.todraft += [self.pool[0]]
            self.pool.pop(0)

    def __str__(self):
        line = "\n" + "-"*73 + "\n"
        strings = super().__str__().split(line)
        strings.insert(1, self.str_cards("Cards pool", "todraft"))
        #return line.join(strings)
        return self.str_cards("Cards pool", "todraft")

if __name__ == "__main__":
    test = Draft(300, player="Guylain", debug=True)
