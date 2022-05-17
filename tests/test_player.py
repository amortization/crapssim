from crapssim import Table, Dice
from crapssim.bet import PassLine
from crapssim.player import Player
from crapssim.strategy import passline


def test_default_strategy():
    player = Player(None, 100)
    assert player.bet_strategy == passline


def test_irremovable_bet():
    bet = PassLine(50)
    table = Table()
    table.fixed_roll([2, 2])
    bet.update(table)
    assert bet.removable is False


def test_existing_bet():
    table = Table()
    table.add_player()
    bet_one = PassLine(50)
    table.players[0].add_bet(bet_one, table)
    bet_two = PassLine(50)
    table.players[0].add_bet(bet_two, table)

    bet_count = len(table.players[0].bets_on_table)
    bet_amount = table.players[0].bets_on_table[0].bet_amount
    bankroll = table.players[0].bankroll
    total_bet_amount = table.players[0].total_bet_amount

    assert (bet_count, bet_amount, bankroll, total_bet_amount) == (1, 100, 0, 100)
