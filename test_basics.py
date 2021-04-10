#

"""
test_basics.py
yep...

"""

import pytest
import BasicGame
from Card import Card


def test_basic_things_my_method():
    assert BasicGame.my_method("a") == "a"
    assert BasicGame.my_method(1) == 1


@pytest.fixture
def cop_fixture():
    my_card = Card("Copper", "Treasure", 0, value=1)
    return my_card


@pytest.fixture
def p_bob():
    """
    This is BOB. He is a player of the game.
    Does THIS docstring get shown?
    YES yes it does!
    """
    bob = BasicGame.Player(10, "bob", "red")
    return bob


@pytest.fixture
def p_chris():
    """
    This is BOB. He is a player of the game.
    Does THIS docstring get shown?
    YES yes it does!
    """
    chris = BasicGame.Player(20, "chris", "blue")
    return chris


@pytest.fixture
def p_ted():
    """
    This is BOB. He is a player of the game.
    Does THIS docstring get shown?
    YES yes it does!
    """
    ted = BasicGame.Player(30, "ted", "green")
    return ted


@pytest.fixture
def game_2_p(p_bob, p_chris):
    """
    2 Player Game. Not sure if I want this as a fixture or not.
    """
    game = BasicGame.Game(players=[p_bob, p_chris])
    return game


@pytest.fixture
def game_3_p(p_bob, p_chris, p_ted):
    """
    3 Player Game. Not sure if I want this as a fixture or not.
    """
    game = BasicGame.Game(players=[p_bob, p_chris, p_ted])
    return game


@pytest.fixture
def card_dict():
    my_list = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Providence"]
    my_dict = {}
    my_select = BasicGame.selection_deck()
    for _ in my_select:
        if _[0].name in my_list:
            my_dict[_[0].name] = _
    return my_dict


def test_errors():
    """
    A Test to check how things work with errors.
    To be used more later!
    """
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("value must be 42")
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "value must be 42"


def test_a_player_exist(p_bob, cop_fixture):
    """A Test to see if the player module works
    together with the the pytest fixture."""
    my_player = BasicGame.Player(10, "bob", "red")
    my_player.hand.append(cop_fixture)
    assert my_player == p_bob
    p_bob.hand.append("Copper")
    assert len(p_bob.hand) > 0
    assert p_bob.hand[0] == "Copper"
    assert my_player.number == 10
    assert my_player.color == "red"
    assert cop_fixture.name in p_bob.hand
    assert cop_fixture in p_bob.hand


def test_a_game_exists():
    """
    A Test to check if the MyGame works as intended.
    :return: None
    """
    my_game = BasicGame.Game(["Bridge"], [BasicGame.Player(10)])
    assert my_game.players[0].name is None
    assert my_game.game_board.name == "Game"


# DONE - Added cards.

def test_cards_exist(cop_fixture):
    """ Test to make su that the cards are callable."""
    my_card = cop_fixture
    assert my_card.name == "Copper"


# -------------------------------------------------------
def test_game_deck():
    """
    The CURRENT Basic Setup of the game!
    I will change this later!
    """
    selection = BasicGame.selection_deck()
    local_game = BasicGame.Game(selection)
    assert len(local_game.decks["Copper"]) > 0
    assert len(local_game.decks["Trash"][1]) == 0
    assert local_game.players[0].name == "Bob"
    assert local_game.players[0].color == "Red"
    assert len(local_game.players[0].hand) == 0


# -------------------------------------------------------
def test_player_score_actions(p_bob, p_chris):
    my_game = BasicGame.Game(players=[p_bob, p_chris])
    p_bob.increase_score(5)
    assert p_bob.score == 5
    p_bob.decrease_score(5)
    assert p_bob.score == 0


# -------------------------------------------------------
def test_player_card_movements(p_bob, p_chris, p_ted):
    """
    Testing all of the card movements that should be allowed by a player.
    Well there are special things like pass a card left/right.
    There also is - remove from game.
    Also - return to piles on game board.
    Also - have the trashed card go to the trash.
    Also - have the gained card actually come from a pile.
    Also - have a 'take an action' thing. Hmm...
    I have not added those to this.
    """

    p_bob.create_deck()
    assert len(p_bob.deck) == 10
    assert len(p_bob.hand) == 0
    p_bob.draw_cards(2)
    print(p_bob.hand)
    print(p_bob.deck)

    assert len(p_bob.hand) == 2
    assert len(p_bob.deck) == 8
    assert len(p_bob.graveyard) == 0
    p_bob.discard_cards(1)
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 8
    assert len(p_bob.graveyard) == 1
    p_bob.discard_to_deck()
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 9
    assert len(p_bob.graveyard) == 0
    my_game = BasicGame.Game(players=[p_bob, p_chris, p_ted])
    p_bob.gain_card(BasicGame.Card("Cellar", "Action"), "hand")
    p_bob.play_card(1)  # Card # not # of cards
    # Make sure you can not play a card that is not an action.
    with pytest.raises(AttributeError) as exc_info:
        p_bob.play_card(0)  # Card # not # of cards
    assert exc_info.type is AttributeError
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 9
    assert len(p_bob.graveyard) == 0
    assert len(p_bob.play_area["cards"]) == 1
    p_bob.clean_up()
    assert len(p_bob.hand) == 0
    assert len(p_bob.deck) == 9
    assert len(p_bob.graveyard) == 2
    assert len(p_bob.play_area["cards"]) == 0
    p_bob.discard_cards(1)
    assert len(p_bob.hand) == 0
    assert len(p_bob.deck) == 9
    assert len(p_bob.graveyard) == 2
    assert len(p_bob.play_area["cards"]) == 0
    p_bob.draw_cards(1)
    p_bob.trash_card(0)
    assert len(p_bob.hand) == 0
    assert len(p_bob.deck) == 8
    assert len(p_bob.graveyard) == 2
    assert len(p_bob.play_area["cards"]) == 0
    assert len(my_game.decks["Trash"][1]) == 1


