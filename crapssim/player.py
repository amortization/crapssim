"""
This module contains the Player class which sit at the Table and
place Bets on the table. Each player has a strategy assigned which
controls the actions of the player.
"""

import typing

from crapssim.bet import Bet
from crapssim.strategy import STRATEGY_TYPE, pass_line

if typing.TYPE_CHECKING:
    from crapssim.table import Table


class NoTableError(Exception):
    """
    Exception raised when there is no table assigned to the player.
    """

    def __init__(self):
        super().__init__('Player has no Table assigned.')


class Player:
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : typing.SupportsFloat
        Starting amount of cash for the player
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, default = "Player"
        Name of the player
    unit : typing.SupportsFloat, default=5
        Standard amount of bet to be used by bet_strategy

    Attributes
    ----------
    bankroll : typing.SupportsFloat
        Current amount of cash for the player
    name : str
        Name of the player
    bet_strategy :
        A function that implements a particular betting strategy. See betting_strategies.py.
    strategy_info : dict[str, typing.Any]
        Variables to be used by the players bet_strategy
    unit : typing.SupportsFloat
        Standard amount of bet to be used by bet_strategy
    bets_on_table : list
        Betting objects for the player that are currently on the table.
    """

    def __init__(self, bankroll: typing.SupportsFloat,
                 bet_strategy: STRATEGY_TYPE = pass_line,
                 name: str = "Player",
                 unit: typing.SupportsFloat = 5,
                 table: typing.Optional['Table'] = None):
        self.bankroll: float = float(bankroll)
        self.bet_strategy: STRATEGY_TYPE = bet_strategy
        self.strategy_info: dict[str, typing.Any] = {}
        self.name: str = name
        self.unit: float = float(unit)
        self.table: typing.Optional["Table"] = None
        if table is not None:
            self.sit_at_table(table)

        self.bets_on_table: list[Bet] = []

    @property
    def total_bet_amount(self) -> float:
        """
        Total amount of bets player currently has on the table.

        Returns
        -------
        float
            Total amount of bets player currently has on the table.
        """
        return sum(bet.bet_amount for bet in self.bets_on_table)

    def sit_at_table(self, table: "Table") -> None:
        """
        Adds player to the given table.

        Parameters
        ----------
        table : Table
            The Table for the player to sit at.
        """
        table.add_player(self)

    def bet(self, bet: Bet) -> None:
        """
        Places the bet given on the table if able to do so.

        Parameters
        ----------
        bet : Bet
            The bet to place.
        """
        if self.can_bet(bet) is False:
            return

        self.bankroll -= bet.bet_amount

        if self.has_bet(name=bet.name,
                        winning_numbers=bet.winning_numbers):
            existing_bet: Bet = self.get_bet(name=bet.name,
                                             winning_numbers=bet.winning_numbers)
            existing_bet.bet_amount += bet.bet_amount
        else:
            self.bets_on_table.append(bet)

    def can_bet(self, bet: Bet) -> bool:
        """
        Is True if the given bet object can be placed, otherwise False.

        Parameters
        ----------
        bet : Bet
            The bet to check whether it can be placed or not.

        Returns
        -------
        bool
            True if bet can be placed, otherwise False.
        """
        if self.table is None:
            raise NoTableError

        can_bet = True
        if not bet.bet_allowed[self.table.point.status]:
            can_bet = False
        if self.bankroll < bet.bet_amount:
            can_bet = False
        return can_bet

    def remove_bet(self, bet: Bet) -> None:
        """
        Remove the given bet and increase bankroll by bet amount.

        Parameters
        ----------
        bet : Bet
            The bet to remove.
        """
        if bet in self.bets_on_table and bet.removable:
            self.bankroll += bet.bet_amount
            self.bets_on_table.remove(bet)

    def has_bet(self, name: str | None = None, names: list[str] | None = None,
                winning_numbers: list[int] | None = None,
                losing_numbers: list[int] | None = None) -> bool:
        """
        Returns True if there is a bet whose name is in bets_to_check
        """
        return len(
            self.get_bets(name=name, names=names,
                          winning_numbers=winning_numbers,
                          losing_numbers=losing_numbers)
        ) > 0

    def get_bets(self, name: str | None = None,
                 names: list[str] | None = None,
                 winning_numbers: list[int] | None = None,
                 losing_numbers: list[int] | None = None) -> list[Bet]:
        """
        Return a list of bets on table for player given the
        parameters of the bet. If a parameter is None, that parameter
        will not be searched.

        Parameters
        ----------
        name : str | None
            Returns bets where the name matches the given name.
        names : list[str] | None
            Returns bets where the name is in the given list of names.
        winning_numbers : list[int] | None
            Returns bets where the winning numbers match the given winning number.
        losing_numbers : list[int] | None
            Returns bets where the losing numbers match the given losing number.

        Returns
        -------
        list[Bet]
            A list of bets that match the given criteria.
        """
        bets: list[Bet] = self.bets_on_table
        if name is not None:
            bets = filter(lambda x: x.name == name, bets)
        if names is not None:
            bets = filter(lambda x: x.name in names, bets)
        if winning_numbers is not None:
            bets = filter(lambda x: x.winning_numbers == winning_numbers, bets)
        if losing_numbers is not None:
            bets = filter(lambda x: x.losing_numbers == losing_numbers, bets)
        return list(bets)

    def get_bet(self, name: str | None = None,
                names: list[str] | None = None,
                winning_numbers: list[int] | None = None,
                losing_numbers: list[int] | None = None) -> Bet:
        """Returns the first bet where all the criteria match"""
        return self.get_bets(name=name,
                             names=names,
                             winning_numbers=winning_numbers,
                             losing_numbers=losing_numbers)[0]

    def number_of_bets(self, name: str | None = None,
                       names: list[str] | None = None,
                       winning_numbers: list[int] | None = None,
                       losing_numbers: list[int] | None = None) -> int:
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        return len(
            self.get_bets(name=name,
                          names=names,
                          winning_numbers=winning_numbers,
                          losing_numbers=losing_numbers)
        )

    def remove_if_present(self, bet_name: str, bet_winning_numbers: list[int] = None) -> None:
        """
        If a bet with the given name and numbers exists, remove it.

        Parameters
        ----------
        bet_name : str
            Bet name to check against.
        bet_winning_numbers : list[int]
            Winning numbers to check against.
        """
        if self.has_bet(name=bet_name, winning_numbers=bet_winning_numbers):
            self.remove_bet(self.get_bet(name=bet_name, winning_numbers=bet_winning_numbers))

    def add_strategy_bets(self) -> None:
        """ Implement the given betting strategy """
        if self.table is None:
            raise NoTableError

        if self.bet_strategy:
            self.bet_strategy(self, self.table, **self.strategy_info)

    def update_bet(self, verbose: bool = False) -> \
            dict[str, dict[str, float | str | None]]:
        """
        Update all of this player's bets on table with the tables dice roll.

        Parameters
        ----------
        verbose : bool
            If True print out description of the bets being won, lost, etc.
        """
        if self.table is None:
            raise NoTableError

        info = {}

        new_bets_on_table = []
        for bet in self.bets_on_table:
            status, win_amount = bet.update_bet(self.table)

            if status == "win":
                self.bankroll += win_amount + bet.bet_amount
                if verbose:
                    print(f"{self.name} won ${win_amount} on {bet.name} bet!")
            elif status == "lose":
                if verbose:
                    print(f"{self.name} lost ${bet.bet_amount} on {bet.name} bet.")
            elif status == "push":
                self.bankroll += bet.bet_amount
                if verbose:
                    print(f"{self.name} pushed ${bet.bet_amount} on {bet.name} bet.")
            else:
                new_bets_on_table.append(bet)

            info[bet.name] = {"status": status, "win_amount": win_amount}

        self.bets_on_table = new_bets_on_table

        return info
