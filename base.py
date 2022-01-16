from random import choice, randint, shuffle, seed
import requests
import os

clear = lambda: os.system('cls')

class ygo_Error(BaseException):
    pass

def verify_int(fonc):
    def new_fonction(arg):
        while True:
            try:
                return fonc(arg)
            except ValueError:
                print("Please enter a valid number")
    return new_fonction


class yugioh_modes:
    players = ["Guylain", "Maxime"]
    banlist =   {
                0: [
                    "Black Luster Soldier - Envoy of the Beginning",
                    "Chaos Emperor Dragon - Envoy of the End",
                    "Cyber Jar",
                    "Cyber-Stein",
                    "Dark Magician of Chaos",
                    "Dark Strike Fighter",
                    "Destiny HERO - Disk Commander",
                    "Fiber Jar",
                    "Magical Scientist",
                    "Magician of Faith",
                    "Makyura the Destructor",
                    "Sinister Serpent",
                    "Thousand-Eyes Restrict",
                    "Tribe-Infecting Virus",
                    "Tsukuyomi",
                    "Victory Dragon",
                    "Witch of the Black Forest",
                    "Yata-Garasu",
                    "Butterfly Dagger - Elma",
                    "Card of Safe Return",
                    "Change of Heart",
                    "Confiscation",
                    "Dark Hole",
                    "Delinquent Duo",
                    "Dimension Fusion",
                    "Graceful Charity",
                    "Harpie's Feather Duster",
                    "Last Will",
                    "Monster Reborn",
                    "Metamorphosis",
                    "Mirage of Nightmare",
                    "Painful Choice",
                    "Pot of Greed",
                    "Premature Burial",
                    "Raigeki",
                    "Snatch Steal",
                    "The Forceful Sentry",
                    "Crush Card Virus",
                    "Exchange of the Spirit",
                    "Imperial Order",
                    "Last Turn",
                    "Ring of Destruction",
                    "Time Seal"],
                1:[
                    'Advanced Ritual Art', 
                    'Allure of Darkness', 
                    'Black Rose Dragon', 
                    'Blackwing - Gale the Whirlwind', 
                    'Brain Control', 
                    'Brionac, Dragon of the Ice Barrier', 
                    'Burial from a Different Dimension', 
                    'Call of the Haunted', 
                    'Card Destruction',
                    'Card Trooper', 
                    'Ceasefire', 
                    'Chaos Sorcerer',
                    'Charge of the Light Brigade',
                    'Cold Wave',
                    'Dark Armed Dragon',
                    'Destiny Draw',
                    'Elemental HERO Stratos',
                    'Emergency Teleport',
                    'Exodia the Forbidden One',
                    'Foolish Burial',
                    'Future Fusion',
                    'Giant Trunade',
                    'Gladiator Beast Bestiari',
                    'Gorz the Emissary of Darkness',
                    'Goyo Guardian',
                    'Gravity Bind',
                    'Heavy Storm',
                    'Left Arm of the Forbidden One',
                    'Left Leg of the Forbidden One',
                    'Level Limit - Area B',
                    'Limiter Removal',
                    'Lumina, Lightsworn Summoner',
                    'Magic Cylinder',
                    'Magical Explosion',
                    'Marshmallon',
                    'Megamorph',
                    'Mezuki',
                    'Mind Control',
                    'Mind Crush',
                    'Mind Master',
                    'Mirror Force',
                    'Monster Gate',
                    'Morphing Jar',
                    'Mystical Space Typhoon',
                    'Necro Gardna',
                    'Necroface',
                    'Neo-Spacian Grand Mole',
                    'Night Assailant',
                    'Ojama Trio', 
                    'One for One',
                    'Overload Fusion', 
                    'Plaguespreader Zombie',
                    'Reasoning', 
                    'Reinforcement of the Army',
                    'Rescue Cat',
                    'Return from the Different Dimension', 
                    'Right Arm of the Forbidden One', 
                    'Right Leg of the Forbidden One',
                    'Sangan',
                    'Scapegoat',
                    'Snipe Hunter',
                    'Solemn Judgment',
                    'Spirit Reaper',
                    'Summoner Monk',
                    'Swords of Revealing Light',
                    'The Transmigration Prophecy',
                    'Torrential Tribute',
                    'Tragoedia',
                    'Trap Dustshoot',
                    'Wall of Revealing Light'],
                2:[
                    "Cyber Dragon",
                    "Dandylion",
                    "Demise, King of Armageddon",
                    "Destiny HERO - Malicious",
                    "Goblin Zombie",
                    "Honest",
                    "Judgment Dragon",
                    "Lonefire Blossom",
                    "Treeborn Frog",
                    "Black Whirlwind",
                    "Chain Strike",
                    "Gold Sarcophagus",
                    "Magical Stone Excavation",
                    "United We Stand",
                    "Bottomless Trap Hole",
                    "Royal Decree",
                    "Royal Oppression",
                    "Skill Drain",
                    "Ultimate Offering"]
                }

    def __init__(self, cards_qty, player,*, seed_str, debug=False):
        self.all_cards = []
        self.accepted_cards = []

        with open("cards_list.txt", "r") as file:
            tempo = file.read().rstrip("\n").split("\n")
            for carte in requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php").json()["data"]:
                self.all_cards.append(carte)
                if carte["name"] in tempo:
                    self.accepted_cards.append(carte)



        seed(seed_str)
        self.seed = seed_str
        self.debug = debug
        self.player_turn = randint(0,1)
        self.player = player
        self.Guylain = []
        self.Maxime = []
        shuffle(self.accepted_cards)
        self.pool = self.accepted_cards[:cards_qty]

    def str_cards(self,start, attribute):
        def justificateur(string, width):
            string2 = string.replace("\n", "\n" + " "*width)
            toreturn = ""
            start = 0
            for longueur in range(80, len(string2), 80):
                toreturn += f"{' ' * width}{string2[start:longueur].ljust(10)}\n"
                start = longueur
            toreturn += f"{' ' * width}{string2[start:]}"
            return toreturn

        string = f'{start} - {len(self[attribute])} cards'
        if not self[attribute]:
            return string

        for no, carte in enumerate(self[attribute]):
            if not carte: 
                string += "Empty Spot\n"
                continue
            string += f'\n{no:2}    {carte["name"]}'
            if "Monster" in carte["type"]:
                string += f' ({carte["type"]})\n        {carte["race"]} - {carte["attribute"]} - level: {carte["level"]}, ATK:{carte["atk"]}, DEF:{carte["def"]}'
            elif "Spell" in carte["type"] or "Trap" in carte["type"]:
                string += f' ({carte["race"]} {carte["type"]})'
            if carte["type"] != "Normal Monster":
                string += f'\n{justificateur(carte["desc"], 12)}'
        return string

    def __str__(self):
        clear()
        head = f"Player: {self.player}\nTour de {self.players[self.player_turn]}"
        line = "\n" + "-"*73 + "\n"

        toreturn = [  head,
                            self.str_cards("My cards:", self.player),
                        ]
        if self.debug:
            toreturn.insert(2,self.str_cards("His cards (For debugging)",self.players[self.players.index(self.player) -1]))
        return line.join(toreturn)

    def __getitem__(self, name):
        return self.__dict__[name]


    def __call__(self):
        print(f'Seed : {self.seed}')
        for _ in range(5):
            print(f'     {choice(self.accepted_cards)["name"]}')
        if not self.debug:
            input("Do the checksum match?\nIf yes, continue\nElse, close the terminal and restart.")
    
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
        with open(f"{self.player}_{self.seed}.lflist.conf", "w") as file:
            file.write(towrite)

if __name__ == "__main__":
    test = yugioh_modes(300,seed_str="Testing2", player="Maxime")
    test()
    test2 = yugioh_modes(300,seed_str="Testing2", player="Guylain")
    test2()