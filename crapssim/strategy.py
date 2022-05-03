"""
This module contains some default basic strategies that can be added to the
Players.
"""

import typing

from crapssim.bet import DontPass, LayOdds, DontCome
from crapssim.bet import Field
from crapssim.bet import PassLine, Odds, Come, Bet
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10

if typing.TYPE_CHECKING:
    from crapssim.player import Player
    from crapssim.table import Table

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""

STRATEGY_TYPE = typing.Union[typing.Callable[['Player', 'Table'], None],
                             typing.Callable[['Player', 'Table', int | str], None],
                             typing.Callable[['Player', 'Table', bool, typing.Iterable[int] | None], None],
                             typing.Callable[['Player', 'Table', str | None], None],
                             typing.Callable[['Player', 'Table', float], None],
                             typing.Callable[['Player', 'Table', int], None]]


def pass_line(player: 'Player', table: 'Table') -> None:
    """ If the point is off place a bet on the Pass Line.

    Parameters
    ----------
    player
        Player object that is using the strategy.
    table
        Table object that the strategy is being used on.

    Returns
    -------
    None
        Dictionary of strategy info.
    """
    # Pass line bet
    if table.point == "Off" and not player.has_bets("PassLine"):
        player.bet(PassLine(player.unit))


def pass_line_odds(player: 'Player', table: 'Table', mult: int | str = 1) -> None:
    """ If the point is off place a bet on the Pass Line. If the point is on, bet the Pass Line Odds.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        mult
            Multiplier integers for the odds or "345" for 345x odds.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)

    # Pass line odds
    if mult == "345":
        if table.point == "On":
            if table.point.number in [4, 10]:
                mult = 3
            elif table.point.number in [5, 9]:
                mult = 4
            elif table.point.number in [6, 8]:
                mult = 5
    elif (isinstance(mult, str) and mult.isdigit()) or isinstance(mult, typing.SupportsInt):
        mult = int(mult)
    else:
        raise NotImplementedError

    if (
            table.point == "On"
            and player.has_bets("PassLine")
            and not player.has_bets("Odds")
    ):
        player.bet(Odds(float(mult) * player.unit, player.get_bet("PassLine")))


def pass_line_odds2(player: 'Player', table: 'Table') -> None:
    """ Pass Line bet when point is off, 2x odds bet when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line_odds(player, table, mult=2)


def pass_line_odds345(player: 'Player', table: 'Table') -> None:
    """ Pass Line bet when point is off, 345x odds bet when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line_odds(player, table, mult='345')


def pass2come(player: 'Player', table: 'Table') -> None:
    """ Pass Line bet followed by 2 come bets when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)

    # Come bet (2)
    if table.point == "On" and player.num_bet("Come") < 2:
        player.bet(Come(player.unit))


def place(player: 'Player', table: 'Table', skip_point: bool = True,
          numbers: typing.Iterable[int] | None = None) -> \
        None:
    """ Place bets, ie 3, 4, 5, 6, 8, 9, 10

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
                skip_point: bool
            If True, don't bet when the point is the given number.
        numbers: set
            Point numbers to place bets on.
        skip_point: bool
            If true skip placing that number if that number is currently the point.

        Returns
        -------
        None
            Dictionary of strategy info.
        """

    if numbers is None:
        numbers = {6, 8}

    numbers = set(numbers).intersection({4, 5, 6, 8, 9, 10})

    if skip_point:
        numbers -= {table.point.number}

    # Place the provided numbers when point is ON
    if table.point == "On":
        if not player.has_bets("Place4") and 4 in numbers:
            player.bet(Place4(player.unit))
        if not player.has_bets("Place5") and 5 in numbers:
            player.bet(Place5(player.unit))
        if not player.has_bets("Place6") and 6 in numbers:
            player.bet(Place6(6 / 5 * player.unit))
        if not player.has_bets("Place8") and 8 in numbers:
            player.bet(Place8(6 / 5 * player.unit))
        if not player.has_bets("Place9") and 9 in numbers:
            player.bet(Place9(player.unit))
        if not player.has_bets("Place10") and 10 in numbers:
            player.bet(Place10(player.unit))

    # Move the bets off the point number if it shows up later
    if skip_point and table.point == "On":
        if player.has_bets("Place4") and table.point.number == 4:
            player.remove(player.get_bet("Place4"))
        if player.has_bets("Place5") and table.point.number == 5:
            player.remove(player.get_bet("Place5"))
        if player.has_bets("Place6") and table.point.number == 6:
            player.remove(player.get_bet("Place6"))
        if player.has_bets("Place8") and table.point.number == 8:
            player.remove(player.get_bet("Place8"))
        if player.has_bets("Place9") and table.point.number == 9:
            player.remove(player.get_bet("Place9"))
        if player.has_bets("Place10") and table.point.number == 10:
            player.remove(player.get_bet("Place10"))


