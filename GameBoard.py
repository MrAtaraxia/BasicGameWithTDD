#!/usr/bin/env python
"""
GameBoard.py
The Basic GameBoard Class.

"""


class GameBoard:
    def __init__(self, name=None) -> None:
        self.name = name
        self.locations = None
