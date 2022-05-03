"""
This module allows you to run simulations of the game of Craps in
order to test strategies and collect data on the outcomes of those
strategies.
"""

__all__ = ["table", "player", "dice", "strategy", "bet"]

from crapssim.dice import Dice
from crapssim.player import Player
from crapssim.table import Table
from . import bet
from . import strategy
