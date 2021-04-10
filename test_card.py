#!/usr/bin/env python
"""
test_card.py
The testing card Class.

"""


import pytest
import BasicGame
from Card import Card


@pytest.fixture
def cop_fixture():
    my_card = Card("Copper", "Treasure", 0, value=1)
    return my_card


def test_equal(cop_fixture):
    assert cop_fixture == Card("Copper", "Treasure", 0, value=1)


def test_int(cop_fixture):
    assert int(cop_fixture) + 5 == 5


def test_gt(cop_fixture):
    new_card = Card("Copper", "Treasure", 1, value=1)
    assert new_card > cop_fixture


def test_str(cop_fixture):
    name = ""
    assert str(cop_fixture) + name == "Copper"
