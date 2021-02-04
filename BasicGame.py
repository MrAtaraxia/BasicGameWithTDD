#!/usr/bin/env python
"""
A Basic setup for a Basic Game.
Mostly going through it in a TDD method
To get practice with it.
"""

import random
from typing import List, Tuple, Set, Dict, Union

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
                 action: str = None, description: str = None, value: int = 0, v_points: int = 0) -> None:
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
    the_deck = [[Card("Copper", "Treasure", 0, value=1), "60"], [Card("Silver", "Treasure", 3, value=2), "40"],
                [Card("Gold", "Treasure", 6, value=3), "30"], [Card("Estate", "Victory", 2, v_points=1), "12"],
                [Card("Duchy", "Victory", 5, v_points=3), "12"], [Card("Providence", "Victory", 8, v_points=6), "12"],
                [Card("Curse", "Curse", 0, v_points=-1), "((len(self.players) - 1) * 10)"],
                [Card("Trash", "Trash"), "0"]]
    return the_deck


def selection_deck() -> List[List[Union[Card, str]]]:
    base_game = [[Card("Cellar", "Action", 2, None,
                       """
                      +1 Actions
                      Discard any number of cards.
                      +1 Card per card discarded.
                      """), "10"],
                 [Card("Chapel", "Action", 2, None,
                       """
                      Trash up to 4 cards from your hand.
                      """), "10"],
                 [Card("Moat", "Action - Reaction", 2, None,
                       """
                      +2 Cards
                      ---
                      When another player plays an Attack
                      card, you may reveal this card from your 
                      hand. If you do, you are unaffected
                      by the attack.
                      """), "10"],
                 [Card("Chancellor", "Action", 3, None,
                       """
                      +2 Gold
                      You may immediately put your 
                      deck into your discard pile.
                      """), "10"],
                 [Card("Village", "Action", 3, None,
                       """
                      +1 Card
                      +2 Actions
                      """), "10"],
                 [Card("Woodcutter", "Action", 3, None,
                       """
                      +1 Buy
                      +2 Coins
                      """), "10"],
                 [Card("Workshop", "Action", 3, None,
                       """
                       Gain a card costing up to 4 Coins.
                      """), "10"],
                 [Card("Feast", "Action", 4, None,
                       """
                      Trash this card.
                      Gain a card costing up to 5.
                      """), "10"],
                 [Card("Garden", "Victory", 4, None,
                       """
                      Worth 1VP
                      for every 10 cards
                      in your deck (rounded down).
                      """), "12"],
                 [Card("Militia", "Action - Attack", 4,
                       """
                      self.coins += 2
                      if other_players.receive_attack():
                        other_players.hand_limit = 3
                      """,
                       """
                      +2 Coins
                      Each other player discards
                      down to 3 cards in his hand.
                      """), "10"],
                 [Card("Moneylender", "Action", 4, None,
                       """
                      Trash a Copper from your hand.
                      If you do +3 Coins.
                      """), "10"],
                 [Card("Remodel", "Action", 4, None,
                       """
                      Trash a card from your hand.
                      Gain a card costing up to 2 Coins more
                      than the trashed card. 
                      """), "10"],
                 [Card("Smithy", "Action", 4,
                       """self.draw_cards(3)""",
                       """
                      +3 Cards
                      """), "10"],
                 [Card("Spy", "Action - Attack", 4, None,
                       """
                      +1 Card
                      +1 Action
                      Each player (including you) reveals
                      the top card of his deck and either
                      discards it or puts it back, your choice.
                      """), "10"],
                 [Card("Thief", "Action - Attack", 4, None,
                       """
                      Each other player reveals the top 
                      2 cards of his deck.
                      If they reveal any Treasure cards,
                      they trash one of them that you choose.
                      You may gain any or all of these 
                      trashed cards. They discard the 
                      other revealed cards.
                      """), "10"],
                 [Card("Throne Room", "Action", 4, None,
                       """
                      Choose an Action card in your hand.
                      Play it twice.
                      """), "10"],
                 [Card("Council Room", "Action", 5, None,
                       """
                      +4 Cards
                      +1 Buy
                      Each other player draws a card.
                      """), "10"],
                 [Card("Festival", "Action", 5,
                       """
                      self.actions += 2
                      self.buys += 1
                      self.coins += 2
                      """,
                       """
                      +2 Actions
                      +1 Buy
                      +2 Coins
                      """), "10"]]
    return base_game


