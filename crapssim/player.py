import typing

from crapssim.bet import Bet
from crapssim.strategy import STRATEGY_TYPE, passline

if typing.TYPE_CHECKING:
    from crapssim.table import Table


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
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player
    """

    def __init__(self, bankroll: typing.SupportsFloat,
                 bet_strategy: STRATEGY_TYPE = passline,
                 name: str = "Player",
                 unit: typing.SupportsFloat = 5,
                 table: 'Table' = None):
        self.bankroll: float = bankroll
        self.bet_strategy: STRATEGY_TYPE = bet_strategy
        self.strategy_info: dict[str, typing.Any] = {}
        self.name: str = name
        self.unit: typing.SupportsFloat = unit
        self.table = None
        if table is not None:
            self.sit_at_table(table)

        self.bets_on_table: list[Bet] = []
        self.total_bet_amount: float = 0.0

    def sit_at_table(self, table: "Table"):
        table.add_player(self)

    def bet(self, bet_object: Bet) -> None:
        if self.table.point.status == 'Off' and not bet_object.can_be_placed_point_off:
            return
        if self.table.point.status == 'On' and not bet_object.can_be_placed_point_on:
            return

        if self.bankroll >= bet_object.bet_amount:
            self.bankroll -= bet_object.bet_amount

            if (bet_object.name, bet_object.sub_name) in [(b.name, b.sub_name) for b in self.bets_on_table]:
                existing_bet: Bet = self.get_bet(bet_object.name, bet_object.sub_name)
                existing_bet.bet_amount += bet_object.bet_amount
            else:
                self.bets_on_table.append(bet_object)

            self.total_bet_amount += bet_object.bet_amount

    def remove(self, bet_object: Bet) -> None:
        if bet_object in self.bets_on_table and bet_object.removable:
            self.bankroll += bet_object.bet_amount
            self.bets_on_table.remove(bet_object)
            self.total_bet_amount -= bet_object.bet_amount

    def has_bet(self, *bets_to_check: str) -> bool:
        """ returns True if bets_to_check and self.bets_on_table has at least one thing in common """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def get_bet(self, bet_name: str, bet_sub_name: str = "") -> Bet:
        """returns first betting object matching bet_name and bet_sub_name.
        If bet_sub_name="Any", returns first betting object matching bet_name"""
        if bet_sub_name == "Any":
            bet_name_list: list[str] = [b.name for b in self.bets_on_table]
            ind: int = bet_name_list.index(bet_name)
        else:
            bet_name_sub_name_list: list[list[str]] = [[b.name, b.sub_name] for b in self.bets_on_table]
            ind = bet_name_sub_name_list.index([bet_name, bet_sub_name])
        return self.bets_on_table[ind]

    def num_bet(self, *bets_to_check: str) -> int:
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        bet_names = [b.name for b in self.bets_on_table]
        return sum([i in bets_to_check for i in bet_names])

    def remove_if_present(self, bet_name: str, bet_sub_name: str = "") -> None:
        if self.has_bet(bet_name):
            self.remove(self.get_bet(bet_name, bet_sub_name))

    def add_strategy_bets(self) -> None:
        """ Implement the given betting strategy """
        if self.bet_strategy:
            self.bet_strategy(self, self.table, **self.strategy_info)

    def update_bet(self, verbose: bool = False) -> \
            dict[str, dict[str, str | None | float]]:
        info = {}
        for b in self.bets_on_table[:]:
            status, win_amount = b._update_bet(self.table, self.table.dice)

            if status == "win":
                self.bankroll += win_amount + b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} won ${win_amount} on {b.name} bet!")
            elif status == "lose":
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} lost ${b.bet_amount} on {b.name} bet.")
            elif status == "push":
                self.bankroll += b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} pushed ${b.bet_amount} on {b.name} bet.")

            info[b.name] = {"status": status, "win_amount": win_amount}
        return info
