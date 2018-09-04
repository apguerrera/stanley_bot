import poloniexAPI
import time
import sys
import boto3  #pip install boto3

import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
#clientdb = boto3.client('dynamodb')
sleep = 2
# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.

#response = clientdb.list_tables()
#print(response)

db_table = dynamodb.Table('stanley_bot')

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


def buy_margin(ask, symbol, trade_msg):
    amount = calc_margin_btc(ask, symbol)
    value = float(amount) * ask
    factor = 0.05  # percentage of total margin avaliable to use on this trade
    print(trade_msg)
    print("Buy %s amount = %s at price %f, value %f" % (symbol, amount, ask, value))
    ret = 'margin'
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
        if ret == 'margin':
            res = poloniexAPI.polo.marginBuy(symbol, ask, amount, lendingRate=0.02)  # if you want margin trade
            print("Res %s at price %f" % (res, ask))
            time.sleep(sleep)  # safe
            margin = poloniexAPI.polo.getMarginPosition(symbol)
            ret_db = db_table.put_item(
               Item={
                    'symbol': symbol,
                    'trade_ts':str(int(time.time())),
                    'trade_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'price': str('{:.8f}'.format(ask)),
                    'amount': str('{:.8f}'.format(abs(float(margin["total"])))),
                    'trade': 'buy_margin',
                    'trade_msg': str(trade_msg),
                    'pl': str('0.0'),
                    'res': str(res),
                }
            )
            print("Db entry added: %s" % (ret_db))


            ret = 'success'
    elif value < 0.02:
        print("Res %s not enough margin balance: %f" % (symbol, value))
        ret = 'no_balance'

    if ret == 'success':
        print("Buy %s amount = %s at price %f, value %f" % (symbol, amount, ask, float(amount) * ask))

    #if res != 'success':
    #    raise BaseException('### Trade Buy error')
    return ret


def sell_margin(bid, symbol, trade_msg):
    amount = calc_margin_btc(bid, symbol)
    value = float(amount) * bid
    factor = 0.05  # percentage of total margin avaliable to use on this trade
    print(trade_msg)
    print("Sell %s amount = %s at price %f, value %f" % (symbol, amount, bid, value))
    ret = 'margin'
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
        if ret == 'margin':
            res = poloniexAPI.sell_margin_api(symbol=symbol, bid=bid, amount=amount)  # if you want margin trade
            print("Res %s at price %f" % (res, bid))
            time.sleep(sleep)  # safe
            margin = poloniexAPI.polo.getMarginPosition(symbol)
            ret_db = db_table.put_item(
               Item={
                    'symbol': symbol,
                    'trade_ts':str(int(time.time())),
                    'trade_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'price': str('{:.8f}'.format(bid)),
                    'amount': str('{:.8f}'.format(abs(float(margin["total"])))),
                    'trade': 'sell_margin',
                    'trade_msg': str(trade_msg),
                    'pl': str('0.0'),
                    'res': str(res),
                }
            )
            print("Db entry added: %s" % (ret_db))

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

