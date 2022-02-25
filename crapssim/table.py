import typing

from crapssim.bet import Bet, Come, DontCome
from crapssim.dice import Dice
from crapssim.player import Player


class Table(object):
    """
    Craps Table that contains Dice, Players, the Players' bets, and updates
    them accordingly.  Main method is run() which should simulate a craps
    table until a specified number of rolls plays out or all players run out
    of money.

    Parameters
    ----------
    NONE

    Attributes
    ----------
    players : list
        List of player objects at the table
    total_player_cash : float
        Sum of all players bankroll and bets on table
    point : string
        The point for the table.  It is either "Off" when point is off or "On"
        when point is on.
    point_number : int
        The point number when point is "On" and None when point is "Off"
    player_has_bets : bool
        Boolean value for whether any player has a bet on the table.
    strat_info : dictionary
        Contains information stored from the strategy, usually mean for
        strategies that alter based on past information
    bet_update_info : dictionary
        Contains information from updating bets, for given player and a bet
        name, this is status of last bet (win/loss), and win amount.
    """

    def __init__(self) -> None:
        self.players: list[Player] = []
        self.player_has_bets: bool = False
        self.strat_info: dict[Player, typing.Any] = {}
        self.point: _Point = _Point()
        self.dice: Dice = Dice()
        self.bet_update_info: dict | None = None
        self.payouts: dict[str, list[int]] = {"fielddouble": [2, 12], "fieldtriple": []}
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 1

    @classmethod
    def with_payouts(cls, **kwargs: list[int]) -> 'Table':
        table = cls()
        for name, value in kwargs.items():
            table.payouts[name] = value
        return table

    def set_payouts(self, name: str, value: list[int]) -> None:
        self.payouts[name] = value

    def add_player(self, player_object: Player) -> None:
        """ Add player object to the table """
        if player_object not in self.players:
            self.players.append(player_object)
            self.strat_info[player_object] = None

    def run(self, max_rolls: int, max_shooter: float | int = float("inf"),
            verbose: bool = True, runout: bool = False) -> None:
        """
        Runs the craps table until a stopping condition is met.

        Parameters
        ----------
        max_shooter : float | int
            Maximum number of shooters to run for
        max_rolls : int
            Maximum number of rolls to run for
        verbose : bool
            If true, print results from table during each roll
        runout : bool
            If true, continue past max_rolls until player has no more bets on the table
        """
        # self.dice = Dice()
        if verbose:
            print("Welcome to the Craps Table!")

        self.ensure_one_player()

        if verbose:
            print(f"Initial players: {[p.name for p in self.players]}")

        # maybe wrap this into update table or something
        self.total_player_cash = sum(
            [p.total_bet_amount + p.bankroll for p in self.players]
        )

        continue_rolling = True
        while continue_rolling:

            # players make their bets
            self._add_player_bets()
            for p in self.players:
                bets = [
                    f"{b.name}{b.subname}, ${b.bet_amount}" for b in p.bets_on_table
                ]
                if verbose:
                    print(f"{p.name}'s current bets: {bets}")

            self.dice.roll()
            if verbose:
                print("")
                print("Dice out!")
                print(f"Shooter rolled {self.dice.total} {self.dice.result}")
            self._update_player_bets(self.dice, verbose)
            self._update_table(self.dice)
            if verbose:
                print(f"Point is {self.point.status} ({self.point.number})")
                print(f"Total Player Cash is ${self.total_player_cash}")

            # evaluate the stopping condition
            if runout:
                continue_rolling = (
                    self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and all(x.bankroll > x.unit for x in self.players)
                ) or self.player_has_bets
            else:
                continue_rolling = (
                    self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and all(x.bankroll > x.unit for x in self.players)
                )

    def ensure_one_player(self) -> None:
        # make sure at least one player is at table
        if len(self.players) == 0:
            self.add_player(Player(500.0, name="Player1"))

    def _add_player_bets(self) -> None:
        """ Implement each player's betting strategy """
        for p in self.players:
            p._add_strategy_bets(self, **self.strat_info[p] or dict())
            # TODO: add player.strat_kwargs as optional parameter (currently manually changed in CrapsTable)

    def _update_player_bets(self, dice: Dice, verbose: bool = False) -> None:
        """ check bets for wins/losses, payout wins to their bankroll, remove bets that have resolved """
        self.bet_update_info = {}
        for p in self.players:
            info = p._update_bet(self, dice, verbose)
            self.bet_update_info[p] = info

    def _update_table(self, dice: Dice) -> None:
        """ update table attributes based on previous dice roll """
        self.pass_rolls += 1
        if self.point == "On" and dice.total == 7:
            self.n_shooters += 1
        if self.point == "On" and (dice.total == 7 or dice.total == self.point.number):
            self.pass_rolls = 0

        self.point.update(self.dice)
        self.total_player_cash = sum(
            [p.total_bet_amount + p.bankroll for p in self.players]
        )
        self.player_has_bets = sum([len(p.bets_on_table) for p in self.players]) >= 1
        self.last_roll = dice.total

    def _get_player(self, player_name: str) -> typing.Union['Player', bool]:
        for p in self.players:
            if p.name == player_name:
                return p
        return False


class _Point:
    """
    The point on a craps table.

    Parameters
    ----------
    NONE

    Attributes
    ----------
    status : str
        Either 'On' or 'Off', depending on whether a point is set
    number : int
        The point number (in [4, 5, 6, 8, 9, 10]) is status == 'On'
    """

    def __init__(self) -> None:
        self.status: str = "Off"
        self.number: int | None = None

    def __eq__(self, other: object) -> bool:
        return self.status == other

    def update(self, dice_object: Dice) -> None:
        if self.status == "Off" and dice_object.total in [4, 5, 6, 8, 9, 10]:
            self.status = "On"
            self.number = dice_object.total
        elif self.status == "On" and dice_object.total in [7, self.number]:
            self.status = "Off"
            self.number = None


if __name__ == "__main__":
    import sys

    # import strategy
    from crapssim.strategy import dicedoctor

    sim = False
    printout = True

    n_sim = 100
    n_roll = 144
    n_shooter = 2
    bankroll = 1000
    strategy = dicedoctor
    strategy_name = "dicedoctor"  # don't include any "_" in this
    runout = True
    runout_str = "-runout" if runout else ""

    if sim:
        # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
        outfile_name = f"./output/simulations/{strategy_name}_sim-{n_sim}_roll-{n_roll}_br-{bankroll}{runout_str}.txt"
        with open(outfile_name, "w") as f_out:
            f_out.write("total_cash,n_rolls")
            f_out.write(str("\n"))
            for i in range(n_sim):
                table = Table()
                table.add_player(Player(bankroll, strategy))
                table.run(n_roll, n_shooter, verbose=False, runout=runout)
                out = f"{table.total_player_cash},{table.dice.n_rolls}"
                f_out.write(str(out))
                f_out.write(str("\n"))

    if printout:
        # Run one simulation with verbose=True to check strategy
        outfile_name = f"./output/printout/{strategy_name}_roll-{n_roll}_br-{bankroll}{runout_str}.txt"
        with open(outfile_name, "w") as f_out:
            sys.stdout = f_out
            table = Table()
            table.add_player(Player(bankroll, strategy))
            table.run(n_roll, verbose=True)
            # out = table.total_player_cash
            # f_out.write(str(out))
            # f_out.write(str('\n'))

    sys.stdout = sys.__stdout__  # reset stdout

    # table = Table().with_payouts(fielddouble=[2], fieldtriple=[12])
    # print(table)
    # print(table.payouts)
