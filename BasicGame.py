#!/usr/bin/env python
"""
A Basic setup for a Basic Game.
Mostly going through it in a TDD method
To get practice with it.
"""

import random
from typing import List, Dict, Union

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
                 player_name: str = None, color: str = None, pronoun: str = "he") -> None:
        self.number = player_number
        self.name = player_name
        self.color = color
        self.score = 0
        self.pronoun = pronoun
        if self.pronoun == "he":
            self.owner_pronoun = "his"
        elif self.pronoun == "she":
            self.owner_pronoun = "her"
        elif self.pronoun == "it":
            self.owner_pronoun = "its"
        self.turn_order = None
        self.cards, self.hand, self.deck, self.graveyard, self.set_aside, self.discards = [], [], [], [], [], []
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

    def organize_discards(self):
        print("ORGANIZE THE CARDS!")
        if self.game:
            self.game.game_log.append(f"{self.name} is organizing {self.owner_pronoun} discarded cards.")

    def discards_to_graveyard(self):
        # reorder the discards.
        self.organize_discards()
        # Put the discards on top of the GraveYard
        for card in self.discards:
            self.graveyard.append(self.discards.pop(0))

    def increase_score(self, amount: int) -> None:
        self.score += amount
        self.game.game_log.append(f"{self.name}'s score has increased by {amount} to {self.score}.")

    def decrease_score(self, amount: int) -> None:
        self.score -= amount
        self.game.game_log.append(f"{self.name}'s score has decreased by {amount} to {self.score}.")

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
        if self.game:
            self.game.game_log.append(f"{self.name}'s deck has been created.")

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
            self.discards.append(self.hand.pop(0))

    def discard_to_deck(self) -> None:
        """
        Combines the discard pile to the deck.
        """
        # Adding a SHUFFLE here in the stupid case I don't shuffle later.
        # SHOULD this be needed, no, but more shuffling is better than NO shuffling!
        random.shuffle(self.graveyard)
        for _ in range(len(self.graveyard)):
            self.deck.append(self.graveyard.pop(0))

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
                if self.game:
                    self.game.game_log.append(f"""{self.name} plays card {self.play_area['cards'][-1]}.""")
            else:
                raise AttributeError("That card is not playable!")

        except IndexError:
            print("You can not play a card from an empty hand.")

    def gain_coins(self) -> None:
        for card in self.hand:
            self.coins += card.value
            if self.game:
                self.game.game_log.append(f"{self.name}'s coins are now {self.coins}.")

    def gain_card(self, card: Card, where: str = "discard") -> None:
        if where == "discard":
            self.graveyard.append(self.game.decks[str(card)][1].pop(0))
            if self.game:
                self.game.game_log.append(f"{self.name}' gained card {str(card)}.")
        elif where == "hand":
            self.hand.append(self.game.decks[str(card)][1].pop(0))
            if self.game:
                self.game.game_log.append(f"{self.name}' gained card {str(card)} to their hand.")

    def buy_card(self, card: Card) -> None:
        if self.coins >= card.cost and self.buys >= 1:
            self.gain_card(card)
            self.buys -= 1
            self.coins -= card.cost
            if self.game:
                self.game.game_log.append(f"{self.name} bought card {str(card)} for {card.cost}.")
        else:
            raise ValueError("You do not have enough coins to buy that card!")

    def clean_up(self) -> None:
        # THIS NEEDS TO BE WORKED ON... SO MUCH TO DO HERE... UGH...
        # IT NEEDS to
        for _ in range(len(self.play_area["cards"])):
            self.graveyard.append(self.play_area["cards"].pop(0))
        self.discard_cards()

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

    def card_hand_to_aside(self, card_number) -> None:
        self.set_aside.append(self.hand.pop(card_number))

    def card_aside_to_hand(self, card_number) -> None:
        self.hand.append(self.set_aside.pop(card_number))

    def start_game(self) -> None:
        self.create_deck()
        self.shuffle_deck()
        self.draw_cards(5)
        self.score = 0
        self.resources = {}
        self.buys = 0
        self.play_area = {"cards": [], "resources": {}}
        self.coins = 0


class GameBoard:
    def __init__(self, name=None) -> None:
        self.name = name
        self.locations = None


class MyGame:
    def __init__(self, choices: List = None, players: List[Player] = None) -> None:
        self.game_log = []

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

        self.game_board = GameBoard("Game")
        self.mark_active_player()
        self.game_log.append("Game Start!")

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
            else:
                player.is_active_player = False
        self.game_log.append(f"It is {self.players[self.active_player].name}'s turn.")

    def setup_turn(self):
        for player in self.players:
            if player.is_active_player:
                player.actions = 1
                player.buys = 1
                player.coins = 0
                self.game_log.append(f"""{player.name} has {player.actions} actions and {player.buys} buys.""")

    def end_turn(self):
        for player in self.players:
            if player.is_active_player:
                player.actions = 0
                player.buys = 0
                player.coins = 0
                player.clean_up()
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
        for b in self.card_choices:
            if b[0].cost > current_max:
                current_max = b[0].cost
            if b[0].cost < current_min:
                current_min = b[0].cost
        my_answer = {}
        for value in range(current_min, current_max + 1):
            my_answer[value] = f""
            for card in self.card_choices:
                if card[0].cost == value:
                    my_answer[value] += f'{str(len(self.decks[card[0].name][1]))}' \
                                        f'{str(card[0].name)}({str(card[0].cost)})  \t'

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

    def start_the_game(self):
        for player in self.players:
            player.start_game()
            self.mark_active_player()
            self.setup_turn()



def my_method(s):
    return s


def main() -> None:
    my_choice = ["Cellar", "Remodel", "Moneylender", "Militia", "Village",
                 "Woodcutter", "Moat", "Feast", "Chapel", "Chancellor"]
    ted = Player(1, "Ted", "Red")
    chris = Player(2, "Chris", "Blue")
    my_board = MyGame(my_choice, [ted, chris])
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
