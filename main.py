from cards import *
import argparse
import random

def getcommand():
    parser = argparse.ArgumentParser(description="Yugioh Card pooler")
    parser.add_argument("seed", 
                        action="store",
                        help="Seed for the randomization",
                        default=str(random.random())[2:],
                        metavar="",
                        type=str)    
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    options = getcommand()
    if options.seed == "0":
        filename = "GB_MAX_BANLIST_final.lflist.conf"
    else:
        random.seed(options.seed)
        filename = f'Random_pool_{options.seed}.lflist.conf'
    auto_ban(filename)
    all_cards = get_cards_pool()
    if options.seed != "0":
        monsters, spells, traps, extras = split_pool(all_cards)
        for ty in [monsters, spells, traps, extras]: random.shuffle(ty)

        # Monsters:
        allow_pool(filename, monsters[:200])
        ban_pool(filename, monsters[201:])

        # Spells:
        allow_pool(filename, spells[:100])
        ban_pool(filename, spells[101:])
        # Traps:
        allow_pool(filename, traps[:100])
        ban_pool(filename, traps[101:])

        # Extras:
        allow_pool(filename, extras[:50])
        ban_pool(filename, extras[51:])
    else:
        allow_pool(filename, get_cards_pool())