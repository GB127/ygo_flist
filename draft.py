from random import choice
from base import ygo_Error, yugioh_modes, verify_int

class Draft(yugioh_modes):
    def __init__(self, cards_qty,*,seed_str, player, debug=False):
        super().__init__(cards_qty,player, seed_str=seed_str, debug=debug)
        self.todraft = []
        self.discarded = []

    def __call__(self,  seed, params={"shuffle":True, "max_draft": 20, "todeal":5, "select": 1, "fill":False, "themed_draft":False}, 
                draft_filters=[None for _ in range(5)]):
        """Args:
            params = {  select = how much card selection per turn
                        max_draft = total cards drafted
                        todeal = Total cards available
                        fill = fill as you select cards (for if you select more than 1 cards)
                        shuffle = Shuffle between selections?
                    }
            """
        def build_filters_spots():
            def complete_themed_draft():
                for _ in range(params["todeal"] - len(self.filters)):
                    scape = "id"
                    while scape in ["id", "card_prices","desc", "name", "card_images", "card_sets"]:
                        scape = choice(list(choice(self.pool).keys()))
                    valeur = choice(list(set([x[scape] for x in self.pool if scape in x])))
                    self.filters.append((scape, valeur))

            self.filters = draft_filters
            if params["themed_draft"]:
                complete_themed_draft()
            self.todraft = [None for _ in range(params["todeal"])]
            self.deal(params["shuffle"])

        def game_loop():
            while any([len(self[x]) < params["max_draft"] for x in self.players]):
                for _ in range(params["select"]):
                    self.select()
                    if params["fill"]: self.deal(params["shuffle"])
                if not params["fill"]: self.deal(params["shuffle"])
                self.player_turn = abs(self.player_turn) - 1

        super().__call__()
        if (-1 + params["todeal"] + params["max_draft"] *2) > len(self.pool):
            raise ygo_Error(f'You have not enough cards in the pool to play with these parameters.\nYou need {-1 + params["todeal"] + params["max_draft"] *2} cards in pool. The pool has {len(self.pool)}')
        if (params["todeal"] != len(draft_filters)):
            raise ygo_Error(f'You must give a filter for each spot.\n{len(draft_filters)} Filters given, {params["todeal"]} cards dealt.')

        build_filters_spots()
        game_loop()
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

        if reset:
            self.discarded += [x for x in self.todraft if x]
            self.todraft = [None for _ in range(len(self.todraft))]
        for spot, filtre in enumerate(self.filters):
            if self.todraft[spot]: continue  # Spot is not empty
            if not self.pool:  # Check if pool is empty!
                self.pool, self.discarded = self.discarded, []
            try:
                id = get_card(filtre[0], filtre[1]) if get_card(filtre[0], filtre[1]) else 0
                self.todraft[spot] = self.pool[id]
                self.pool.pop(id)
            except TypeError:  # Use any card. (No filter)
                self.todraft[spot] = self.pool[0]
                self.pool.pop(0)


    def __str__(self):
        line = "\n" + "-"*73 + "\n"
        strings = super().__str__().split(line)
        strings.insert(1, self.str_cards("Cards pool", "todraft"))
        return line.join(strings)


if __name__ == "__main__":
    
    test = Draft(50, seed_str= "testing", player="Guylain", debug=True)
    test("testing")