class Player:

    def __init__(self, player_number: int = None,
                 player_name: str = None, color: str = None) -> None:
        self.number = player_number
        self.name = player_name
        self.color = color
        self.score = 0
        self.turn_order = None
        self.cards, self.hand, self.deck, self.discard, self.set_aside = [], [], [], [], []
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
        self.cards = []
        if self.game:
            self.cards.extend([self.game.decks["Copper"] for _ in range(7)])
            self.cards.extend([self.game.decks["Estate"] for _ in range(3)])
        else:
            default = default_decks()
            for card in default:
                if card[0].name == "Copper":
                    self.cards.extend([card[0] for _ in range(7)])
                if card[0].name == "Estate":
                    self.cards.extend([card[0] for _ in range(3)])
        self.deck = self.cards.copy()

    def draw_cards(self, number) -> None:
        try:
            for _ in range(number):
                self.hand.append(self.deck.pop(0))
        except IndexError:
            print("You can not draw a card from an empty deck.")

    def discard_cards(self, number: int = None) -> None:
        """
        Not RANDOM YET!
        Not selecting card yet.
        just removing 1 card for now!
        NO CHECKING YET!
        :param number: The number of cards. None == Discard ALL CARDS!
        :return: None
        """
        # discard all cards if None.
        if number is None:
            number = len(self.hand)
        # Can only discard up to the number of cards you have in your hand.
        if number > len(self.hand):
            number = len(self.hand)
        for _ in range(number):
            self.discard.append(self.hand.pop(0))

    def discard_to_deck(self) -> None:
        """
        Combines the discard pile to the deck.
        """
        # Adding a SHUFFLE here in the stupid case I don't shuffle later.
        # SHOULD this be needed, no, but more shuffling is better than NO shuffling!
        random.shuffle(self.discard)
        for _ in range(len(self.discard)):
            self.deck.append(self.discard.pop(0))

    def shuffle_deck(self) -> None:
        """
        Shuffles the players deck.
        :return: None
        """
        random.shuffle(self.deck)

    def play_card(self, number: int) -> None:
        """
        :param number: the number of the location of the card that is being played.
        """
        try:
            # print(self.hand[number].card_type)
            if str(self.hand[number].card_type) == "Action" or \
                    str(self.hand[number].card_type) == "Action Attack":
                self.play_area["cards"].append(self.hand.pop(number))
            else:
                raise AttributeError("That card is not playable!")

        except IndexError:
            print("You can not play a card from an empty hand.")

    def gain_coins(self) -> None:
        for card in self.hand:
            self.coins += card.value

    def gain_card(self, card: Card, where: str = "discard") -> None:
        if where == "discard":
            self.discard.append(self.game.decks[card][1].pop(0))
        elif where == "hand":
            self.hand.append(self.game.decks[card][1].pop(0))

    def buy_card(self, card: Card) -> None:
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
        self.game.decks["Trash"][1].append(self.hand.pop(card_number))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> hash:
        return hash(self.name)

    def __str__(self) -> str:
        return f'Player:{self.name}'

    def __repr__(self) -> str:
        return f'Player(number{self.number}, my_name={self.name}, color={self.color})'


class GameBoard:
    def __init__(self, name=None) -> None:
        self.name = name
        self.locations = None


