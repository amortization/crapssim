"""
This module contains classes for all the different types of
bets found on the Craps table. These bets are what get placed on the table
by a Player and are updated as the dice are rolled.
"""

import typing
from abc import ABC

from crapssim import Dice

if typing.TYPE_CHECKING:
    from crapssim.table import Table


class Bet(ABC):
    """
    A generic bet for the craps table

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet

    Attributes
    ----------
    bet_amount: typing.SupportsFloat
        Wagered amount for the bet
    name : string
        Name for the bet
    sub_name : string
        Sub-name, usually denotes number for a come/don't come bet
    winning_numbers : list
        Numbers to roll for this bet to win
    losing_numbers : list
        Numbers to roll that cause this bet to lose
    payout_ratio : typing.SupportsFloat
        Ratio that bet pays out on a win
    removable : bool
        Whether the bet can be removed or not
    can_be_placed_point_on : bool
        Whether the bet can be placed when the point is on
    can_be_placed_point_off : bool
        Whether the bet can be placed when the point is off
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        self.bet_amount: float = float(bet_amount)
        self.name: str = str()
        self.sub_name: str = str()
        self.winning_numbers: list[int] = []
        self.losing_numbers: list[int] = []
        self.payout_ratio: typing.SupportsFloat = float(1)
        self.removable: bool = True
        self.can_be_placed_point_on = True
        self.can_be_placed_point_off = True

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        """
        Returns whether the bet's status is win, lose or None and if win the amount won.

        Parameters
        ----------
        table : Table
            The table to check the bet was made on.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        status: str | None = self.get_status(table.dice)
        win_amount: float = self.get_win_amount(status)

        return status, win_amount

    def get_status(self, dice: Dice) -> str | None:
        """
        Get the status of the bet based on the dice. Either win, lose or None.

        Parameters
        ----------
        dice : Dice
            The Dice whose number(s) get the status.

        Returns
        -------
        str | None
            Either "win", "lose", or None as the status depending on the dice.
        """
        if dice.total in self.winning_numbers:
            return "win"
        if dice.total in self.losing_numbers:
            return "lose"
        return None

    def get_win_amount(self, status: str | None) -> float:
        """
        Gives the win amount based on the status of the dice.

        Parameters
        ----------
        status : str | None
            The bets status, either "win", "lose", or None.

        Returns
        -------
        float
            The amount of winnings of the bet.

        """
        if status is None or status == 'lose':
            return 0.0
        if status == 'win':
            return float(self.payout_ratio) * self.bet_amount
        raise NotImplementedError

# Pass Line and Come bets


class PassLine(Bet):
    """
    Bet placed on the Pass Line prior to the point being established.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet

    """
    def __init__(self, bet_amount: float):

        super().__init__(bet_amount)
        self.name: str = "PassLine"
        self.winning_numbers: list[int] = [7, 11]
        self.losing_numbers: list[int] = [2, 3, 12]
        self.payout_ratio: typing.SupportsFloat = 1.0
        self.pre_point: bool = True
        self.can_be_placed_point_on = False

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status: str | None = None
        win_amount: typing.SupportsFloat = 0.0

        if table.dice.total in self.winning_numbers:
            status = "win"
            win_amount = float(self.payout_ratio) * self.bet_amount
        elif table.dice.total in self.losing_numbers:
            status = "lose"
        elif self.pre_point:
            self.winning_numbers = [table.dice.total]
            self.losing_numbers = [7]
            self.pre_point = False
            self.removable = False

        return status, float(win_amount)