# -------------------------------------------------------
def test_basic_game_round(p_bob, p_chris, p_ted):
    """
    Test a basic game round.
    """
    my_game = BasicGame.Game(players=[p_bob, p_chris, p_ted])
    my_game.start_the_game()
    my_game.display_player(0)
    assert len(p_bob.hand) == 5
    assert len(p_chris.hand) == 5
    assert len(p_ted.hand) == 5
    my_game.next_player()
    assert False


# -------------------------------------------------------
def test_setting_cards_aside(p_bob, p_chris, p_ted):
    """
    Testing the setting cards aside action.
    """

    my_game = BasicGame.Game(players=[p_bob, p_chris, p_ted])
    p_bob.create_deck()
    p_bob.draw_cards(5)
    p_bob.card_hand_to_aside(0)
    assert len(p_bob.set_aside) == 1
    assert len(p_bob.hand) == 4
    p_bob.card_aside_to_hand(0)
    assert len(p_bob.set_aside) == 0
    assert len(p_bob.hand) == 5


# -------------------------------------------------------
def test_overdraw_card_movements(capsys, p_bob):
    """
    testing overdrawing cards.
    """
    p_bob.draw_cards(1)
    assert capsys.readouterr().out == "You can not draw a card " \
                                      "from an empty deck.\n"
    p_bob.play_card(0)
    assert capsys.readouterr().out == "You can not play a card " \
                                      "from an empty hand.\n"
    assert len(p_bob.play_area["cards"]) == 0


# -------------------------------------------------------
def test_player_card_shuffling(p_bob):
    """
    testing player cards.
    """
    p_bob.create_deck()
    my_deck = p_bob.deck.copy()
    p_bob.shuffle_deck()
    assert my_deck != p_bob.deck


# -------------------------------------------------------
def test_setting_up_the_cards_on_the_board(game_2_p):
    assert game_2_p.game_board.name == "Game"
    assert len(game_2_p.decks["Copper"][1]) == 60
    assert len(game_2_p.decks["Silver"][1]) == 40
    assert len(game_2_p.decks["Gold"][1]) == 30
    assert len(game_2_p.decks["Estate"][1]) == 12
    assert len(game_2_p.decks["Duchy"][1]) == 12
    assert len(game_2_p.decks["Providence"][1]) == 12
    assert len(game_2_p.decks["Curse"][1]) == 10
    assert len(game_2_p.decks["Trash"][1]) == 0


# -------------------------------------------------------
def test_active_player(p_bob, p_chris):
    my_game = BasicGame.Game(["Church"], [p_bob, p_chris])
    assert my_game.players[0].is_active_player
    my_game.next_player()
    assert my_game.players[1].is_active_player
    my_game.players[0].actions = 0
    my_game.next_player()
    assert my_game.players[0].is_active_player
    assert my_game.players[0].actions == 1
    assert my_game.players[0].buys == 1


# -------------------------------------------------------
def test_player_game_attaches(p_bob, p_chris):
    my_game = BasicGame.Game(["Church"], [p_bob, p_chris])
    assert my_game.players[0].game == my_game


# -------------------------------------------------------
def test_players_buys(p_bob, p_chris):
    """
    I have to actually add costs to continue this...
    That is going to be a bit of a thing.
    THIS SHOULD NOT WORK...
    """
    my_game = BasicGame.Game(["Church"], [p_bob, p_chris])
    with pytest.raises(ValueError) as exc_info:
        my_game.players[0].buy_card(BasicGame.Card("Church", "Action"))
    assert exc_info.type == ValueError
    assert exc_info.value.args[0] == "You do not have enough " \
                                     "coins to buy that card!"


# -------------------------------------------------------
def test_different_cards():
    my_game = BasicGame.Game()
    chosen_cards = 10
    vp_cards = 3
    treasure_cards = 3
    curse_cards = 1
    trash_card = 1
    sum_of_cards = chosen_cards + vp_cards \
                                + treasure_cards \
                                + curse_cards \
                                + trash_card
    print(my_game.decks)
    print(my_game.card_choices)
    assert len(my_game.decks) == sum_of_cards


# -------------------------------------------------------
def test_basic_player_graphic():
    my_game = BasicGame.Game()
    my_game.players[0].create_deck()
    assert "Copper" in my_game.display_player(0)


# -------------------------------------------------------
def test_basic_board_graphic():
    my_game = BasicGame.Game()
    assert "Copper" in my_game.display_board()


# -------------------------------------------------------
def test_basic_game_log():
    my_game = BasicGame.Game()
    assert "Game Start" in my_game.display_log()


# -------------------------------------------------------
def test_write_more_tests():
    """
    TODO - Write more tests!
    """
    assert False
