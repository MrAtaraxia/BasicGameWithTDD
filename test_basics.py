# test_basics.py
"""
A Basic setup for testing BasicGame.py

2020.01.28 - I think this is coming along nicely.
It has only been 2 days, I think.
I almost have it all set to actually be at the 'start of game' condition.
I do like doing TDD!
I don't know the whole "do it with someone else" mentality though.
I will have to look into that more.

"""

import pytest
import BasicGame


def test_basic_things_my_method():
    assert BasicGame.my_method("a") == "a"
    assert BasicGame.my_method(1) == 1


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
def game_for_testing(p_bob, p_chris):
    """
    Ok So this will be used as a general game thing.
    Would bob be modifiable from p_bob
    while using this or not... hmmm...
    I will have to look into that more later.
    """
    game = BasicGame.MyGame(["Bridge"], [p_bob, p_chris])
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


@pytest.fixture
def cop_fixture():
    my_card = BasicGame.Card("Copper", "Treasure", 0, value=1)
    return my_card


def test_errors():
    """
    A Test to check how things work with errors. To be used more later!
    """
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("value must be 42")
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "value must be 42"


def test_a_player_exist(p_bob, cop_fixture):
    """A Test to see if the player module works together with the the pytest fixture."""
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
    my_game = BasicGame.MyGame(["Bridge"], [BasicGame.Player(10)])
    assert my_game.players[0].name is None
    assert my_game.game_board.name == "Game"


# DONE - Added cards.

def test_cards_exist(cop_fixture):
    """ Test to make su that the cards are callable."""
    my_card = cop_fixture
    assert my_card.name == "Copper"


# TODO - What other things do I want to add to this?
# DONE - Add a method to add cards to your hand.
# DONE - Add a list of cards.
# DONE - Add more than 1 player, Added as a list so allows multiple players
# dev()
# help()
# DONE - For this game, I could probably use a dict...
# DONE - But if I want to keep track of order in general
#  for the draw pile on the game board I would probably
#  want to keep it as an array.
# I USED A DICT of arrays!!! I think it will work out nicely. or at least I hope so.

# Done - Add a take turn method to the game. (might need more players first)
# Well it is an 'active player' method but yeah. It rotates at least!
# DONE Add 10 selected decks.
# TODO - Finish setting up the beginning of the game:
#  reverse the players and cards... yeah I probably should.
#  Add more players.
#  Make card count for certain cards vary depending on players like it is supposed to.
#  (ex Curses is (Players -1) * 10 and VP cards are different for lower counts.)
#  Add dealing original cards to players?
# TODO - Setup the players having actions on their turns.
#  Make the turns go in turn order.
#  Make each turn have the correct phases (Actions / Buy / Cleanup)
#  Figure out what I want to do about the other parts other sets added.
# TODO - Add card actions!
#  THIS will take a LONG time. I think.
#  Mostly because I think I will have issues with edge cases causing me problems.
# TODO - What does it need to be able to set up a game?
# TODO - What else?
#  Add ability to select the 10 cards. (probably a lot later!)
#  Add ability to select the sets to play from (A LOT LATER)
# TODO - Add Graphics (FAR FAR FAR in the future! Once working from cmd line!)
# TODO - Look up how to move around better with the mouse in
# TODO - Pycharm
# TODO - AND Bash Shell. How to move up and down especially. Shift PgUp/Down but less
# TODO -
# TODO - OK for future, I MIGHT try and do it as followed:
# TODO - Make the (Game) and make it so it is setup as it starts.
# TODO - THEN do all the other things, like players AFTERWARDS!
# I have a lot of cleaning up to do later... yeah... BUT I will get more important things
# working FIRST!

# -------------------------------------------------------
def test_game_deck():
    """
    The CURRENT Basic Setup of the game!
    I will change this later!
    """
    selection = BasicGame.selection_deck()
    local_game = BasicGame.MyGame(selection)
    assert len(local_game.decks["Copper"]) > 0
    assert len(local_game.decks["Trash"][1]) == 0
    assert local_game.players[0].name == "Bob"
    assert local_game.players[0].color == "Red"
    assert len(local_game.players[0].hand) == 0


# -------------------------------------------------------
def test_player_score_actions(p_bob):
    p_bob.increase_score(5)
    assert p_bob.score == 5
    p_bob.decrease_score(5)
    assert p_bob.score == 0


# -------------------------------------------------------
def test_player_card_movements(p_bob):
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
    assert len(p_bob.discard) == 0
    p_bob.discard_cards(1)
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 8
    assert len(p_bob.discard) == 1
    p_bob.discard_to_deck()
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 9
    assert len(p_bob.discard) == 0
    my_game = BasicGame.MyGame([], [p_bob])
    p_bob.gain_card("Cellar", "hand")
    p_bob.play_card(1)  # Card # not # of cards
    with pytest.raises(AttributeError) as exc_info:
        p_bob.play_card(0)  # Card # not # of cards
    assert exc_info.type is AttributeError
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 9
    assert len(p_bob.discard) == 0
    assert len(p_bob.play_area["cards"]) == 1
    p_bob.clean_up()
    assert len(p_bob.hand) == 1
    assert len(p_bob.deck) == 9
    assert len(p_bob.discard) == 1
    assert len(p_bob.play_area["cards"]) == 0
    p_bob.discard_cards(1)
    assert len(p_bob.hand) == 0
    assert len(p_bob.deck) == 9
    assert len(p_bob.discard) == 2
    assert len(p_bob.play_area["cards"]) == 0
    p_bob.draw_cards(1)
    p_bob.trash_card(0)
    assert len(p_bob.hand) == 0
    assert len(p_bob.deck) == 8
    assert len(p_bob.discard) == 2
    assert len(p_bob.play_area["cards"]) == 0
    assert len(my_game.decks["Trash"][1]) == 1


