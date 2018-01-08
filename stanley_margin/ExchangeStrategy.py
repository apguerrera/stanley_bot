import poloniexAPI
import time
import sys


# region ### Methods
def calc_margin_alt(price, symbol):
    current_balance = poloniexAPI.polo.returnTradableBalances()  # make it more flexible...
    coin =  symbol.replace("BTC_", "")
    coin_balance = float(current_balance[symbol][coin])
    relative_balance = coin_balance*0.95  # 95% of current balance for buffer
    print("My malt margin balancse = %s at price %f" % (relative_balance, price))

    amount = relative_balance
    return amount


# region ### Methods
def calc_margin_btc(price, symbol):
    balance = poloniexAPI.polo.returnTradableBalances()
    coin_balance = float(balance[symbol]["BTC"])
    relative_balance = coin_balance*0.90  # 2= 50% of current balance
    print("My mbtc margin balance = %f at price %f" % (relative_balance, price))

    amount = relative_balance / price
    return amount

def buy_margin_amount(ask, symbol, amount):
    value = float(amount) * ask
    print("Buy %s Amount = %s at price %f, value %f" % (symbol, amount, ask, value))
    if value > 0.02:  # enough margin to place a trade
        amount = amount * factor
        res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
        print("Res %s at price %f" % (res, ask))
        ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin: %f" % (symbol, value))
        ret = 'no_margin'
    return ret

def sell_margin_amount(bid, symbol, amount):
    value = float(amount) * bid
    print("Sell %s Amount = %s at price %f, value %f" % (symbol, amount, bid, value))
    if value > 0.02:  # enough margin to place a trade
        res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=0.02)  # if you want margin trade
        print("Res %s at price %f" % (res, bid))
        ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin: %f" % (symbol, value))
        ret = 'no_margin'
    return ret


# region ### Methods
def calc_amount_alt(price, coin):
    current_balance = poloniexAPI.get_balance(coin)  # make it more flexible...
    print("My trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 8  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance
    return amount

# region ### Methods
def calc_amount_btc(price):
    current_balance = poloniexAPI.get_balance('BTC')  # make it more flexible...
    print("My trade balance = %s at price %f" % (current_balance, price))

    relative_balance = current_balance / 8  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance / price
    return amount

def buy(ask, symbol):
    amount = calc_amount_btc(ask)
    #SYMBOL = 'BTC_ETH'
    print("Buy %s amount = %s at price %f" % (symbol, amount, ask))

    # uncomment to make trades
    #res = poloniexAPI.polo.buy(symbol, ask, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=2.4)  # if you want margin trade
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
    #res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')
    res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=2.4)  # if you want margin trade
    print("Res %s at price %f" % (res, bid))

    #res = 'success'  # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return res


def buy_margin(ask, symbol):
    amount = calc_margin_btc(ask, symbol)
    value = float(amount) * ask
    factor = 0.05  # percentage of total margin avaliable to use on this trade
    print("Buy %s amount = %s at price %f, value %f" % (symbol, amount, ask, value))

    if value > 0.02:  # enough margin to place a trade
        if value * factor > 0.02:  # trade a fraction of available funds
            amount = amount * factor
        elif value * factor * 3 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 3
        elif value * factor * 6 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 6
        elif value * factor * 12 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 12
        else:
            print("Res %s not enough margin: %f" % (symbol, value))
            ret = 'no_margin'
        if ret != 'no_margin':
            res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
            print("Res %s at price %f" % (res, ask))
            ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin balance: %f" % (symbol, value))
        ret = 'no_balance'

    if ret == 'success':
        print("Buy %s amount = %s at price %f, value %f" % (symbol, amount, ask, float(amount) * ask))

    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return ret


def sell_margin(bid, symbol):
    amount = calc_margin_btc(bid, symbol)
    value = float(amount) * bid
    factor = 0.05  # percentage of total margin avaliable to use on this trade
    print("Sell %s amount = %s at price %f, value %f" % (symbol, amount, bid, value))

    if value > 0.02:  # enough margin to place a trade
        if value * factor > 0.02:  # trade a fraction of available funds
            amount = amount * factor
        elif value * factor * 3 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 3
        elif value * factor * 6 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 6
        elif value * factor * 12 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 12
        else:
            print("Res %s not enough margin: %f" % (symbol, value))
            ret = 'no_margin'
        if ret != 'no_margin':
            res = poloniexAPI.sell_margin_api(symbol=symbol, bid=bid, amount=amount)  # if you want margin trade
            print("Res %s at price %f" % (res, bid))
            ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin balance: %f" % (symbol, value))
        ret = 'no_balance'
    else:
        print("Res %s no value from API: %f" % (symbol, value))
        ret = 'no_amount'
    if ret == 'success':
        print("Sell %s amount = %s at price %f, value %f" % (symbol, amount, bid, float(amount) * bid))

    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return ret

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


