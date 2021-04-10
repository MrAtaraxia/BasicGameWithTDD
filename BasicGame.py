#!/usr/bin/env python
"""
A Basic setup for a Basic Game.
Mostly going through it in a TDD method
To get practice with it.
"""

from Player import Player
from Game import Game, selection_deck
from Card import Card

"""
More Notes!!!!
from typing import Tuple, Dict, Set, List
LOOK UP TYPING!

List vs list (for typing)
"""


def my_method(s):
    return s


def main() -> None:
    my_choice = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                 "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
    ted = Player(1, "Ted", "Red")
    chris = Player(2, "Chris", "Blue")
    my_board = Game(my_choice, [ted, chris])
    my_board.start_the_game()
    my_board.next_player()
    my_board.next_player()
    print(my_board.players[0].number)
    print(my_board.decks)
    print(my_board.decks["Trash"])
    print(my_board.players)
    # my_board.populate_deck()
    for card in my_board.decks:
        print(card)
    print("ABC")
    print(f"""PLAYER BOARD:{my_board.display_player(0)}""")
    print(my_board.display_board())
    chris.increase_score(2)
    chris.decrease_score(2)
    my_board.players[0].increase_score(1)
    my_board.players[0].decrease_score(1)
    for my_log in my_board.game_log:
        print(my_log)


if __name__ == "__main__":
    main()