# -------------------------------------------------------
def test_overdraw_card_movements(capsys, p_bob):
    """
    TODO - NEED TO ADD CHECKING FOR Overdrawing each type! ETC!
    TODO - Overdrawing Deck
    # Might get rid of overdrawing deck error.
    That is because you CAN do that in the game.
    and it should instead reshuffle the discard into the deck, after you draw all in the deck,
    and then draw from those cards.
    If those are not enough you just don't get any more cards. There is no error.
    Might change the function to that.
    TODO - Overdrawing Hand
    # Might adjust this one too. As you can try and discard a card, if it tells you to, when your hand is empty
    so I am not sure how I want to handle this one in the future either.
    TODO - Error handling for - Discarding from an empty hand
    Discarding from empty hand should just discard nothing... so hmm...
    Oh I could adjust discard cards to, if blank do all?
    Lets try that.
    TODO - Error handling for - Playing from an empty hand
    """
    p_bob.draw_cards(1)
    assert capsys.readouterr().out == "You can not draw a card from an empty deck.\n"
    #p_bob.discard_cards()
    #assert capsys.readouterr().out == "You can not discard a card from an empty hand.\n"
    p_bob.play_card(0)
    assert capsys.readouterr().out == "You can not play a card from an empty hand.\n"
    assert len(p_bob.play_area["cards"]) == 0

    # with pytest.raises(IndexError) as exc_info:
    # assert exc_info.type is IndexError
    # assert exc_info.value.args[0] == "pop from empty list"


# -------------------------------------------------------
def test_player_card_shuffling(p_bob):
    p_bob.create_deck()
    my_deck = p_bob.deck.copy()
    p_bob.shuffle_deck()
    assert my_deck != p_bob.deck


# -------------------------------------------------------
def test_setting_up_the_cards_on_the_board(game_for_testing):
    assert game_for_testing.game_board.name == "Game"
    assert len(game_for_testing.decks["Copper"][1]) == 60
    assert len(game_for_testing.decks["Silver"][1]) == 40
    assert len(game_for_testing.decks["Gold"][1]) == 30
    assert len(game_for_testing.decks["Estate"][1]) == 12
    assert len(game_for_testing.decks["Duchy"][1]) == 12
    assert len(game_for_testing.decks["Providence"][1]) == 12
    assert len(game_for_testing.decks["Curse"][1]) == 10
    assert len(game_for_testing.decks["Trash"][1]) == 0


# -------------------------------------------------------
def test_active_player(p_bob, p_chris):
    my_game = BasicGame.MyGame(["Church"], [p_bob, p_chris])
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
    my_game = BasicGame.MyGame(["Church"], [p_bob, p_chris])
    assert my_game.players[0].game == my_game


# -------------------------------------------------------
def test_players_buys(p_bob, p_chris):
    """
    I have to actually add costs to continue this...
    That is going to be a bit of a thing.
    THIS SHOULD NOT WORK...
    """
    my_game = BasicGame.MyGame(["Church"], [p_bob, p_chris])
    with pytest.raises(ValueError) as exc_info:
        my_game.players[0].buy_card(BasicGame.Card("Church", "Action"))
    assert exc_info.type == ValueError
    assert exc_info.value.args[0] == "You do not have enough coins to buy that card!"


# -------------------------------------------------------
def test_different_cards():
    my_game = BasicGame.MyGame()
    chosen_cards = 10
    vp_cards = 3
    treasure_cards = 3
    curse_cards = 1
    trash_card = 1
    sum_of_cards = chosen_cards + vp_cards + treasure_cards + curse_cards + trash_card
    print(my_game.decks)
    print(my_game.card_choices)
    assert len(my_game.decks) == sum_of_cards


# -------------------------------------------------------
def test_basic_player_graphic():
    my_game = BasicGame.MyGame()
    my_game.players[0].create_deck()
    assert "Copper" in my_game.display_player(0)


# -------------------------------------------------------
def test_basic_board_graphic():
    my_game = BasicGame.MyGame()
    assert "Copper" in my_game.display_board()


# -------------------------------------------------------
def test_basic_game_log():
    my_game = BasicGame.MyGame()
    assert "Game Start" in my_game.display_log()


# -------------------------------------------------------
def test_write_more_tests():
    """
    What does my Minimum Viable Product look like?
    What tests can/should I use to get there?
    What functionality do I want this to have at this stage?

    A Test to make it fail because there are need for more tests!
    :return: None
    Done - NEED TO SET it so GAME gives the starting cards, not the player!
    Not doing that! I looked at the rules and if the players are not playing those cards are not included
    So there is 'technically' no reason to give them to the game.
    It COULD allow me to have an easier time managing where cards are, but I will look into that later,
    If I even decide that I WANT that later.
    TODO - Check the type of all cards throughout to make sure they are all of type Cards?
    """
    assert False
