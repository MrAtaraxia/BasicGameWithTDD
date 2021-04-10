#!/usr/bin/env python
"""
Card.py
The Basic Card Class.

"""

from typing import List, Union


class Card:
    """
    The class of cards
    """

    def __new__(cls, *args, **kwargs):
        """
        WHY DO I HAVE THIS? IDK... It seemed interesting at the time!
        """
        instance = super().__new__(cls)
        return instance

    def __init__(self, name: str, card_type: str, cost: int = 1,
                 action: str = None, description: str = None,
                 value: int = 0, v_points: int = 0) -> None:
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.description = description
        self.action = action
        self.value = value
        self.points = v_points

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __int__(self) -> int:
        return self.cost

    def __gt__(self, other):
        return int(self) > int(other)

    def __repr__(self) -> str:
        """
        I Might want to change this one. I am not sure yet.
        """
        return "Card: " + self.name

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> hash:
        return hash("Card: " + self.name)


def default_decks() -> List[List[Union[Card, str]]]:
    the_deck = [[Card("Copper", "Treasure", 0, value=1), "60"],
                [Card("Silver", "Treasure", 3, value=2), "40"],
                [Card("Gold", "Treasure", 6, value=3), "30"],
                [Card("Estate", "Victory", 2, v_points=1), "12"],
                [Card("Duchy", "Victory", 5, v_points=3), "12"],
                [Card("Providence", "Victory", 8, v_points=6), "12"],
                [Card("Curse", "Curse", 0, v_points=-1),
                 "((len(self.players) - 1) * 10)"],
                [Card("Trash", "Trash"), "0"]]
    return the_deck


if __name__ == "__main__":
    pass
