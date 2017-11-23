import poloniexAPI
import time
import sys


# region ### Methods
def calc_margin_alt(price, symbol):
    current_balance = poloniexAPI.polo.returnTradableBalances()  # make it more flexible...
    coin =  symbol.replace("BTC_", "")
    coin_balance = float(current_balance[symbol][coin])
    relative_balance = coin_balance*0.95  # 95% of current balance for buffer
    print("My malt margin balance = %s at price %f" % (relative_balance, price))

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

    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return ret


def sell_margin_amount(bid, symbol, amount):

    #amount = calc_margin_alt(bid, symbol)
    value = float(amount) * bid
    #factor = 0.2
    print("Sell %s Amount = %s at price %f, value %f" % (symbol, amount, bid, value))

    if value > 0.02:
        res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=0.02)  # if you want margin trade
        print("Res %s at price %f" % (res, bid))
        ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin: %f" % (symbol, value))
        ret = 'no_margin'
     # fix it when uncomment!
    #if res != 'success':
    #    raise BaseException('### Trade Sell error')
    return ret


def buy_margin(ask, symbol):
    amount = calc_margin_btc(ask, symbol)
    value = float(amount) * ask
    factor = 0.10  # percentage of total margin avaliable to use on this trade
    print("Buy %s amount = %s at price %f, value %f" % (symbol, amount, ask, value))

    if value > 0.02:  # enough margin to place a trade
        if value * factor > 0.02:  # trade a fraction of available funds
            amount = amount * factor
            res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
            print("Res %s at price %f" % (res, ask))
            ret = 'success'
        elif value * factor * 3 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 3
            res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
            print("Res %s at price %f" % (res, ask))
            ret = 'success'
        elif value * factor * 6 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 6
            res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
            print("Res %s at price %f" % (res, ask))
            ret = 'success'
        else:
            print("Res %s not enough margin: %f" % (symbol, value))
            ret = 'no_margin'
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
    factor = 0.10  # percentage of total margin avaliable to use on this trade
    print("Sell %s amount = %s at price %f, value %f" % (symbol, amount, bid, value))

    if value > 0.02:  # enough margin to place a trade
        if value * factor > 0.02:  # trade a fraction of available funds
            amount = amount * factor
            res = poloniexAPI.sell_margin_api(symbol=symbol, bid=bid, amount=amount)  # if you want margin trade
            print("Res %s at price %f" % (res, bid))
            ret = 'success'
        elif value * factor * 3 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 3
            res = poloniexAPI.sell_margin_api(symbol=symbol, bid=bid, amount=amount)  # if you want margin trade
            print("Res %s at price %f" % (res, bid))
            ret = 'success'
        elif value * factor * 6 > 0.02:  # trade with remaining margin available > 0.02 btc
            amount = amount * factor * 6
            res = poloniexAPI.sell_margin_api(symbol=symbol, bid=bid, amount=amount)  # if you want margin trade
            print("Res %s at price %f" % (res, bid))
            ret = 'success'
        else:
            print("Res %s not enough margin: %f" % (symbol, value))
            ret = 'no_margin'
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


