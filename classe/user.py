class User:
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

    def __init__(self, username):
        assert username in ["Guylain", "Maxime"]
        self.username = username
        self.cards = []

    def take_cards(self, liste_card):
        assert isinstance(liste_card, list)
        self.cards += liste_card


    def save(self):
        towrite = f"#[2005.4 GOAT]\n!TEST\n#Cards after TG5\n"
        with open(f'cards_alt.txt') as file:
            for id in file.readlines():
                tempo = id.strip("\n")
                towrite += f'{tempo} -1 \n'
        for card in self.all_cards:
            if card not in self[self.player]:
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