def place68(player: 'Player', table: 'Table') -> None:
    """ Place the 6 and the 8.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)
    # Place 6 and 8 when point is ON
    p_has_place_bets = player.has_bets(
        "Place4", "Place5", "Place6", "Place8", "Place9", "Place10"
    )
    if table.point == "On" and not p_has_place_bets:
        if table.point.number == 6:
            player.bet(Place8(6 / 5 * player.unit))
        elif table.point.number == 8:
            player.bet(Place6(6 / 5 * player.unit))
        else:
            player.bet(Place8(6 / 5 * player.unit))
            player.bet(Place6(6 / 5 * player.unit))


def dont_pass(player: 'Player', table: 'Table') -> None:
    """ Place a bet on the Don't Pass line.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    # Don't pass bet
    if table.point == "Off" and not player.has_bets("DontPass"):
        player.bet(DontPass(player.unit))


def lay_odds(player: 'Player', table: 'Table', win_mult: int | str = 1) -> None:
    """ Place a lay bet.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        win_mult: str | int
            Either '345' or an integer that will be multiplied against the odds to calculate bet.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    # Assume that someone tries to win the `win_mult` times the unit on each bet, which corresponds
    # well to the max_odds on a table.
    # For `win_mult` = "345", this assumes max of 3-4-5x odds
    dont_pass(player, table)
    mult = 1.0
    # Lay odds for don't pass
    if win_mult == "345":
        mult = 6.0
    elif isinstance(win_mult, int):
        if table.point == "On":
            if table.point.number in [4, 10]:
                mult = 2 * win_mult
            elif table.point.number in [5, 9]:
                mult = 3 / 2 * win_mult
            elif table.point.number in [6, 8]:
                mult = 6 / 5 * win_mult

    if (
            table.point == "On"
            and player.has_bets("DontPass")
            and not player.has_bets("LayOdds")
    ):
        player.bet(LayOdds(mult * player.unit, player.get_bet("DontPass")))


"""
Detailed Strategies
"""


def place68_2come(player: 'Player', table: 'Table') -> None:
    """ Once point is established, place 6 and 8, with 2 additional come bets.
        The goal is to be on four distinct numbers, moving place bets if necessary

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    """

    """
    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    if table.point == "On" and len(player.bets_on_table) < 4:
        # always place 6 and 8 when they aren't come bets or place bets already
        if 6 not in current_numbers:
            player.bet(Place6(6 / 5 * player.unit))
        if 8 not in current_numbers:
            player.bet(Place8(6 / 5 * player.unit))

    # add come of pass_line bets to get on 4 numbers
    if player.num_bet("Come", "PassLine") < 2 and len(player.bets_on_table) < 4:
        if table.point == "On":
            player.bet(Come(player.unit))
        if table.point == "Off" and (
                player.has_bets("Place6") or player.has_bets("Place8")
        ):
            player.bet(PassLine(player.unit))

    # if come bet or pass_line goes to 6 or 8, move place bets to 5 or 9
    pass_come_winning_numbers = []
    if player.has_bets("PassLine"):
        pass_come_winning_numbers += player.get_bet("PassLine").winning_numbers
    if player.has_bets("Come"):
        pass_come_winning_numbers += player.get_bet("Come", None).winning_numbers

    if 6 in pass_come_winning_numbers:
        if player.has_bets("Place6"):
            player.remove(player.get_bet("Place6"))
        if 5 not in current_numbers:
            player.bet(Place5(player.unit))
        elif 9 not in current_numbers:
            player.bet(Place9(player.unit))
    elif 8 in pass_come_winning_numbers:
        if player.has_bets("Place8"):
            player.remove(player.get_bet("Place8"))
        if 5 not in current_numbers:
            player.bet(Place5(player.unit))
        elif 9 not in current_numbers:
            player.bet(Place9(player.unit))