class Strategy:
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

    def crossover_strategy(self, time_period, fast_period, mid_period, slow_period, confirm_period, trim_count):
        try:
            print("Symbol: %s  " % (self.SYMBOL ))
            time.sleep(0.2)
            price_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=3)
            time.sleep(0.2)
            fast_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=fast_period)
            time.sleep(0.2)  # safe
            slow_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=slow_period)
            time.sleep(0.2)  # safe
            mid_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=mid_period)
            time.sleep(0.2)  # safe
            self.trim  = trim_count
            exit_token = ""

            net_margin = poloniexAPI.get_net_margin()  # btc total value
            alt_margin = poloniexAPI.get_margin_total(self.SYMBOL)
            current_btc = poloniexAPI.get_btc_balance(self.SYMBOL)
            time.sleep(0.2)  # safe

            current_alt = poloniexAPI.get_margin_balance(self.SYMBOL)
            time.sleep(0.2)  # safe
            last_price = poloniexAPI.get_orderbook(self.SYMBOL)
            time.sleep(0.2)  # safe

            pl = poloniexAPI.get_pl(self.SYMBOL) #+ "%"

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



            if self.is_buy_open or self.is_sell_open:
                #print("%s Strategy" % (self.SYMBOL))
                if  current_margin < 0.38 :    # max margin per coin
                    print("%s margin less than 38 percent %s " % (self.SYMBOL, str(current_margin)))
                    exit_token = "exit"
                if self.trim > 0:
                    print("%s self trim > 0 %.0f " % (self.SYMBOL, self.trim))
                    self.trim = 0
                    #exit_token = "exit"
                if abs(alt_margin) > net_margin :    # max margin per coin
                    exit_token = "exit"
                    print("%s alt_converted %f greater than current_margin %f" % (self.SYMBOL, alt_margin, net_margin))

                if exit_token == "exit":
                    self.ticket = exit_margin(ask, self.SYMBOL, 1, 1 )
                    exit_token = " "
                    self.is_buy_open = False
                    self.is_sell_open = False

            if self.is_buy_open:
                if fast_ma < mid_ma:
                    print("%s self fast_ma < mid_ma" % (self.SYMBOL))
                    self.ticket = exit_margin(ask, self.SYMBOL, self.ticket, confirm_period )
                elif price_ma < slow_ma:
                    print("%s self price_ma < slow_ma " % (self.SYMBOL))
                    self.ticket = exit_margin(ask, self.SYMBOL, self.ticket, confirm_period )

                elif fast_ma > slow_ma:
                    print("%s self fast_ma > slow_ma " % (self.SYMBOL ))
                    if current_margin > 0.50:
                        if fast_ma > mid_ma and abs(alt_margin) < net_margin * 0.5:
                            if self.ticket < self.confirm:
                                self.ticket = self.ticket + 1
                            else:
                                margin_res = buy_margin(ask, self.SYMBOL)
                                print("Margin Res: %s" % (margin_res))
                                if  margin_res == "success":
                                    self.ticket = 0
                                    self.confirm = 20
                                elif margin_res == "no_balance":
                                    self.trim = self.trim + 1
                        else:
                            print("%s alt_converted %f greater than half current_margin %f" % (self.SYMBOL, alt_margin, net_margin))
                            self.ticket = 0
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0

            elif self.is_sell_open:
                if fast_ma > mid_ma:
                    print("%s self fast_ma > mid_ma" % (self.SYMBOL))
                    self.ticket = exit_margin(bid, self.SYMBOL, self.ticket, confirm_period)
                elif price_ma > slow_ma:
                    print("%s self price_ma > slow_ma  " % (self.SYMBOL ))
                    self.ticket = exit_margin(bid, self.SYMBOL, self.ticket, confirm_period)

                elif fast_ma < slow_ma:
                    print("%s self fast_ma < slow_ma" % (self.SYMBOL ))
                    if  current_margin > 0.50:
                        if fast_ma < mid_ma and abs(alt_margin) < net_margin * 0.5:
                            if self.ticket < self.confirm:
                                self.ticket = self.ticket + 1
                            else:
                                margin_res = sell_margin(bid, self.SYMBOL)
                                print("Margin Res: %s" % (margin_res))
                                if  margin_res == "success":
                                    self.ticket = 0
                                    self.confirm = 20
                                elif margin_res == "no_balance":
                                    self.trim = self.trim + 1
                        else:
                            print("%s alt_converted %f greater than half current_margin %f" % (self.SYMBOL, alt_margin, net_margin))
                            self.ticket = 0
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0


            elif self.is_sell_open is False and self.is_buy_open is False :
                self.confirm = confirm_period
                if current_margin > 0.42:
                    if  fast_ma < mid_ma and price_ma < slow_ma : # and slow_ma <= mid_ma:
                        print("%s is_sell_open new entry" % (self.SYMBOL ))
                        if self.ticket < self.confirm:
                            self.ticket = self.ticket + 2
                        else:
                            margin_res = sell_margin(bid, self.SYMBOL)
                            print("Margin Res: %s" % (margin_res))
                            if  margin_res == "success":
                                self.ticket = 0
                                self.confirm = 20
                            elif margin_res == "no_balance":
                                self.trim = self.trim + 1

                    elif  fast_ma > mid_ma and price_ma > slow_ma: #  and slow_ma >= mid_ma:
                        print("%s is_buy_open new entry" % (self.SYMBOL ))
                        if self.ticket < self.confirm:
                            self.ticket = self.ticket + 2
                        else:
                            margin_res = buy_margin(ask, self.SYMBOL)
                            print("Margin Res: %s" % (margin_res))
                            if  margin_res == "success":
                                self.ticket = 0
                                self.confirm = 20
                            elif margin_res == "no_balance":
                                self.trim = self.trim + 1
                    else:
                        #print("%s no trade Ticket %.0f " % (self.SYMBOL, self.ticket))
                        self.ticket = 0

        except:
            self.ticket = 0
            print("%s error 0" % (self.SYMBOL))
            raise
            return self.trim


        return self.trim
        #    def supertrend_strategy(self, fast_period, slow_period):
