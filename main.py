from draft import Draft
import argparse
from random import random

def getcommand():
    parser = argparse.ArgumentParser(description="Yugioh Card pooler")
    parser.add_argument("--pool", action="store", type=int, default=200, help="# of card in the pool")
    parser.add_argument("--seed",
                            action="store",
                            help="Seed for the randomization",
                            default=str(random())[2:],
                            metavar="seed",
                            type=str)
    parser.add_argument("-d", "--draft",
                            nargs=3,
                            help="Draft mode : [Total, River, select]")
    parser.add_argument("-s", "--shuffle",
                            action="store_true",
                            help="Shuffle cards between actions")
    parser.add_argument("-v", "--visible", action="store_true",
                            help="Make common cards always visible.")

    parser.add_argument("-f", "--fill",
                            action="store_true",
                            help="Fill cards between actions")
    parser.add_argument("-t", "--themed",
                            action="store_true",
                            help="Cards spots follows a theme.")


    options = parser.parse_args()
    return options

if __name__ == "__main__":
    options = getcommand()
    if options.draft:
        game = Draft(300,seed_str=options.seed, player_name="Maxime")
        game(options.draft, 
                options.fill,
                options.shuffle,
                options.themed,
                options.visible)