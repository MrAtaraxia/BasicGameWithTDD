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
        """
        WHY DO I HAVE THIS? IDK... It seemed interesting at the time!
        """
        instance = super().__new__(cls)
        return instance

    def __init__(self, name: str, card_type: str, cost: int = 1,
                 action: str = None, description: str = None, value: int = 0, v_points: int = 0):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.description = description
        self.action = action
        self.value = value
        self.points = v_points

    def __eq__(self, other):
        return str(self) == str(other)

    def __gt__(self, other):
        return self.cost > other.cost

    def __repr__(self) -> str:
        """
        I Might want to change this one. I am not sure yet.
        """
        return "Card: " + self.name

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> hash:
        return hash("Card: " + self.name)


def selection_deck():
    base_game = [Card("Cellar", "Action", 2, None,
                      """
                      +1 Actions
                      Discard any number of cards.
                      +1 Card per card discarded.
                      """),
                 Card("Chapel", "Action", 2, None,
                      """
                      Trash up to 4 cards from your hand.
                      """),
                 Card("Moat", "Action - Reaction", 2, None,
                      """
                      +2 Cards
                      ---
                      When another player plays an Attack
                      card, you may reveal this card from your 
                      hand. If you do, you are unaffected
                      by the attack.
                      """),
                 Card("Chancellor", "Action", 3, None,
                      """
                      +2 Gold
                      You may immediately put your 
                      deck into your discard pile.
                      """),
                 Card("Village", "Action", 3, None,
                      """
                      +1 Card
                      +2 Actions
                      """),
                 Card("Woodcutter", "Action", 3, None,
                      """
                      +1 Buy
                      +2 Coins
                      """),
                 Card("Feast", "Action", 4, None,
                      """
                      Trash this card.
                      Gain a card costing up to 5.
                      """),
                 Card("Militia", "Action - Attack", 4,
                      """
                      self.coins += 2
                      if other_players.receive_attack():
                        other_players.hand_limit = 3
                      """,
                      """
                      +2 Coins
                      Each other player discards
                      down to 3 cards in his hand.
                      """),
                 Card("Moneylender", "Action", 4, None,
                      """
                      Trash a Copper from your hand.
                      If you do +3 Coins.
                      """),
                 Card("Remodel", "Action", 4, None,
                      """
                      Trash a card from your hand.
                      Gain a card costing up to 2 Coins more
                      than the trashed card. 
                      """),
                 Card("Smithy", "Action", 4,
                      """self.draw_cards(3)""",
                      """
                      +3 Cards
                      """),
                 Card("Spy", "Action - Attack", 4, None,
                      """
                      +1 Card
                      +1 Action
                      Each player (including you) reveals
                      the top card of his deck and either
                      discards it or puts it back, your choice.
                      """),
                 Card("Thief", "Action - Attack", 4, None,
                      """
                      Each other player reveals the top 
                      2 cards of his deck.
                      If they reveal any Treasure cards,
                      they trash one of them that you choose.
                      You may gain any or all of these 
                      trashed cards. They discard the 
                      other revealed cards.
                      """),
                 Card("Throne Room", "Action", 4, None,
                      """
                      Choose an Action card in your hand.
                      Play it twice.
                      """),
                 Card("Council Room", "Action", 5, None,
                      """
                      +4 Cards
                      +1 Buy
                      Each other player draws a card.
                      """),
                 Card("Festival", "Action", 5,
                      """
                      self.actions += 2
                      self.buys += 1
                      self.coins += 2
                      """,
                      """
                      +2 Actions
                      +1 Buy
                      +2 Coins
                      """)]
    return base_game


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
        self.coins = 0
        self.resources = {}
        self.play_area = {"cards": [], "resources": {}}
        self.is_active_player = False
        # print(self)
        if self == str(self):
            self.game = None
        # self.create_deck()

    def increase_score(self, amount: int) -> None:
        self.score += amount

    def decrease_score(self, amount: int) -> None:
        self.score -= amount

    def create_deck(self) -> None:
        if self.game:
            self.cards.extend([self.game.decks["Copper"] for _ in range(7)])
            self.cards.extend([self.game.decks["Estate"] for _ in range(3)])
        else:
            self.cards.extend([Card("Copper", "Treasure", 0, None, None, 1)] for _ in range(7))
            self.cards.extend([Card("Estate", "Victory", 2, v_points=1)] for _ in range(3))
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
            print(self.hand[number][0].card_type)
            if str(self.hand[number][0].card_type) == "Action" or \
                    str(self.hand[number][0].card_type) == "Action Attack":
                self.play_area["cards"].append(self.hand.pop(number))
            else:
                raise AttributeError("That card is not playable!")

        except IndexError:
            print("You can not play a card from an empty hand.")

    def gain_coins(self):
        for card in self.hand:
            self.coins += card.value

    def gain_card(self, card, where="discard"):
        if where == "discard":
            self.discard.append(self.game.decks[card].pop(0))
        elif where == "hand":
            self.hand.append([self.game.decks[card].pop(0)])

    def buy_card(self, card) -> None:
        if self.coins >= card.cost and self.buys >= 1:
            self.gain_card(card)
            self.buys -= 1
            self.coins -= card.cost
        else:
            raise ValueError("You do not have enough coins to buy that card!")

    def clean_up(self) -> None:
        for _ in range(len(self.play_area["cards"])):
            self.discard.append(self.play_area["cards"].pop(0))

    def trash_card(self, card_number) -> None:
        self.game.decks["Trash"].append(self.hand.pop(card_number))

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


