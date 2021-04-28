import requests
import os
from copy import deepcopy
import random

def auto_ban(filename):
    end = "10/26/2010"
    today = "04/27/2021"
    rep_toban = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={end}&enddate={today}&dateregion=ocg_date")
    if rep_toban.status_code == 200:
        all_toban = rep_toban.json()["data"]
    else:
        raise BaseException("Something went wrong")
    toreturn = "#[2005.4 GOAT]\n!2010.10 GB&MAX\n#Cards after TG5\n"
    for card in all_toban:
        toreturn += f"{card['id']} -1 \n"

    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as fichier:
        fichier.write(toreturn)

def get_cards_pool():
    end = "10/26/2010"
    start = "02/04/1999"
    rep = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={start}&enddate={end}&dateregion=ocg_date")
    if rep.status_code == 200:
        card_pool = rep.json()["data"]
    else:
        raise BaseException("Something went wrong")
    return card_pool

def apply_banlist(filename, pool):
    no_ban = []
    forbidden = [
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
        "Time Seal"
        ]
    limited = [
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
        'Wall of Revealing Light']
    semi = [
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

    for card in pool:
        if card["name"] in forbidden:
            with open(filename, "a") as fichier:
                fichier.write(f'{card["id"]} 0 \n')
        elif card["name"] in limited:
            with open(filename, "a") as fichier:
                fichier.write(f'{card["id"]} 1 \n')
        elif card["name"] in limited:
            with open(filename, "a") as fichier:
                fichier.write(f'{card["id"]} 2 \n')
        else:
            no_ban.append(card)
    return no_ban

def allow_pool(filename, pool):
    with open(filename, "a") as fichier:
        for card in pool:
            fichier.write(f'{card["id"]} 3 \n')

def ban_pool(filename, pool):
    with open(filename, "a") as fichier:
        for card in pool:
            fichier.write(f'{card["id"]} 0 \n')
