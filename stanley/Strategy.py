import poloniexAPI
PERIOD_MA_SLOW = 120
PERIOD_MA_FAST = 20

# region ### Methods
def calc_amount_alt(price, coin):
    current_balance = poloniexAPI.get_balance(coin)  # make it more flexible...
    print("My trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 2  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance
    return amount

# region ### Methods
def calc_amount_btc(price):
    current_balance = poloniexAPI.get_balance('BTC')  # make it more flexible...
    print("My trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 2  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance / price
    return amount

def buy(ask, symbol):
    amount = calc_amount_btc(ask)
    #SYMBOL = 'BTC_ETH'
    print("Buy %s amount = %s at price %f" % (symbol, amount, ask))

    # uncomment to make trades
    res = poloniexAPI.polo.buy(symbol, ask, amount, orderType='immediateOrCancel')
    # res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=2.4)  # if you want margin trade
    print("Res %s at price %f" % (res, ask))

    #res = 'success'
    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return res


def sell(bid, symbol):
    coin =  symbol.replace("BTC_", "")
    amount = calc_amount_alt(bid, coin)
    #SYMBOL = 'BTC_ETH'
    print("Sell %s amount = %s at price %f" % (symbol, amount, bid))

    # uncomment to make trades
    res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')
    #res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=2.4)  # if you want margin trade
    print("Res %s at price %f" % (res, bid))

    #res = 'success'  # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return res

def buy_margin(ask, symbol):
    amount = calc_amount_btc(ask)
    #SYMBOL = 'BTC_ETH'
    print("Buy %s amount = %s at price %f" % (symbol, amount, ask))

    # uncomment to make trades
    res = poloniexAPI.polo.buy(symbol, ask, amount, orderType='immediateOrCancel')
    # res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=2.4)  # if you want margin trade
    print("Res %s at price %f" % (res, ask))

    #res = 'success'
    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return res


def sell_margin(bid, symbol):
    coin =  symbol.replace("BTC_", "")
    amount = calc_amount_alt(bid, coin)
    #SYMBOL = 'BTC_ETH'
    print("Sell %s amount = %s at price %f" % (symbol, amount, bid))

    # uncomment to make trades
    res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')
    #res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=2.4)  # if you want margin trade
    print("Res %s at price %f" % (res, bid))

    #res = 'success'  # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return res
# endregion


class Strategy:
    is_buy_open = False
    is_sell_open = False
    SYMBOL = None
    ticket = -1
    confirm = 3

    def __init__(self, symbol):
        self.SYMBOL = symbol
        self.ticket = 0
        self.confirm = 3
    def crossover_strategy(self, fast_period, slow_period):

        fast_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=5, period=fast_period)
        slow_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=5, period=slow_period)

        last_price = poloniexAPI.get_orderbook(self.SYMBOL)
        ask = float(last_price['asks'][0][0])*1.01
        bid = float(last_price['bids'][0][0])*0.99

        if self.is_buy_open and slow_ma > fast_ma:
            if self.ticket < self.confirm:
                self.ticket = self.ticket + 1
            else:
                sell(bid, self.SYMBOL)
                self.ticket = 0
                self.is_sell_open = True
                self.is_buy_open = False

        elif self.is_sell_open and slow_ma < fast_ma:
            if self.ticket < self.confirm:
                self.ticket = self.ticket + 1
            else:
                buy(ask, self.SYMBOL)
                self.ticket = 0
                self.is_sell_open = False
                self.is_buy_open = True

        if self.is_buy_open is False and self.is_sell_open is False and slow_ma < fast_ma:
            # first buy
            buy(ask, self.SYMBOL)
            self.is_buy_open = True

        elif self.is_sell_open is False and self.is_buy_open is False and slow_ma > fast_ma:
            # first sell
            sell(bid, self.SYMBOL)
            self.is_sell_open = True


#    def supertrend_strategy(self, fast_period, slow_period):
