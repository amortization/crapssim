import pytest

from crapssim.bet import PassLine, Odds
from crapssim.strategy import BetPassLine, PassLineOddsMultiplier
from crapssim.table import Table, TableUpdate


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, None, 
        [],
        None, 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (3, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (1, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (5, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (6, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (6, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 2, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (4, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (6, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (3, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (1, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (5, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (4, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (5, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (3, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (3, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (3, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (2, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 2, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 9, bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (5, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 12, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (1, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        4, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 5, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (6, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (5, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 8, bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (5, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=5.0)]
    )
])
def test_passline_odds_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    table.add_player(bankroll=float("inf"),
                     strategy=BetPassLine(5) + PassLineOddsMultiplier(1))  # ADD STRATEGY HERE
    table.point.number = point
    table.last_roll = last_roll
    table.players[0].bets_on_table = bets_before
    table.dice.result = dice_result
    TableUpdate().run_strategies(table)
    assert table.players[0].bets_on_table == bets_after