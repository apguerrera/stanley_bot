import poloniexAPI
import time

PERIOD_MA_SLOW = 120
PERIOD_MA_FAST = 20

# region ### Methods
def calc_amount_alt(price, coin):
    current_balance = poloniexAPI.get_balance(coin)  # make it more flexible...
    print("My alt trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 8  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance
    return amount

# region ### Methods
def calc_amount_btc(price):
    current_balance = poloniexAPI.get_balance('BTC_XRP')  # make it more flexible...
    print("My btc trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 8  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance / price
    return amount


# region ### Methods
def calc_margin_alt(price, symbol):
    current_balance = poloniexAPI.polo.returnTradableBalances()  # make it more flexible...
    #print("My trade balance = %s at price %f" % (current_balance, price))

    coin =  symbol.replace("BTC_", "")
    coin_balance = float(current_balance[symbol][coin])
    print("My malt trade balance = %s at price %f" % (coin_balance, price))

    relative_balance = coin_balance*0.5  # 2= 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance
    return amount


# region ### Methods
def calc_margin_btc(price, symbol):
    current_balance = poloniexAPI.get_btc_balance(symbol)  # make it more flexible...

    print("My mbtc margin balance = %f at price %f" % (current_balance, price))

    relative_balance = current_balance*0.5 # 2= 50% of current balance
    #relative_balance = 0.021  # 2= 50% of current balance

    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance / price
    return amount



def buy_margin(ask, symbol):
    amount = calc_margin_btc(ask, symbol)
    #SYMBOL = 'BTC_ETH'
    print("Buy %s amount = %s at price %f" % (symbol, amount, ask))

    # uncomment to make trades
    #res = poloniexAPI.polo.buy(symbol, ask, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
    print("Res %s at price %f" % (res, ask))

    #res = 'success'
    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return res

def exit_buy_margin(ask, symbol):
    amount = calc_margin_btc(ask, symbol) * 0.4
    #SYMBOL = 'BTC_ETH'
    print("Exit %s amount = %s at price %f" % (symbol, amount, ask))

    # uncomment to make trades
    #res = poloniexAPI.polo.buy(symbol, ask, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
    print("Res %s at price %f" % (res, ask))

    #res = 'success'
    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return res

def sell_margin(bid, symbol):
    #coin =  symbol.replace("BTC_", "")
    amount = calc_margin_alt(bid, symbol)
    #SYMBOL = 'BTC_ETH'
    print("Sell %s amount = %s at price %f" % (symbol, amount, bid))

    # uncomment to make trades
    #res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=0.02)  # if you want margin trade
    print("Res %s at price %f" % (res, bid))

    #res = 'success'  # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return res

def exit_sell_margin(bid, symbol):
    #coin =  symbol.replace("BTC_", "")
    amount = calc_margin_alt(bid, symbol) * 0.4
    #SYMBOL = 'BTC_ETH'
    print("Sell %s amount = %s at price %f" % (symbol, amount, bid))

    # uncomment to make trades
    #res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=0.02)  # if you want margin trade
    print("Res %s at price %f" % (res, bid))

    #res = 'success'  # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return res

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
# endregion


class Strategy:
    is_buy_open = False
    is_sell_open = False
    SYMBOL = None
    ticket = -1
    confirm = 3
    initiate = 0

    def __init__(self, symbol):
        self.SYMBOL = symbol
        self.ticket = 0
        self.confirm = 3
        self.initiate = 0
    def crossover_strategy(self, time_period, fast_period, mid_period, slow_period):

        fast_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=fast_period)
        time.sleep(0.2)  # safe
        slow_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=slow_period)
        time.sleep(0.2)  # safe
        mid_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=mid_period)
        time.sleep(0.2)  # safe

        current_btc = poloniexAPI.get_btc_balance(self.SYMBOL)
        time.sleep(0.2)  # safe

        current_alt = poloniexAPI.get_margin_balance(self.SYMBOL)
        time.sleep(0.2)  # safe

        last_price = poloniexAPI.get_orderbook(self.SYMBOL)
        alt_converted = float(current_alt)  * float(last_price['bids'][0][0])

        ask = float(last_price['asks'][0][0])*1.02
        bid = float(last_price['bids'][0][0])*0.98
        current_margin = poloniexAPI.get_current_margin()
        print("%s Alt %f at price %f" % (self.SYMBOL, alt_converted, current_btc))
        print("%s confirm %f at ticket %f" % (self.SYMBOL, self.confirm, self.ticket))
        print("%s sell open %f buy open %f" % (self.SYMBOL, self.is_sell_open, self.is_buy_open))

        # initate trade
        if self.initiate == 0 :
            if self.is_buy_open is False and self.is_sell_open is False:
                if slow_ma > fast_ma:
                    if alt_converted > 0.08 :
                        # first sell
                        sell_margin(bid, self.SYMBOL)
                        self.is_sell_open = True
                        initiate = 1
                    elif alt_converted < 0.08 :
                        # first sell
                        #sell_margin(bid, self.SYMBOL)
                        self.is_sell_open = True
                        initiate = 1
                elif slow_ma < fast_ma:
                    if current_btc > 0.08:
                        # first buy
                        buy_margin(ask, self.SYMBOL)
                        self.is_buy_open = True
                        initiate = 1
                    elif current_btc < 0.08:
                        # first sell
                        #sell_margin(bid, self.SYMBOL)
                        self.is_buy_open = True
                        initiate = 1

        # trade strategy
        if self.is_buy_open:
            if fast_ma > slow_ma:
                if current_btc > 0.09 and current_margin > 0.45:
                    buy_margin(ask, self.SYMBOL)
                    self.is_buy_open = True
            if fast_ma < mid_ma and current_btc > 0.07  and current_margin > 0.45:
                exit_sell_margin(bid, self.SYMBOL)
                self.is_buy_open = False
                self.ticket = 0
            if current_margin < 0.25 :
                exit_sell_margin(bid, self.SYMBOL)
                self.is_buy_open = False
                self.ticket = 0
                    #self.is_sell_open = True
                    #self.is_buy_open = False
        elif self.is_sell_open:
            if fast_ma < slow_ma:
                if alt_converted > 0.09 and current_margin > 0.45:
                    sell_margin(bid, self.SYMBOL)
                    self.is_sell_open = True
            if fast_ma > mid_ma and alt_converted > 0.07 and current_margin > 0.45:
                exit_buy_margin(ask, self.SYMBOL)
                self.is_sell_open = False
                self.ticket = 0
            if current_margin < 0.25 :
                exit_buy_margin(ask, self.SYMBOL)
                self.is_sell_open = False
                self.ticket = 0

        elif self.is_sell_open is False and self.is_buy_open is False :
            if  fast_ma > slow_ma and fast_ma > mid_ma:
                if self.ticket < self.confirm:
                    self.ticket = self.ticket + 1
                else:
                    buy_margin(ask, self.SYMBOL)
                    self.ticket = 0
                    self.is_sell_open = False
                    self.is_buy_open = True
            if  fast_ma < slow_ma and fast_ma < mid_ma:
                if self.ticket < self.confirm:
                    self.ticket = self.ticket + 1
                else:
                    sell_margin(bid, self.SYMBOL)
                    self.ticket = 0
                    self.is_sell_open = True
                    self.is_buy_open = False

        #    def supertrend_strategy(self, fast_period, slow_period):
