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
    if options.seed == 0:
        filename = "GB_MAX_BANLIST_final.lflist.conf"
    else:
        filename = f'Random_pool_{options.seed}.lflist.conf'

    auto_ban(filename)
    all_cards = get_cards_pool()
    apply_banlist(filename, all_cards)
    if options.seed != 0:
        print("allo")