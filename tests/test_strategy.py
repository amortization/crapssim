from collections import namedtuple

import pytest

from crapssim import Player, Table
from crapssim.strategy import pass_line, pass_line_odds, pass_line_odds2, pass_line_odds345, pass2come, place, place68, \
    dont_pass, lay_odds, place68_2come, iron_cross, hammerlock, risk12, knockout, dice_doctor, place68_dont_come2odds


@pytest.mark.parametrize(['strategy', 'strategy_info', 'rolls', 'correct_bets'], [
    (pass_line, {}, [], {('PassLine', (7, 11), 5.0)}),
    (pass_line, {}, [(4, 4)], {('PassLine', (8,), 5.0)}),
    (pass_line_odds, {}, [], {('PassLine', (7, 11), 5.0)}),
    (pass_line_odds, {}, [(4, 4)], {('PassLine', (8,), 5.0), ('Odds', (8,), 5.0)}),
    (pass_line_odds, {}, [(4, 4), (3, 3)], {('PassLine', (8,), 5.0), ('Odds', (8,), 5.0)}),
    (pass_line_odds, {'mult': '345'}, [], {('PassLine', (7, 11), 5.0)}),
    (pass_line_odds, {'mult': '345'}, [(6, 4)], {('PassLine', (10,), 5.0), ('Odds', (10,), 15.0)}),
    (pass_line_odds2, {}, [(2, 2)], {('PassLine', (4,), 5.0), ('Odds', (4,), 10.0)}),
    (pass_line_odds345, {}, [(3, 4), (3, 3)], {('PassLine', (6,), 5.0), ('Odds', (6,), 25.0)}),
    (pass2come, {}, [], {('PassLine', (7, 11), 5.0)}),
    (pass2come, {}, [(4, 5)], {('PassLine', (9,), 5.0), ('Come', (7, 11), 5.0)}),
    (pass2come, {}, [(4, 5), (5, 5)], {('PassLine', (9,), 5.0), ('Come', (7, 11), 5.0), ('Come', (10,), 5.0)}),
    (pass2come, {}, [(4, 5), (5, 5), (3, 3)], {('PassLine', (9,), 5.0), ('Come', (10,), 5.0), ('Come', (6,), 5.0)}),
    (place, {'numbers': {4}, 'skip_point': True}, [], set()),
    (place, {'numbers': {5}, 'skip_point': True}, [(3, 3)], {('Place5', (5,), 5.0)}),
    (place, {'numbers': {5}, 'skip_point': True}, [(3, 2)], set()),
    (place, {'numbers': {5}, 'skip_point': False}, [(3, 2)], {('Place5', (5,), 5.0)}),
    (place68, {}, [(4, 5)], {('PassLine', (9,), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (place68, {}, [(2, 4)], {('PassLine', (6,), 5.0), ('Place8', (8,), 6.0)}),
    (dont_pass, {}, [], {('DontPass', (2, 3), 5.0)}),
    (lay_odds, {'win_mult': 1}, [], {('DontPass', (2, 3), 5.0)}),
    (lay_odds, {'win_mult': '345'}, [(3, 3)], {('LayOdds', (7,), 30.0), ('DontPass', (7,), 5.0)}),
    (place68_2come, {}, [], set()),
    (place68_2come, {}, [(3, 3)], {('Come', (7, 11), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (place68_2come, {}, [(3, 3), (3, 6)],
     {('Come', (7, 11), 5.0), ('Come', (9,), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (place68_2come, {}, [(3, 3), (4, 4)],
     {('Come', (7, 11), 5.0), ('Come', (8,), 5.0), ('Place6', (6,), 6.0), ('Place5', (5,), 5.0)}),
    (iron_cross, {}, [], {('PassLine', (7, 11), 5.0)}),
    (iron_cross, {'mult': '2'}, [(4, 4)],
     {('Odds', (8,), 10.0), ('PassLine', (8,), 5.0), ('Place5', (5,), 5.0), ('Field', (2, 3, 4, 9, 10, 11, 12), 5.0),
      ('Place6', (6,), 6.0)}),
    (hammerlock, {}, [], {('DontPass', (2, 3), 5.0), ('PassLine', (7, 11), 5.0)}),
    (hammerlock, {}, [(3, 3)],
     {('PassLine', (6,), 5.0), ('LayOdds', (7,), 30.0), ('Place8', (8,), 6.0), ('DontPass', (7,), 5.0),
      ('Place6', (6,), 6.0)}),
    (hammerlock, {}, [(3, 3), (4, 4)],
     {('PassLine', (6,), 5.0), ('LayOdds', (7,), 30.0), ('Place8', (8,), 6.0), ('Place5', (5,), 5.0),
      ('Place9', (9,), 5.0), ('DontPass', (7,), 5.0), ('Place6', (6,), 6.0)}),
    (risk12, {}, [], {('Field', (2, 3, 4, 9, 10, 11, 12), 5.0), ('PassLine', (7, 11), 5.0)}),
    (risk12, {}, [(1, 3)], {('PassLine', (4,), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (risk12, {}, [(5, 6), (2, 3)], {('PassLine', (5,), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (knockout, {}, [], {('DontPass', (2, 3), 5.0), ('PassLine', (7, 11), 5.0)}),
    (knockout, {}, [(4, 2)], {('Odds', (6,), 25.0), ('PassLine', (6,), 5.0), ('DontPass', (7,), 5.0)}),
    (dice_doctor, {}, [], {('Field', (2, 3, 4, 9, 10, 11, 12), 10.0)}),
    (dice_doctor, {}, [(1, 1), (5, 6), (5, 5)], {('Field', (2, 3, 4, 9, 10, 11, 12), 30.0)}),
    (place68_dont_come2odds, {}, [], set()),
    (place68_dont_come2odds, {}, [(4, 4)], {('DontCome', (2, 3), 5.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0)}),
    (place68_dont_come2odds, {}, [(4, 4), (2, 2)],
     {('LayOdds', (7,), 20.0), ('Place6', (6,), 6.0), ('Place8', (8,), 6.0), ('DontCome', (7,), 5.0)})])
def test_strategies_compare_bets(strategy, strategy_info, rolls: list[tuple[int, int]],
                                 correct_bets: {(str, str, float)}):
    def strat(player, table, **strat_info):
        if strat_info != {}:
            return strategy(player, table, **strat_info)
        return strategy(player, table, **strategy_info)

    table = Table()
    player = Player(100, bet_strategy=strat)
    table.add_player(player)

    table.fixed_run(rolls)
    table.add_player_bets(verbose=False)

    bets = table.players[0].bets_on_table

    assert {(b.name, tuple(b.winning_numbers), b.bet_amount) for b in bets} == correct_bets