class MyGame:
    def __init__(self, choices: List[str] = None, players: List[Player] = None) -> None:
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
            if card[0].name.lower() in choices:
                card_choices.append(card)
        if len(card_choices) == 10:
            self.card_choices = card_choices
        else:
            card_choices = []
            choices = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                       "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
            for card in my_deck:
                if card[0].name.lower() in choices:
                    print(card[0], card[1])
                    card_choices.append([card, [card[0] for _ in range(eval("10"))]])
            self.card_choices = card_choices

        self.first_player = 0
        self.active_player = self.first_player
        self.decks = self.setup_decks(self.card_choices)
        self.resources = {}
        # self.setup_decks()
        # self.discard = []
        self.game_log = []

        self.game_board = GameBoard("Game")
        self.mark_active_player()

    def __repr__(self) -> str:
        return f"MyGame({self.players})"

    def setup_decks(self, card_choices) -> Dict[str, Union[List[List[Union[Card, str]]], List[Card]]]:
        current_deck = {}
        default_deck = default_decks()
        for cards in card_choices:
            print(cards)
            current_deck[str(cards[0])] = [cards, [cards[0] for _ in range(eval(cards[1]))]]
        for cards in default_deck:
            current_deck[str(cards[0])] = [cards, [cards[0] for _ in range(eval(cards[1]))]]
        return current_deck

    def mark_active_player(self) -> None:
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

    def next_player(self) -> None:
        self.active_player = (self.active_player + 1) % len(self.players)
        self.mark_active_player()

    def display_player(self, player) -> str:
        return f'Player:   {self.players[player].name}\n' \
               f'DrawPile: {self.players[player].deck}\n' \
               f'Hand:     {self.players[player].hand}\n' \
               f'Discard:  {self.players[player].discard}\n' \
               f'PlayArea: {self.players[player].play_area}'

    def display_board(self) -> str:
        my_string = []
        my_string.append(f'{len(self.decks["Copper"][1])}Copper({self.decks["Copper"][0][0].cost})  '
                         f'{len(self.decks["Silver"][1])}Silver({self.decks["Silver"][0][0].cost})  '
                         f'{len(self.decks["Gold"][1])}Gold({self.decks["Gold"][0][0].cost})       ')

        my_string.append(f'{len(self.decks["Estate"][1])}Estate ({self.decks["Estate"][0][0].cost})'
                         f' {len(self.decks["Duchy"][1])}Duchy({self.decks["Duchy"][0][0].cost}) '
                         f'  {len(self.decks["Providence"][1])}Providence({self.decks["Providence"][0][0].cost}) ')
        my_string.append(f' {len(self.decks["Trash"][1])}{self.decks["Trash"][0][0].name}'
                         f'                                   ')
        current_max = 0
        current_min = 10
        print(self.card_choices)
        for b in self.card_choices:
            print(b[0].cost)
            if b[0].cost > current_max:
                current_max = b[0].cost
            if b[0].cost < current_min:
                current_min = b[0].cost
        print(current_min, current_max)
        my_answer = {}
        for value in range(current_min, current_max + 1):
            my_answer[value] = f""
            for card in self.card_choices:
                if card[0].cost == value:
                    my_answer[value] += f'{str(len(self.decks[card[0].name][1]))}{str(card[0].name)}({str(card[0].cost)})  \t'
        print(my_answer)

        # current_string = my_string[0] + "\n" + my_string[1]
        current_string = ""
        for my_number, value in enumerate(range(current_min, current_max + 1)):
            current_string += my_string[my_number] + my_answer[value] + "\n"
        return current_string

    def display_log(self) -> str:
        the_log = ""
        for current_log in self.game_log:
            the_log += current_log
        return the_log


def my_method(s):
    return s


def main() -> None:
    my_choice = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                 "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
    my_board = MyGame(my_choice)
    print(my_board.players[0].number)
    print(my_board.decks)
    print(my_board.decks["Trash"])
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
