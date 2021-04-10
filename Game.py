#!/usr/bin/env python
"""
Game.py
The Basic Game Class.

"""

from typing import List, Dict, Union
from Card import Card, default_decks
from GameBoard import GameBoard
from Player import Player


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


class Game:
    def __init__(self, choices: List = None, players: List[Player] = None) -> None:
        self.game_log = []

        if players is None:
            self.players = [Player(1, "Bob", "Red"),
                            Player(2, "Chris", "Blue")]
        else:
            self.players = players
        for player in self.players:
            player.game = self

        my_deck = selection_deck()
        card_choices = []
        if choices:
            choices = [str(x).lower() for x in choices]
        else:
            choices = ["cellar", "remodel",
                       "moneylender", "militia",
                       "village", "woodcutter",
                       "moat", "feast",
                       "chapel", "chancellor"]
        for card in my_deck:
            if card[0].name.lower() in choices:
                card_choices.append(card)
        if len(card_choices) == 10:
            self.card_choices = card_choices
        else:
            card_choices = []
            choices = ["Cellar", "Remodel",
                       "Moneylender", "Militia",
                       "Village", "Woodcutter",
                       "Moat", "Feast",
                       "Chapel", "Chancellor"]
            for card in my_deck:
                if card[0].name.lower() in choices:
                    print(card[0], card[1])
                    card_choices.append([card,
                                         [card[0] for _ in
                                          range(eval("10"))]])
            self.card_choices = card_choices

        self.first_player = 0
        self.active_player = self.first_player
        self.decks = self.setup_decks(self.card_choices)
        self.resources = {}

        self.game_board = GameBoard("Game")
        self.mark_active_player()
        self.game_log.append("Game Start!")

    def __repr__(self) -> str:
        return f"MyGame({self.players})"

    def setup_decks(self, card_choices) -> \
            Dict[str,
                 Union[List[List[Union[Card, str]]],
                       List[Card]]]:
        current_deck = {}
        default_deck = default_decks()
        for cards in card_choices:
            print(cards)
            current_deck[str(cards[0])] = \
                [cards, [cards[0] for _ in range(eval(cards[1]))]]
        for cards in default_deck:
            current_deck[str(cards[0])] = \
                [cards, [cards[0] for _ in range(eval(cards[1]))]]
        return current_deck

    def mark_active_player(self) -> None:
        """
        Setup the players turn and mark them as active player.
        """
        for player in self.players:
            if player == self.players[self.active_player]:
                player.is_active_player = True
            else:
                player.is_active_player = False
        self.game_log.\
            append(f"It is "
                   f"{self.players[self.active_player].name}'s turn.")

    def setup_turn(self):
        for player in self.players:
            if player.is_active_player:
                player.actions = 1
                player.buys = 1
                player.coins = 0
                self.game_log.append(f"{player.name} "
                                     f"has {player.actions} "
                                     f"actions and {player.buys} buys.")

    def end_turn(self):
        for player in self.players:
            if player.is_active_player:
                player.actions = 0
                player.buys = 0
                player.coins = 0
                player.clean_up()
                player.draw_cards(player.draw_size)
                self.game_log.append(f"""{player.name} turn has ended.""")

    def next_player(self) -> None:
        self.end_turn()
        self.active_player = (self.active_player + 1) % len(self.players)
        self.mark_active_player()
        self.setup_turn()

    def display_player(self, player) -> str:
        return f'Player:   {self.players[player].name}\n' \
               f'DrawPile: {self.players[player].deck}\n' \
               f'Hand:     {self.players[player].hand}\n' \
               f'Discard:  {self.players[player].graveyard}\n' \
               f'PlayArea: {self.players[player].play_area}'

    def display_board(self) -> str:
        my_string = []
        my_string.append(f'{len(self.decks["Copper"][1])}'
                         f'Copper({self.decks["Copper"][0][0].cost})  '
                         f'{len(self.decks["Silver"][1])}'
                         f'Silver({self.decks["Silver"][0][0].cost})  '
                         f'{len(self.decks["Gold"][1])}'
                         f'Gold({self.decks["Gold"][0][0].cost})       ')

        my_string.append(f'{len(self.decks["Estate"][1])}'
                         f'Estate ({self.decks["Estate"][0][0].cost})'
                         f' {len(self.decks["Duchy"][1])}'
                         f'Duchy({self.decks["Duchy"][0][0].cost}) '
                         f'  {len(self.decks["Providence"][1])}'
                         f'Providence('
                         f'{self.decks["Providence"][0][0].cost}) ')
        my_string.append(f' {len(self.decks["Trash"][1])}'
                         f'{self.decks["Trash"][0][0].name}'
                         f'                                   ')
        current_max = 0
        current_min = 10
        for b in self.card_choices:
            if b[0].cost > current_max:
                current_max = b[0].cost
            if b[0].cost < current_min:
                current_min = b[0].cost
        my_answer = {}
        for value in range(current_min, current_max + 1):
            my_answer[value] = ""
            for card in self.card_choices:
                if card[0].cost == value:
                    my_answer[value] += \
                        f'{str(len(self.decks[card[0].name][1]))}' \
                        f'{str(card[0].name)}({str(card[0].cost)})  \t'

        # current_string = my_string[0] + "\n" + my_string[1]
        current_string = ""
        for my_number, value in enumerate(range(current_min,
                                                current_max + 1)):
            current_string += my_string[my_number] + my_answer[value] + "\n"
        return current_string

    def display_log(self) -> str:
        the_log = ""
        for current_log in self.game_log:
            the_log += current_log
        return the_log

    def start_the_game(self):
        for player in self.players:
            player.start_game()
            self.mark_active_player()
            self.setup_turn()
