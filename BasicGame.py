#!/usr/bin/env python
"""
A Basic setup for a Basic Game.
Mostly going through it in a TDD method
To get practice with it.
"""

import random
from typing import List

"""
More Notes!!!!
from typing import Tuple, Dict, Set, List
LOOK UP TYPING!

List vs list (for typing)
"""


class Card:
    """
    The class of cards
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, name: str, card_type: str = None, cost: int = 1,
                 action: str = None, description: str = None):
        self.name = name
        self.cost = cost
        self.type = card_type
        self.description = description
        self.action = action

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self) -> str:
        """
        I Might want to change this one. I am not sure yet.
        """
        return "Card: " + self.name

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> hash:
        return hash("Card: " + self.name)


class Player:

    def __init__(self, player_number: int = None,
                 player_name: str = None, color: str = None) -> None:
        self.number = player_number
        self.name = player_name
        self.color = color
        self.score = 0
        self.turn_order = None
        self.cards, self.hand, self.deck, self.discard, = [], [], [], []
        self.buys = 1
        self.actions = 1
        self.gold = 0
        self.resources = {}
        self.play_area = {"cards": [], "resources": {}}
        self.is_active_player = False
        self.game = None

    def increase_score(self, amount: int) -> None:
        self.score += amount

    def decrease_score(self, amount: int) -> None:
        self.score -= amount

    def create_deck(self) -> None:
        self.cards.extend(["Copper", "Copper", "Copper", "Copper",
                           "Copper", "Copper", "Copper", "Estate",
                           "Estate", "Estate"])
        self.deck.extend(self.cards)

    def draw_cards(self, number) -> None:
        try:
            for _ in range(number):
                self.hand.append(self.deck.pop(0))
        except IndexError:
            print("You can not draw a card from an empty deck.")

    def discard_cards(self, number: int = 1) -> None:
        """
        Not RANDOM YET!
        Not selecting card yet.
        just removing 1 card for now!
        NO CHECKING YET!
        :param number: The number of cards.
        :return: None
        """
        # if len(self.hand) - number > min_count:
        try:
            for _ in range(number):
                self.discard.append(self.hand.pop(0))
        except IndexError:
            print("You can not discard a card from an empty hand.")

    def discard_to_deck(self) -> None:
        """
        Combines the discard pile to the deck.
        """
        for _ in range(len(self.discard)):
            self.deck.append(self.discard.pop(0))

    def shuffle_deck(self) -> None:
        """
        Shuffles the players deck.
        :return: None
        """
        random.shuffle(self.deck)

    def play_card(self, number) -> None:
        """
        :param number: the number of the location of the card that is being played.
        """
        try:
            self.play_area["cards"].append(self.hand.pop(number))
        except IndexError:
            print("You can not play a card from an empty hand.")

    def gain_card(self, card):
        self.discard.append(self.game.decks[card].pop(0))

    def buy_card(self, card) -> None:
        if self.gold >= card.cost and self.buys >= 1:
            self.gain_card(card)
            self.buys -= 1
            self.gold -= card.cost

    def clean_up(self) -> None:
        for _ in range(len(self.play_area["cards"])):
            self.discard.append(self.play_area["cards"].pop(0))

    def trash_card(self) -> None:
        self.hand.pop(0)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'Player:{self.name}'

    def __repr__(self):
        return f'Player(number{self.number}, my_name={self.name}, color={self.color})'


class GameBoard:
    def __init__(self, name=None):
        self.name = name
        self.locations = None
        self.discard = [Card]


class MyGame:
    def __init__(self, card_choices: List[Card] = None, players: List[Player] = None):
        if card_choices:
            self.card_choices = card_choices
        else:
            self.card_choices = [Card("Explorer", "Action"),
                                 Card("Moat", "Reaction"),
                                 Card("Thief", "Action-Attack"),
                                 Card("Duke", "Action-Victory"),
                                 Card("Torturer", "Action-Attack"),
                                 Card("Card1", "Action"),
                                 Card("Card2", "Action"),
                                 Card("Card3", "Action"),
                                 Card("Card4", "Action"),
                                 Card("Card5", "Action")]
        self.first_player = 0
        self.active_player = self.first_player
        self.decks = self.setup_decks(self.card_choices)
        self.resources = {}
        # self.setup_decks()
        self.discard = []

        if players is None:
            self.players = [Player(100, "Bob", "Red")]
            print(self.players[0].number)
        else:
            self.players = players
        for player in self.players:
            player.game = self
        self.game_board = GameBoard("Game")
        self.mark_active_player()

    def __repr__(self):
        return f"MyGame({self.players})"

    @staticmethod
    def setup_decks(card_choices):
        current_deck = {"Copper": [Card("Copper", "Treasure") for _ in range(60)],
                        "Silver": [Card("Silver", "Treasure") for _ in range(60)],
                        "Gold": [Card("Gold", "Treasure") for _ in range(60)],
                        "Estate": [Card("Estate", "Victory") for _ in range(12)],
                        "Duchy": [Card("Duchy", "Victory") for _ in range(12)],
                        "Providence": [Card("Providence", "Victory") for _ in range(12)],
                        "Curse": [Card("Curse", "Curse") for _ in range(10)],
                        "Trash": []}
        for cards in card_choices:
            current_deck[str(cards)] = [cards for _ in range(10)]
        return current_deck

    def mark_active_player(self):
        """
        Setup the players turn and mark them as active player.
        """
        for player in self.players:
            if player == self.players[self.active_player]:
                player.is_active_player = True
                player.actions = 1
                player.buys = 1
            else:
                player.is_active_player = False

    def next_player(self):
        self.active_player = (self.active_player + 1) % len(self.players)
        self.mark_active_player()


def my_method(s):
    return s


def main():
    my_board = MyGame()
    print(my_board.players[0].number)
    print(my_board.decks)
    print(my_board.discard)
    print(repr(my_board.players))
    print(my_board.players)
    my_card = Card("Copper")
    # my_board.populate_deck()
    for card in my_board.decks:
        print(card)
    print(my_card)
    print("ABC")


if __name__ == "__main__":
    main()