class Come(PassLine):
    """
    Bet placed on the Come after the point is established.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(float(bet_amount))
        self.name: str = "Come"
        self.can_be_placed_point_off = False
        self.can_be_placed_point_on = True

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status, win_amount = super().update_bet(table)
        if not self.pre_point and self.sub_name == "":
            self.sub_name = "".join(str(e) for e in self.winning_numbers)
        return status, win_amount


# Pass Line and Come Bet Odds

class Odds(Bet):
    """
    Bet placed with either a PassLine bet or Come bet that pays odds for the bet.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    bet_object : Bet
        Come or PassLine bet object to tie the Odds to.
    """
    def __init__(self, bet_amount: typing.SupportsFloat, bet_object: Bet):
        super().__init__(bet_amount)

        if not isinstance(bet_object, PassLine) and not isinstance(bet_object, Come):
            raise TypeError('bet_object must be either a PassLine or Come Bet.')
        if isinstance(bet_object, PassLine):
            self.can_be_placed_point_off = False

        self.name: str = "Odds"
        self.sub_name: str = "".join(str(e) for e in bet_object.winning_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.winning_numbers in [[4], [10]]:
            self.payout_ratio = 2 / 1
        elif self.winning_numbers in [[5], [9]]:
            self.payout_ratio = 3 / 2
        elif self.winning_numbers in [[6], [8]]:
            self.payout_ratio = 6 / 5


# Place Bets on 4,5,6,8,9,10

class Place(Bet):
    """
    Bet placed on a number after the point is established.
    """
    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        # place bets are inactive when point is "Off"
        if table.point == "On":
            return super().update_bet(table)
        return None, 0


class Place4(Place):
    """
    Place bet on the 4.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Place4"
        self.winning_numbers: list[int] = [4]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(9 / 5)


class Place5(Place):
    """
    Place bet on the 5.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Place5"
        self.winning_numbers: list[int] = [5]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(7 / 5)


class Place6(Place):
    """
    Place bet on the 6.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place6"
        self.winning_numbers: list[int] = [6]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(7 / 6)


class Place8(Place):
    """
    Place bet on the 8.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Place8"
        self.winning_numbers: list[int] = [8]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(7 / 6)


class Place9(Place):
    """
    Place bet on the 9.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Place9"
        self.winning_numbers: list[int] = [9]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(7 / 5)


class Place10(Place):
    """
    Place bet on the 10.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place10"
        self.winning_numbers: list[int] = [10]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = float(9 / 5)


# Field bet

class Field(Bet):
    """
    Parameters
    ----------
    double : list
        Set of numbers that pay double on the field bet (default = [2,12])
    triple : list
        Set of numbers that pay triple on the field bet (default = [])
    """

    def __init__(self, bet_amount: typing.SupportsFloat, double=None, triple=None):
        super().__init__(bet_amount)
        if triple is None:
            triple = []
        if double is None:
            double = [2, 12]
        self.name: str = "Field"
        self.double_winning_numbers: list[int] = double
        self.triple_winning_numbers: list[int] = triple
        self.winning_numbers: list[int] = [2, 3, 4, 9, 10, 11, 12]
        self.losing_numbers: list[int] = [5, 6, 7, 8]

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if table.dice.total in self.triple_winning_numbers:
            status = "win"
            win_amount = 3 * self.bet_amount
        elif table.dice.total in self.double_winning_numbers:
            status = "win"
            win_amount = 2 * self.bet_amount
        elif table.dice.total in self.winning_numbers:
            status = "win"
            win_amount = 1 * self.bet_amount
        elif table.dice.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


# Don't Pass and Don't Come bets

class DontPass(Bet):
    """
    Bet placed on the Don't Pass bar prior to the point being established.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "DontPass"
        self.winning_numbers: list[int] = [2, 3]
        self.losing_numbers: list[int] = [7, 11]
        self.push_numbers: list[int] = [12]
        self.payout_ratio: float = 1.0
        self.pre_point: bool = True
        self.can_be_placed_point_on = False

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if table.dice.total in self.winning_numbers:
            status = "win"
            win_amount = self.payout_ratio * self.bet_amount
        elif table.dice.total in self.losing_numbers:
            status = "lose"
        elif table.dice.total in self.push_numbers:
            status = "push"
        elif self.pre_point:
            self.winning_numbers = [7]
            self.losing_numbers = [table.dice.total]
            self.push_numbers = []
            self.pre_point = False

        return status, win_amount


