import poloniexAPI
import time
import sys


def exit_margin(price, symbol, ticket, confirm):
    if ticket < confirm:
        print("Exit ticket: %s" % (str(ticket)))
        ticket = ticket + 1
    else:
        print("Exit ticket close: %s" % (str(ticket)))
        res = poloniexAPI.polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
        print("Res %s at price %f" % (res, price))
        ticket = 0

    return ticket


class Portfolio:
    is_buy_open = False
    is_sell_open = False
    SYMBOL = None
    ticket = -1
    confirm = 4
    initiate = 0

    def __init__(self, symbol, confirm_period):
        self.SYMBOL = symbol
        self.ticket = 0
        self.confirm = confirm_period
        self.initiate = 0
        self.trim = 0
        self.dont_trade = "none"

    def crossover_strategy(self, time_period, fast_period, mid_period, slow_period, confirm_period, trim_count):
        try:
            print("Symbol: %s  " % (self.SYMBOL ))
            time.sleep(0.2)