def iron_cross(player: 'Player', table: 'Table', mult: int | str = 1) -> None:
    """ Bet the Pass Line, the Pass Line Odds, and Place on 5, 6, and 8. If point is on and no bet on the field, place
        a bet on the field.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        mult
            Either '345' or an integer that will be multiplied against the odds to calculate bet.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)
    pass_line_odds(player, table, mult)
    place(player, table, numbers={5, 6, 8})

    if table.point == "On":
        if not player.has_bets("Field"):
            player.bet(Field(
                player.unit,
                double=table.payouts["fielddouble"],
                triple=table.payouts["fieldtriple"],
            ))


def hammerlock(player: 'Player', table: 'Table', mode: str | None = None) -> None:
    """ Pass Line Bet, Don't Pass bet with a lay of odds. A phased place bet approach, starting inside and then
        shifting outside eventually taking bet down if two place bets win.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        mode: str
            Current phase of the Hammerlock, either "place68", "place_inside" or "takedown"

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)
    lay_odds(player, table, win_mult="345")

    place_nums = set()
    for bet in player.bets_on_table:
        if isinstance(bet, Place):
            place_nums.add(bet.winning_numbers[0])
    place_point_nums = place_nums.copy()
    if table.point.number:
        place_point_nums.add(table.point.number)

    has_place68 = (6 in place_nums) or (8 in place_nums)
    has_place5689 = (
            (5 in place_nums) or (6 in place_nums) or (8 in place_nums) or (9 in place_nums)
    )
    # 3 phases, place68, place_inside, takedown
    if mode is None or table.point == "Off":
        mode = 'place68'
        for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
            player.remove_if_present(bet_nm)

    if mode == "place68":
        if table.point == "On" and has_place68 and place_nums != {6, 8}:
            # assume that a place 6/8 has won
            if player.has_bets("Place6"):
                player.remove(player.get_bet("Place6"))
            if player.has_bets("Place8"):
                player.remove(player.get_bet("Place8"))
            mode = "place_inside"
            place(player, table, numbers={5, 6, 8, 9}, skip_point=False)
        else:
            place(player, table, numbers={6, 8}, skip_point=False)
    elif mode == "place_inside":
        if table.point == "On" and has_place5689 and place_nums != {5, 6, 8, 9}:
            # assume that a place 5/6/8/9 has won
            for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
                player.remove_if_present(bet_nm)
            mode = "takedown"
        else:
            place(player, table, numbers={5, 6, 8, 9}, skip_point=False)
    elif mode == "takedown" and table.point == "Off":
        mode = None

    player.strategy_info['mode'] = mode


def risk12(player: 'Player', table: 'Table', winnings: float = 0) -> None:
    """ Pass line and field bet before the point is established. Once the point is established place the 6 and 8.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        winnings: float
            Amount that has been won thus far.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line(player, table)

    if table.pass_rolls == 0:
        winnings = 0.0

    if table.point == "Off":
        if table.last_roll in table.payouts["fielddouble"]:
            # win double from the field, lose pass line, for a net of 1 unit win
            winnings += player.unit
        elif table.last_roll in table.payouts["fieldtriple"]:
            # win triple from the field, lose pass line, for a net of 2 unit win
            winnings += 2 * player.unit
        elif table.last_roll == 11:
            # win the field and pass line, for a net of 2 units win
            winnings += 2 * player.unit

    if table.point == "Off":
        player.bet(Field(
            player.unit,
            double=table.payouts["fielddouble"],
            triple=table.payouts["fieldtriple"],
        ))
        if table.last_roll == 7:
            for bet_nm in ["Place6", "Place8"]:
                player.remove_if_present(bet_nm)
    elif table.point.number in [4, 9, 10]:
        place(player, table, numbers={6, 8})
    elif table.point.number in [5, 6, 8]:
        # lost field bet, so can't automatically cover the 6/8 bets.  Need to rely on potential early winnings
        if winnings >= 2 * player.unit:
            place(player, table, numbers={6, 8})
        elif winnings >= 1.0 * player.unit:
            if table.point.number != 6:
                place(player, table, numbers={6})
            else:
                place(player, table, numbers={8})

    player.strategy_info['winnings'] = winnings


def knockout(player: 'Player', table: 'Table') -> None:
    """ Pass line bet, don't pass bet, 345x odds behind the pass line bet.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    pass_line_odds345(player, table)
    dont_pass(player, table)


