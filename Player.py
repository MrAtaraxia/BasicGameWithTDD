#!/usr/bin/env python
"""
Player.py
The Basic Player Class.

"""
import random
from Card import Card, default_decks


class Player:

    def __init__(self, player_number: int = None,
                 player_name: str = None, color: str = None, pronoun: str = "he") -> None:
        self.number = player_number
        self.name = player_name
        self.color = color
        self.score = 0
        self.draw_size = 5
        self.hand_limit = 25
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
        for _ in self.discards:
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
        self.discards_to_graveyard()

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
        self.draw_cards(self.draw_size)
        self.score = 0
        self.resources = {}
        self.buys = 0
        self.play_area = {"cards": [], "resources": {}}
        self.coins = 0


if __name__ == "__main__":
    pass
