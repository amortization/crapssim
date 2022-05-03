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
    total_bet_amount : int
        Sum of bet value for the player
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
        return sum(bet.bet_amount for bet in self.bets_on_table)

    def sit_at_table(self, table: "Table"):
        table.add_player(self)

    def bet(self, bet_object: Bet) -> None:
        if self.can_bet(bet_object) is False:
            return

        self.bankroll -= bet_object.bet_amount

        if (bet_object.name, bet_object.winning_numbers) in \
                [(b.name, b.winning_numbers) for b in self.bets_on_table]:
            existing_bet: Bet = self.get_bet(bet_object.name, bet_object.winning_numbers)
            existing_bet.bet_amount += bet_object.bet_amount
        else:
            self.bets_on_table.append(bet_object)

    def can_bet(self, bet_object: Bet):
        if self.table is None:
            raise NoTableError

        can_bet = True
        if not bet_object.bet_allowed[self.table.point.status]:
            can_bet = False
        if self.bankroll < bet_object.bet_amount:
            can_bet = False
        return can_bet

    def remove(self, bet_object: Bet) -> None:
        if bet_object in self.bets_on_table and bet_object.removable:
            self.bankroll += bet_object.bet_amount
            self.bets_on_table.remove(bet_object)

    def has_bet(self, *bets_to_check: str) -> bool:
        """
        returns True if bets_to_check and self.bets_on_table has at least one thing in common
        """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def get_bets(self, name: str | None = None,
                 winning_number: int | None = None,
                 winning_numbers: list[int] | None = None,
                 losing_number: int | None = None,
                 losing_numbers: list[int] | None = None,
                 payout_ratio: float | None = None,
                 removable: bool | None = None) -> list[Bet]:
        """
        Return a list of bets on table for player given the
        parameters of the bet. If a parameter is None, that parameter
        will not be searched.

        Parameters
        ----------
        name : str | None
            Returns bets where the name matches the given name.
        winning_number : int | None
            Returns bets where the winning number is included in the bets winning numbers.
        winning_numbers : list[int] | None
            Returns bets where the winning numbers match the given winning number.
        losing_number : int | None
            Returns bets where the losing number is included in the bets losing numbers.
        losing_numbers : list[int] | None
            Returns bets where the losing numbers match the given losing number.
        payout_ratio : float | None
            Returns bets where the payout ratio matches the given ratio.
        removable : bool | None
            Returns bets where the removable flag matches the given flag.

        Returns
        -------
        list[Bet]
            A list of bets that match the given criteria.
        """
        bets: list[Bet] = self.bets_on_table
        if name is not None:
            bets = filter(lambda x: x.name == name, bets)
        if winning_number is not None:
            bets = filter(lambda x: winning_number in x.winning_numbers, bets)
        if winning_numbers is not None:
            bets = filter(lambda x: x.winning_numbers == winning_numbers, bets)
        if losing_number is not None:
            bets = filter(lambda x: losing_number in x.losing_numbers, bets)
        if losing_numbers is not None:
            bets = filter(lambda x: x.losing_numbers == losing_numbers, bets)
        if payout_ratio is not None:
            bets = filter(lambda x: x.payout_ratio is payout_ratio, bets)
        if removable is not None:
            bets = filter(lambda x: x.removable is removable, bets)
        return list(bets)

    def get_bet(self, bet_name: str, bet_winning_numbers: str = None) -> Bet:
        """returns first betting object matching bet_name and bet_winning_numbers.
        If bet_winning_numbers="Any", returns first betting object matching bet_name"""
        return self.get_bets(name=bet_name, winning_numbers=bet_winning_numbers)[0]

    def num_bet(self, *bets_to_check: str) -> int:
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        bet_names = [b.name for b in self.bets_on_table]
        return sum([i in bets_to_check for i in bet_names])

    def remove_if_present(self, bet_name: str, bet_winning_numbers: str = None) -> None:
        if self.has_bet(bet_name):
            self.remove(self.get_bet(bet_name, bet_winning_numbers))

    def add_strategy_bets(self) -> None:
        """ Implement the given betting strategy """
        if self.table is None:
            raise NoTableError

        if self.bet_strategy:
            self.bet_strategy(self, self.table, **self.strategy_info)

    def update_bet(self, verbose: bool = False) -> \
            dict[str, dict[str, float | str | None]]:
        if self.table is None:
            raise NoTableError

        info = {}
        for b in self.bets_on_table[:]:
            status, win_amount = b.update_bet(self.table)

            if status == "win":
                self.bankroll += win_amount + b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} won ${win_amount} on {b.name} bet!")
            elif status == "lose":
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} lost ${b.bet_amount} on {b.name} bet.")
            elif status == "push":
                self.bankroll += b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} pushed ${b.bet_amount} on {b.name} bet.")

            info[b.name] = {"status": status, "win_amount": win_amount}
        return info
