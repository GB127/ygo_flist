from classe.base import ygo_Error, yugioh_modes, verify_int

class Draft(yugioh_modes):
    def __init__(self, pool_size,*,seed_str, player_name, debug=False):
        super().__init__(pool_size, player_name, seed_str=seed_str, debug=debug)
        self.river = []
        self.discarded = []

    def __call__(self, 
                    cards_qtys,  # [draft, river, selection]
                    fill,
                    shuffle,
                    themed_spots,
                    visible,
                    draft_filters=[]):
        def build_filters_spots():
            self.filters= draft_filters + [None for _ in range(river - len(draft_filters))]
            self.river = [None for _ in range(river)]
            if themed_spots:
                pass
            self.deal(shuffle)

        def game_loop():
            while any([len(self[x]) < max_draft for x in self.players]):
                for _ in range(max_sel):
                    self.select()
                    if fill: self.deal(shuffle)
                if not fill: self.deal(shuffle)
                self.player_turn = abs(self.player_turn) - 1

        def error_manager():
            if max_draft * 2 > len(self.pool):
                raise ygo_Error(f"Not enough card inpool.\nPool: {len(self.pool)}\nMinimum needed if {max_draft} cards per person: {max_draft * 2}")
            elif river > len(self.pool):
                raise ygo_Error(f"River too big.\nPool: {len(self.pool)} cards\nRiver: {river} cards")
            elif max_sel > river and not fill:
                raise ygo_Error(f'Selection too big if no fill.\nRiver: {river} cards\nSelecting {max_sel} cards...')
            elif len(draft_filters) > river:
                raise ygo_Error(f"Too many filter given.\n{len(draft_filters)}filters given.\n{river} cards in river.")
        super().__call__()

        max_draft, river, max_sel = [int(x) for x in cards_qtys]
        self.visible = visible

        error_manager()
        build_filters_spots()
        game_loop()
        self.save()

    @verify_int
    def select(self):
        print(self)
        if self.debug:
            command = next((i for i, j in enumerate(self.river) if j), None)
        elif self.player == self.players[self.player_turn]:
            command = input(f"Which card do you want? [0 - {len(self.river)-1}] ")
        elif self.player != self.players[self.player_turn]:
            command = input(f"Which card did he want? [0 - {len(self.river)-1}] ")
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
            strings.insert(0,str(self.player))
            strings.insert(1, str(self.players[self.player_turn]))
            if self.visible and str(self.player) != str(self.players[self.player_turn]):
                strings.insert(1, self.str_cards("Cards pool", "river"))
            elif str(self.player) == str(self.players[self.player_turn]):
                strings.insert(1, self.str_cards("Cards pool", "river"))
            return line.join(strings)
        except TypeError:
            raise BaseException(str([x["name"] if x else None for x in self.river]))


if __name__ == "__main__":
    test1 = Draft(100, seed_str="testing", player_name="Maxime", debug=True)
    test1([20, 5, 1], False, False, False)

    test = Draft(100, seed_str="testing", player_name="Guylain", debug=True)
    test([20, 5, 1], False, False, False)

    print(test1 == test)