def exit_margin(price, symbol, ticket, confirm, trade_msg):
    if ticket < confirm:
        print("Exit ticket: %s" % (str(ticket)))
        ticket = ticket + 1
    else:
        print(trade_msg)
        margin = poloniexAPI.polo.getMarginPosition(symbol)
        print("Exit ticket close: %s Margin: %s" % (str(ticket), str(margin["total"])))
        time.sleep(sleep)
        pl = poloniexAPI.get_pl(symbol)
        print(pl)
        time.sleep(sleep)
        res = poloniexAPI.polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
        print("Res %s at price %f" % (res, price))
        ret_db = db_table.put_item(
            Item={
                 'symbol': symbol,
                 'trade_ts':str(int(time.time())),
                 'trade_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                 'price': str('{:.8f}'.format(price)),
                 'amount': str('{:.8f}'.format(abs(float(margin["total"])))),
                 'trade': 'exit_margin',
                 'trade_msg': str(trade_msg),
                 'pl': str(pl),
                 'res': str(res)
            }
        )
        print("Db entry added: %s" % (ret_db))
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
        self.dont_trade = "none"
        self.max_pl = 0.0

    def get_symbol(self):
        return self.SYMBOL

    def crossover_strategy(self, time_period, fast_period, mid_period, slow_period, confirm_period, trim_count):
        try:

            print("Symbol: %s  " % (self.SYMBOL ))
            time.sleep(sleep)
            price_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=3)
            time.sleep(sleep)
            fast_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=fast_period)
            time.sleep(sleep)  # safe
            slow_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=slow_period)
            time.sleep(sleep)  # safe
            mid_ma = poloniexAPI.get_ma(self.SYMBOL, timeframe=time_period, period=mid_period)
            time.sleep(sleep)  # safe
            self.trim  = trim_count
            exit_token = ""
            trade_msg = ""

            net_margin = poloniexAPI.get_net_margin()  # btc total value
            alt_margin = poloniexAPI.get_margin_total(self.SYMBOL) # total margin amount in BTC
            current_btc = poloniexAPI.get_btc_balance(self.SYMBOL)
            time.sleep(sleep)  # safe

            current_alt = poloniexAPI.get_margin_balance(self.SYMBOL)
            time.sleep(sleep)  # safe
            last_price = poloniexAPI.get_orderbook(self.SYMBOL)
            time.sleep(sleep)  # safe

            pl = poloniexAPI.get_pl(self.SYMBOL)
            self.max_pl = max(float(self.max_pl),float(pl))
            print("%s profit and loss %.3f. max_pl = %.3f " % (self.SYMBOL, pl, self.max_pl))


            alt_converted = float(current_alt)  * float(last_price['bids'][0][0])
            ask = float(last_price['asks'][0][0])*1.003
            bid = float(last_price['bids'][0][0])*0.997
            current_margin = poloniexAPI.get_current_margin()  # ratio

            margin_type = poloniexAPI.get_margin_type(self.SYMBOL)
            time.sleep(sleep)  # safe
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
                if fast_ma < mid_ma and price_ma < fast_ma:
                    trade_msg = "%s self fast_ma < mid_ma" % (self.SYMBOL)
                    exit_token = "slow_exit"
                elif price_ma < slow_ma:
                    trade_msg ="%s self price_ma < slow_ma " % (self.SYMBOL)
                    exit_token = "slow_exit"
                elif fast_ma > slow_ma and fast_ma > mid_ma:
                    trade_msg = "%s self fast_ma > slow_ma " % (self.SYMBOL )
                    exit_token = "topup"

            # if short position
            elif self.is_sell_open:
                price = bid
                if fast_ma > mid_ma and price_ma > fast_ma:
                    trade_msg = "%s self fast_ma > mid_ma" % (self.SYMBOL)
                    exit_token = "slow_exit"
                elif price_ma  > slow_ma:     # exit on reversal
                    trade_msg = "%s self price_ma > slow_ma " % (self.SYMBOL)
                    exit_token = "slow_exit"
                elif fast_ma < slow_ma and fast_ma < mid_ma:  # top up if successful
                    trade_msg = "%s self fast_ma < mid_ma < slow_ma " % (self.SYMBOL )
                    exit_token = "topup"

            # New trades signals if no positions are open
            elif self.is_sell_open is False and self.is_buy_open is False :
                self.confirm = confirm_period
                if current_margin > 0.42:
                    if  fast_ma < (0.999 * mid_ma) and price_ma < slow_ma and price_ma < mid_ma and price_ma < fast_ma: # and slow_ma <= mid_ma:

                        if self.dont_trade != "sell":
                            trade_msg = "%s is_sell_open new entry" % (self.SYMBOL )
                            exit_token = "new_sell"
                        else:
                            print("%s is flagged dont_trade %s" % (self.SYMBOL, self.dont_trade ))
                    elif  fast_ma > (1.001 * mid_ma) and price_ma > slow_ma and price_ma > mid_ma and price_ma > fast_ma: #  and slow_ma >= mid_ma:
                        if self.dont_trade != "buy":
                            trade_msg = "%s is_buy_open new entry" % (self.SYMBOL )
                            exit_token = "new_buy"
                        else:
                            print("%s is flagged dont_trade %s" % (self.SYMBOL, self.dont_trade ))
            if self.is_buy_open or self.is_sell_open:  # if open position

                #print("%s Strategy" % (self.SYMBOL))
                if  current_margin < 0.38 :    # if current trades less than minimum desired 38 percent margin
                    print("%s margin less than 38 percent %s " % (self.SYMBOL, str(current_margin)))
                    if pl < -2:
                        if self.is_buy_open:
                            self.dont_trade = "buy"
                        if self.is_sell_open:
                            self.dont_trade = "sell"
                        exit_token = "exit"
                        trade_msg = "%s fast exit < 2pc" % (self.SYMBOL)

                    else:
                        exit_token = "slow_exit"
                        trade_msg = "%s slow exit < 38pc margin" % (self.SYMBOL)

                if pl < (self.max_pl - 10):
                    if self.is_buy_open:
                        self.dont_trade = "buy"
                    if self.is_sell_open:
                        self.dont_trade = "sell"
                    exit_token = "exit"
                    trade_msg = "%s exit < 13pc hard stop loss " % (self.SYMBOL)

                if pl < (self.max_pl - 9):
                    exit_token = "slow_exit"
                    trade_msg = "%s slow_exit < 10pc stop loss " % (self.SYMBOL)

                if pl < (self.max_pl - 6) and abs(alt_margin) > 0.07:   # stop loss for bigger trades
                    exit_token = "slow_exit"
                    trade_msg = "%s slow_exit < 8pc with high margin " % (self.SYMBOL)

                if self.trim > 0:   # if the trim trigger is true then close position
                    print("%s self trim > 0 %.0f " % (self.SYMBOL, self.trim))
                    if pl < -2:
                        if self.is_buy_open:
                            self.dont_trade = "buy"
                        if self.is_sell_open:
                            self.dont_trade = "sell"
                        exit_token = "exit"
                        trade_msg = "%s exit_token %s" % (self.SYMBOL, exit_token)

                if abs(alt_margin) > net_margin :    # max margin per coin
                    #exit_token = "exit"
                    print("%s alt_converted %f greater than current_margin %f" % (self.SYMBOL, alt_margin, net_margin))

            # execute trades
            if exit_token == "exit":   # exit open trade
                self.ticket = exit_margin(ask, self.SYMBOL, 1, 1, trade_msg )
                exit_token = " "
                self.is_buy_open = False
                self.is_sell_open = False
                self.trim = 0
                self.max_pl = 0

            # exit after confirmation
            elif exit_token == "slow_exit":
                if self.ticket < confirm_period:
                    self.ticket = self.ticket + 1
                else:
                    self.ticket = exit_margin(price, self.SYMBOL, self.ticket, confirm_period, trade_msg)
                    self.trim = 0
                    exit_token = " "
                    self.max_pl = 0

            # new trade signals
            elif exit_token == "new_buy" or exit_token == "new_sell":
                print("%s exit_token is %s" % (self.SYMBOL, exit_token))
                if self.ticket < self.confirm:
                    self.ticket = self.ticket + 2
                else:
                    if exit_token == "new_buy":
                        margin_res = buy_margin(ask, self.SYMBOL, trade_msg)
                    elif exit_token == "new_sell":
                        margin_res = sell_margin(bid, self.SYMBOL, trade_msg)
                    print("Margin Res: %s" % (margin_res))
                    if  margin_res == "success":
                        self.ticket = 0
                        self.confirm = 10
                        self.dont_trade = "none"
                    elif margin_res == "no_balance":
                        self.trim = 1

            # top up successful trades
            elif exit_token == "topup":
                if current_margin > 0.60 and pl > 3:  # have margin to spend and trade is profitable
                    if abs(alt_margin) < net_margin * 0.5:  # one position not more than 50% margin
                        if self.ticket < self.confirm:
                            self.ticket = self.ticket + 1
                        else:
                            if self.is_buy_open:
                                margin_res = buy_margin(ask, self.SYMBOL, trade_msg)
                            elif self.is_sell_open:
                                margin_res = sell_margin(bid, self.SYMBOL, trade_msg)
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