class ExchangeStrategy:
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

    def get_symbol(self):
        return self.SYMBOL

    def crossover_strategy(self, time_period, fast_period, mid_period, slow_period, confirm_period, trim_count):
        try:
            print("Symbol: %s  " % (self.SYMBOL ))
            time.sleep(0.1)
            price_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=3)
            time.sleep(0.1)
            fast_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=fast_period)
            time.sleep(0.1)  # safe
            slow_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=slow_period)
            time.sleep(0.1)  # safe
            mid_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=mid_period)
            time.sleep(0.1)  # safe
            self.trim  = trim_count
            exit_token = ""

            net_margin = poloniexAPI.get_net_margin()  # btc total value
            alt_margin = poloniexAPI.get_margin_total(self.SYMBOL)
            current_btc = poloniexAPI.get_btc_balance(self.SYMBOL)
            time.sleep(0.1)  # safe

            current_alt = poloniexAPI.get_margin_balance(self.SYMBOL)
            time.sleep(0.1)  # safe
            last_price = poloniexAPI.get_orderbook(self.SYMBOL)
            time.sleep(0.1)  # safe

            pl = poloniexAPI.get_pl(self.SYMBOL)

            print("%s profit and loss %s " % (self.SYMBOL, str(pl)))


            alt_converted = float(current_alt)  * float(last_price['bids'][0][0])
            ask = float(last_price['asks'][0][0])*1.003
            bid = float(last_price['bids'][0][0])*0.997
            current_margin = poloniexAPI.get_current_margin()  # ratio

            margin_type = poloniexAPI.get_margin_type(self.SYMBOL)
            time.sleep(0.2)  # safe
            if margin_type == "short":
                self.is_buy_open = False
                self.is_sell_open = True
            elif margin_type == "long":
                self.is_buy_open = True
                self.is_sell_open = False
            elif margin_type == "none":
                self.is_buy_open = False
                self.is_sell_open = False

            print("%s confirm %.0f at ticket %.0f sell %.0f buy %.0f" % (self.SYMBOL, self.confirm, self.ticket, self.is_sell_open, self.is_buy_open))
            print("%s ask %.8f at bid %.8f alt %.6f btc %.6f" % (self.SYMBOL, ask, bid, alt_converted, current_btc))
            print("slow_ma  %.8f \nmid_ma   %.8f \nfast_ma  %.8f \nprice_ma %.8f" % ( slow_ma, mid_ma,fast_ma,price_ma ))



            # if long position
            if self.is_buy_open:
                price = ask
                if fast_ma < mid_ma:
                    print("%s self fast_ma < mid_ma" % (self.SYMBOL))
                    exit_token = "slow_exit"
                elif price_ma < slow_ma:
                    print("%s self price_ma < slow_ma " % (self.SYMBOL))
                    exit_token = "slow_exit"
                elif fast_ma > slow_ma and fast_ma > mid_ma:
                    print("%s self fast_ma > slow_ma " % (self.SYMBOL ))
                    exit_token = "topup"

            # if short position
            elif self.is_sell_open:
                price = bid
                if fast_ma > mid_ma:
                    print("%s self fast_ma > mid_ma" % (self.SYMBOL))
                    exit_token = "slow_exit"
                elif price_ma > slow_ma:
                    print("%s self price_ma > slow_ma " % (self.SYMBOL))
                    exit_token = "slow_exit"
                elif fast_ma < slow_ma and fast_ma < mid_ma:
                    print("%s self fast_ma < mid_ma < slow_ma " % (self.SYMBOL ))
                    exit_token = "topup"

            # if no positions are open
            elif self.is_sell_open is False and self.is_buy_open is False :
                self.confirm = confirm_period
                if current_margin > 0.42:
                    if  fast_ma < mid_ma and price_ma < slow_ma and price_ma < fast_ma: # and slow_ma <= mid_ma:
                        if self.dont_trade != "sell":
                            print("%s is_sell_open new entry" % (self.SYMBOL ))
                            exit_token = "new_sell"
                        else:
                            print("%s is flagged dont_trade %.0f" % (self.SYMBOL, self.dont_trade ))
                    elif  fast_ma > mid_ma and price_ma > slow_ma and price_ma > fast_ma: #  and slow_ma >= mid_ma:
                        if self.dont_trade != "buy":
                            print("%s is_buy_open new entry" % (self.SYMBOL ))
                            exit_token = "new_buy"

            if self.is_buy_open or self.is_sell_open:  # if open position
                #print("%s Strategy" % (self.SYMBOL))
                if  current_margin < 0.37 :    # if current trades less than minimum desired 38 percent margin
                    print("%s margin less than 38 percent %s " % (self.SYMBOL, str(current_margin)))
                    if pl < -5:
                        if self.is_buy_open:
                            self.dont_trade = "buy"
                        if self.is_sell_open:
                            self.dont_trade = "sell"
                        exit_token = "exit"
                        print("%s fast exit" % (self.SYMBOL))

                    else:
                        exit_token = "slow_exit"
                        print("%s slow exit" % (self.SYMBOL))

                if self.trim > 0:   # if the trim trigger is true then close position
                    print("%s self trim > 0 %.0f " % (self.SYMBOL, self.trim))
                    if pl < -5:
                        if self.is_buy_open:
                            self.dont_trade = "buy"
                        if self.is_sell_open:
                            self.dont_trade = "sell"
                        exit_token = "exit"
                if abs(alt_margin) > net_margin :    # max margin per coin
                    #exit_token = "exit"
                    print("%s alt_converted %f greater than current_margin %f" % (self.SYMBOL, alt_margin, net_margin))

            print("%s exit_token %s" % (self.SYMBOL, exit_token))

            # execute trades
            if exit_token == "exit":
                self.ticket = exit_margin(ask, self.SYMBOL, 1, 1 )
                exit_token = " "
                self.is_buy_open = False
                self.is_sell_open = False
                self.trim = 0

            elif exit_token == "slow_exit":
                if self.ticket < self.confirm:
                    self.ticket = self.ticket + 1
                else:
                    self.ticket = exit_margin(price, self.SYMBOL, self.ticket, confirm_period)
                    self.trim = 0

            elif exit_token == "new_buy" or exit_token == "new_sell":
                print("%s exit_token is %s" % (self.SYMBOL, exit_token))
                if self.ticket < self.confirm:
                    self.ticket = self.ticket + 2
                else:
                    if exit_token == "new_buy":
                        margin_res = buy_margin(ask, self.SYMBOL)
                    elif exit_token == "new_sell":
                        margin_res = sell_margin(bid, self.SYMBOL)
                    print("Margin Res: %s" % (margin_res))
                    if  margin_res == "success":
                        self.ticket = 0
                        self.confirm = 10
                        self.dont_trade = "none"
                    elif margin_res == "no_balance":
                        self.trim = 1

            elif exit_token == "topup":
                if current_margin > 0.45 and pl > 3:  # have margin to spend and trade is profitable
                    if abs(alt_margin) < net_margin * 0.5:  # one position not more than 50% margin
                        if self.ticket < self.confirm:
                            self.ticket = self.ticket + 1
                        else:
                            if self.is_buy_open:
                                margin_res = buy_margin(ask, self.SYMBOL)
                            elif self.is_sell_open:
                                margin_res = sell_margin(bid, self.SYMBOL)
                            print("Margin Res: %s" % (margin_res))
                            if  margin_res == "success":
                                self.ticket = 0
                                self.confirm = 10
                            #elif margin_res == "no_balance":
                                #self.trim = self.trim + 1
                    else:
                        print("%s alt_converted %f greater than half current_margin %f" % (self.SYMBOL, alt_margin, net_margin))
                        self.ticket = 0
                else:
                    self.ticket = 0
        except:
            self.ticket = 0
            raise
            print("%s error 0" % (self.SYMBOL))
            return self.trim


        return self.trim
        #    def supertrend_strategy(self, fast_period, slow_period):
