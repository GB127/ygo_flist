from base import ygo_Error, yugioh_modes, verify_int

class Draft(yugioh_modes):
    def __init__(self, cards_qty,*, player, debug=False):
        super().__init__(cards_qty, player, debug)
        self.todraft = []
        self.discarded = []

    def __call__(self,seed, params={"max_draft": 20, "todeal":5, "select": 1, "fill":False}):
        """Args:
            params = {  select = how much card selection per turn
                        max_draft = total cards drafted
                        todeal = Total cards available
                        fill = fill as you select cards (for if you select more than 1 cards)
                    }
            """
        self.todraft = [None for _ in range(params["todeal"])]
        if (-1 + params["todeal"] + params["max_draft"] *2) > len(self.pool):
            raise ygo_Error(f'You have not enough cards in the pool to play with these parameters.\nYou need {-1 + params["todeal"] + params["max_draft"] *2} cards in pool. The pool has {len(self.pool)}')
        self.deal()
        while any([len(self[x]) < params["max_draft"] for x in self.players]):
            for _ in range(params["select"]):
                self.select()
                if params["fill"]: self.deal()
            if not params["fill"]: self.deal()
            self.player_turn = abs(self.player_turn) - 1
        print(self)
        self.save(seed)
    
    @verify_int
    def select(self):
        print(self)
        if self.debug:
            command = "0"
        elif self.player == self.players[self.player_turn]:
            command = input(f"Which card do you want? [1 - {len(self.todraft)}] ")
        elif self.player != self.players[self.player_turn]:
            command = input(f"Which card did he want? [1 - {len(self.todraft)}] ")
        self[self.players[self.player_turn]].append(self.todraft[int(command)])
        self.todraft[int(command)] = None

    def deal(self, reset=False):
        def get_card(clé, valeur):
            liste_cartes_filtrées = [valeur in x[clé] for x in self.pool]
            if any(liste_cartes_filtrées):
                return liste_cartes_filtrées.index(True)
            return False
        filters = [
                    ("type", "Monster"),
                    ("type", "Trap"),
                    ("type", "Ritual"),
                    ("type", "Monster"),
                    ("type", "Spell")]
        if reset:
            self.discarded += [x for x in self.todraft if x]
            self.todraft = [None for _ in range(len(self.todraft))]
        for spot, (clé, valeur) in enumerate(filters):
            if self.todraft[spot]: continue
            if not self.pool:
                self.pool, self.discarded = self.discarded, [] 
            id = get_card(clé, valeur) if get_card(clé, valeur) else 0
            self.todraft[spot] = self.pool[id]
            self.pool.pop(id)

    def __str__(self):
        line = "\n" + "-"*73 + "\n"
        strings = super().__str__().split(line)
        strings.insert(1, self.str_cards("Cards pool", "todraft"))
        return line.join(strings)


if __name__ == "__main__":
    
    test = Draft(50, player="Guylain", debug=True)
    test("testing")