class MyGame:
    def __init__(self, choices: List[str] = None, players: List[Player] = None):
        if players is None:
            self.players = [Player(1, "Bob", "Red"), Player(2, "Chris", "Blue")]
        else:
            self.players = players
        for player in self.players:
            player.game = self

        my_deck = selection_deck()
        card_choices = []
        if choices:
            choices = [str(x).lower() for x in choices]
        else:
            choices = ["cellar", "remodel", "moneylender", "militia", "village",
                       "woodcutter", "moat", "feast", "chapel", "chancellor"]
        for card in my_deck:
            if card.name.lower() in choices:
                card_choices.append(card)
        if len(card_choices) == 10:
            self.card_choices = card_choices
        else:
            card_choices = []
            choices = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                       "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
            for card in my_deck:
                if card.name.lower() in choices:
                    card_choices.append(card)
            self.card_choices = card_choices

        self.first_player = 0
        self.active_player = self.first_player
        self.decks = self.setup_decks(self.card_choices)
        self.resources = {}
        # self.setup_decks()
        self.discard = []

        self.game_board = GameBoard("Game")
        self.mark_active_player()

    def __repr__(self):
        return f"MyGame({self.players})"

    @staticmethod
    def setup_decks(card_choices):
        current_deck = {"Copper": [Card("Copper", "Treasure", 0, value=1) for _ in range(60)],
                        "Silver": [Card("Silver", "Treasure", 3, value=2) for _ in range(60)],
                        "Gold": [Card("Gold", "Treasure", 6, value=3) for _ in range(60)],
                        "Estate": [Card("Estate", "Victory", 2, v_points=1) for _ in range(12)],
                        "Duchy": [Card("Duchy", "Victory", 5, v_points=3) for _ in range(12)],
                        "Providence": [Card("Providence", "Victory", 8, v_points=6) for _ in range(12)],
                        "Curse": [Card("Curse", "Curse", 0, v_points=-1) for _ in range(10)],
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

    def display_player(self, player):
        return f'Player:   {self.players[player].name}\n' \
               f'DrawPile: {self.players[player].deck}\n' \
               f'Hand:     {self.players[player].hand}\n' \
               f'Discard:  {self.players[player].discard}\n' \
               f'PlayArea: {self.players[player].play_area}'

    def display_board(self):
        my_string = []
        my_string.append(f' {len(self.decks["Copper"])}{self.decks["Copper"][0].name}  '
                         f' {len(self.decks["Silver"])}{self.decks["Silver"][0].name}  '
                         f' {len(self.decks["Gold"])}{self.decks["Gold"][0].name}   ')

        my_string.append(f' {len(self.decks["Estate"])}{self.decks["Estate"][0].name} '
                         f'  {len(self.decks["Duchy"])}{self.decks["Duchy"][0].name} '
                         f'   {len(self.decks["Providence"])}{self.decks["Providence"][0].name}')
        my_string.append("                                  ")
        current_max = 0
        current_min = 10
        for b in self.card_choices:
            if b.cost > current_max:
                current_max = b.cost
            if b.cost < current_min:
                current_min = b.cost
        print(current_min, current_max)
        my_answer = {}
        for value in range(current_min, current_max + 1):
            my_answer[value] = f"\t"
            for card in self.card_choices:
                if card.cost == value:
                    my_answer[value] +=  str(len(self.decks[card.name])) + str(card.name) + " \t"
        print(my_answer)

        # current_string = my_string[0] + "\n" + my_string[1]
        current_string = ""
        for my_number, value in enumerate(range(current_min, current_max + 1)):
            current_string += my_string[my_number] + my_answer[value] + "\n"
        return current_string


def my_method(s):
    return s


def main():
    my_choice = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                 "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
    my_board = MyGame(my_choice)
    print(my_board.players[0].number)
    print(my_board.decks)
    print(my_board.discard)
    print(repr(my_board.players))
    print(my_board.players)
    my_card = Card("Copper", "Treasure")
    # my_board.populate_deck()
    for card in my_board.decks:
        print(card)
    print(my_card)
    print("ABC")
    print(my_board.display_board())


if __name__ == "__main__":
    main()