class DontCome(DontPass):
    """
    Bet placed on the Don't Come bar prior to the point being established.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "DontCome"
        self.can_be_placed_point_off = False
        self.can_be_placed_point_on = True

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status, win_amount = super().update_bet(table)
        if not self.pre_point and self.sub_name == "":
            self.sub_name = "".join(str(e) for e in self.losing_numbers)
        return status, win_amount


# Don't Pass/Don't Come lay odds


class LayOdds(Bet):
    """
    Odds placed on either a DontPass or DontCome bet.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat, bet_object: Bet):
        super().__init__(bet_amount)
        self.name: str = "LayOdds"
        self.sub_name: str = "".join(str(e) for e in bet_object.losing_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.losing_numbers in [[4], [10]]:
            self.payout_ratio = 1 / 2
        elif self.losing_numbers in [[5], [9]]:
            self.payout_ratio = 2 / 3
        elif self.losing_numbers in [[6], [8]]:
            self.payout_ratio = 5 / 6


# Center-table Bets


class Any7(Bet):
    """
    Bet that a 7 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Any7"
        self.winning_numbers: list[int] = [7]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 4


class Two(Bet):
    """
    Bet that a 2 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Two"
        self.winning_numbers: list[int] = [2]
        self.losing_numbers: list[int] = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 30


class Three(Bet):
    """
    Bet that a 3 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Three"
        self.winning_numbers: list[int] = [3]
        self.losing_numbers: list[int] = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 15


class Yo(Bet):
    """
    Bet that an 11 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Yo"
        self.winning_numbers: list[int] = [11]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        self.payout_ratio: int = 15


class Boxcars(Bet):
    """
    Bet that a 12 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Boxcars"
        self.winning_numbers: list[int] = [12]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.payout_ratio: int = 30


class AnyCraps(Bet):
    """
    Bet that any craps number (2, 3, 12) is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "AnyCraps"
        self.winning_numbers: list[int] = [2, 3, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10, 11]
        self.payout_ratio: int = 7


class CAndE(Bet):
    """
    Bet that any craps number (2, 3, 12) or 11 is rolled.

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "CAndE"
        self.winning_numbers: list[int] = [2, 3, 11, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10]

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if table.dice.total in self.winning_numbers:
            status = "win"
            if table.dice.total in [2, 3, 12]:
                payout_ratio = 3
            elif table.dice.total in [11]:
                payout_ratio = 7
            else:
                raise NotImplementedError
            win_amount = payout_ratio * self.bet_amount
        elif table.dice.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


class HardWay(Bet):
    """
    Bet that a number is rolled with the dice faces matching before a
    7 or the non-matching number is rolled.

    Attributes
    ----------
    number : int
        The relevant number that the bet wins and loses on (for hard ways)
    winning_result : list(int)
        The combination of dice the bet wins on
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.number: int | None = None
        self.winning_result: list[int | None] = [None, None]

    def update_bet(self, table: "Table") -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if table.dice.result == self.winning_result:
            status = "win"
            win_amount = float(self.payout_ratio) * self.bet_amount
        elif table.dice.total in [self.number, 7]:
            status = "lose"

        return status, win_amount


class Hard4(HardWay):
    """
    Bet that two twos are rolled prior to a four in another way, or a seven.
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Hard4"
        self.winning_result: list[int | None] = [2, 2]
        self.number: int = 4
        self.payout_ratio: int = 7


class Hard6(HardWay):
    """
    Bet that two threes are rolled prior to a six in another way, or a seven.
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Hard6"
        self.winning_result: list[int | None] = [3, 3]
        self.number: int = 6
        self.payout_ratio: int = 9


class Hard8(HardWay):
    """
    Bet that two fours are rolled prior to a eight in another way, or a seven.
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Hard8"
        self.winning_result: list[int | None] = [4, 4]
        self.number: int = 8
        self.payout_ratio: int = 9


class Hard10(HardWay):
    """
    Bet that two fives are rolled prior to a ten in another way, or a seven.
    """
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.name: str = "Hard10"
        self.winning_result: list[int | None] = [5, 5]
        self.number: int = 10
        self.payout_ratio: int = 7
