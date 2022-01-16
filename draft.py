from base import ygo_Error, yugioh_modes, verify_int

class Draft(yugioh_modes):
    def __init__(self, pool_size,*,seed_str, player_name, debug=False):
        super().__init__(pool_size, player_name, seed_str=seed_str, debug=debug)
        self.river = []
        self.discarded = []

    def __call__(self, 
                    cards_qtys,
                    fill,
                    shuffle,
                    themed_spots,
                    draft_filters=[]):
        def build_filters_spots():
            self.filters= draft_filters + [None for _ in range(river - len(draft_filters))]
            self.river = [None for _ in range(river)]
            if themed_spots:
                print("WIP")
            self.deal(shuffle)

        def game_loop():
            while any([len(self[x]) < max_draft for x in self.players]):
                for _ in range(max_sel):
                    self.select()
                    if fill: self.deal(shuffle)
                if not fill: self.deal(shuffle)
                self.player_turn = abs(self.player_turn) - 1

        super().__call__()

        max_draft, river, max_sel = [int(x) for x in cards_qtys]

        build_filters_spots()
        game_loop()
        self.save()

    @verify_int
    def select(self):
        print(self)
        if self.debug:
            command = next((i for i, j in enumerate(self.river) if j), None)
        elif self.player == self.players[self.player_turn]:
            command = input(f"Which card do you want? [1 - {len(self.river)}] ")
        elif self.player != self.players[self.player_turn]:
            command = input(f"Which card did he want? [1 - {len(self.river)}] ")
        if not self.river[int(command)]: raise ValueError("A None card has been drawn")
        self[self.players[self.player_turn]].append(self.river[int(command)])
        self.river[int(command)] = None
    
    def deal(self, reset=False):
        def get_first_match(clé, valeur):
            liste_cartes_filtrées = [valeur in x[clé] for x in self.pool]
            if any(liste_cartes_filtrées):
                return liste_cartes_filtrées.index(True)
            return False

        if reset:
            self.discarded += [x for x in self.river if x]
            self.river = [None for _ in range(len(self.river))]
        for spot, filtre in enumerate(self.filters):
            if self.river[spot]: continue  # Spot is not empty
            if not self.pool:  # Check if pool is empty!
                self.pool, self.discarded = self.discarded, []
            try:
                id = get_first_match(filtre[0], filtre[1]) if get_first_match(filtre[0], filtre[1]) else 0
                self.river[spot] = self.pool[id]
                self.pool.pop(id)
            except TypeError:  # Use any card. (No filter)
                self.river[spot] = self.pool[0]
                self.pool.pop(0)


    def __str__(self):
        try:
            line = "\n" + "-"*73 + "\n"
            strings = super().__str__().split(line)
            strings.insert(1, self.str_cards("Cards pool", "todraft"))
            return line.join(strings)
        except TypeError:
            raise BaseException(str([x["name"] if x else None for x in self.river]))


if __name__ == "__main__":
    test = Draft(300, seed_str="testing", player="Maxime", debug=True)
    test([20, 5, 2], True, True, True)