def dice_doctor(player: 'Player', table: 'Table', progression: int = 0) -> None:
    """ Field bet with a progression if you win.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.
        progression
            How far into the progression list the strategy is

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    if table.last_roll in Field(0).losing_numbers:
        progression = 0

    bet_progression = [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150]
    if progression < len(bet_progression):
        amount = bet_progression[progression] * player.unit / 5
    elif progression % 2 == 0:
        # alternate between second to last and last
        amount = bet_progression[len(bet_progression) - 2] * player.unit / 5
    else:
        amount = bet_progression[len(bet_progression) - 1] * player.unit / 5

    player.bet(Field(
        amount,
        double=table.payouts["fielddouble"],
        triple=table.payouts["fieldtriple"],
    ))

    progression += 1

    player.strategy_info['progression'] = progression


# def place68_cpr(player: 'Player', table: 'Table', unit: int = 5, strategy_info: dict[]=None) -> dict[str, str]:
#     """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
#     ## NOTE: NOT WORKING
#     if strategy_info is None:
#         strategy_info = {"mode6": "collect", "mode8": "collect"}
#
#     if table.point == "On":
#         # always place 6 and 8 when they aren't place bets already
#         if not player.has_bets("Place6"):
#             player.bet(Place6(6 / 5 * unit))
#         if not player.has_bets("Place8"):
#             player.bet(Place8(6 / 5 * unit))
#
#     if table.bet_update_info is not None:
#         # place6
#         if player.has_bets("Place6"):
#             bet = player.get_bet("Place6")
#             if (
#                 table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(table.bet_update_info[player][bet.name])
#                 if table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place6 mode: {}".format(strategy_info["mode6"]))
#                     if strategy_info["mode6"] == "press":
#                         player.remove(bet)
#                         player.bet(Place6(2 * bet.bet_amount))
#                         strategy_info["mode6"] = "regress"
#                     elif strategy_info["mode6"] == "regress":
#                         player.remove(bet)
#                         player.bet(Place6(6 / 5 * unit))
#                         strategy_info["mode6"] = "collect"
#                     elif strategy_info["mode6"] == "collect":
#                         strategy_info["mode6"] = "press"
#                     # print("updated place6 mode: {}".format(strategy_info["mode6"]))
#         # place8
#         if player.has_bets("Place8"):
#             bet = player.get_bet("Place8")
#             if (
#                 table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(table.bet_update_info[player][bet.name])
#                 if table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place8 mode: {}".format(strategy_info["mode8"]))
#                     if strategy_info["mode8"] == "press":
#                         player.remove(bet)
#                         player.bet(Place8(2 * bet.bet_amount))
#                         strategy_info["mode8"] = "regress"
#                     elif strategy_info["mode8"] == "regress":
#                         player.remove(bet)
#                         player.bet(Place8(6 / 5 * unit))
#                         strategy_info["mode8"] = "collect"
#                     elif strategy_info["mode8"] == "collect":
#                         strategy_info["mode8"] = "press"
#
#     print(strategy_info)
#     return strategy_info


def place68_dont_come2odds(player: 'Player', table: 'Table') -> None:
    """ Place the 6 and 8, bet don't come with 2x odds.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        table
            Table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    place(player, table, numbers={6, 8}, skip_point=False)

    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    dont_come_losing_numbers = []
    if player.has_bets("DontCome"):
        dont_come_losing_numbers += player.get_bet("DontCome", None).losing_numbers

    if 6 in dont_come_losing_numbers:
        if player.has_bets("Place6"):
            player.remove(player.get_bet("Place6"))
        if 5 not in current_numbers:
            player.bet(Place5(player.unit))
    elif 8 in dont_come_losing_numbers:
        if player.has_bets("Place8"):
            player.remove(player.get_bet("Place8"))
        if 9 not in current_numbers:
            player.bet(Place9(player.unit))

    if table.point == "On" and player.num_bet("DontCome") < 1:
        player.bet(DontCome(player.unit))

    if player.has_bets("DontCome"):
        dc: Bet = player.get_bet("DontCome", None)

        if not isinstance(dc, DontCome):
            raise TypeError
        mult: typing.SupportsFloat = 1
        win_mult: int | float = 2
        # Lay odds for don't come
        if win_mult == "345":
            mult = 6.0
        else:
            win_mult = float(win_mult)
            # print([[b.name, b.sub_name] for b in player.bets_on_table])
            if not dc.pre_point:
                lose_num = dc.losing_numbers[0]
                if lose_num in [4, 10]:
                    mult = 2 * win_mult
                elif lose_num in [5, 9]:
                    mult = 3 / 2 * win_mult
                elif lose_num in [6, 8]:
                    mult = 6 / 5 * win_mult

        if not player.has_bets("LayOdds") and not dc.pre_point:
            player.bet(LayOdds(float(mult) * float(player.unit), dc))


if __name__ == "__main__":
    # Test a betting strategy

    from crapssim.player import Player
    from crapssim.dice import Dice
    from crapssim.table import Table

    # table = CrapsTable()
    # table._add_player(Player(500, place68_2come))

    d = Dice()
    p = Player(500, place68_2come)
    t = Table()
    p.bet(PassLine(5))
    p.bet(Place6(6))
    print(p.bets_on_table)
    print(p.bankroll)
    print(p.total_bet_amount)
