import requests
import time

import poloniex  # pip/ pip3 install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.6.zip

from passwords import PRIVATE_API_KEY, PRIVATE_SECRET_KEY
from collections import defaultdict

api_key = PRIVATE_API_KEY
secret_key = PRIVATE_SECRET_KEY

polo = poloniex.Poloniex(api_key, secret_key)

#print(": %s  " % (polo))

# ### Methods
def get_orderbook(symbol='BTC_ETH'):
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    r = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair=' + symbol + '&depth=1', headers={"USER-AGENT":u_a})
    return r.json()


def get_chart_data(symbol='BTC_ETH', timeframe=5, period=120):
    """
    Get OHLC data of selected symbol
    :param symbol:
    :param timeframe: Bars timeframe (5,15,30, etc)
    :param period: Depth. Number of bars back to history
    :return: Returns JSON formatted data
    """
    timeframe_seconds = timeframe * 60
    start_time = time.time() - period * timeframe_seconds  # ~ 120 * 5, back to 120 5-min bars
    req = 'https://poloniex.com/public?command=returnChartData&currencyPair=' \
          + symbol + '&start=' + str(start_time) \
          + '&end=9999999999&period=' + str(timeframe_seconds)
    try:
        r = requests.get(req)
        res = r.json()
    except:
        raise ValueError(str(res) + ' e.g. 5,15,30,60 etc...')
        return res

    return res


def get_ma(symbol, timeframe, period, source='close'):
    """
    Calculate moving average (default by Close). Returns Moving Average value
    :param symbol:
    :param timeframe: Bars timeframe (5,15,30, etc)
    :param period:
    :param source: Default calculate MA by Close. Select Open, High, Close of Low.
    :return: Moving Average value
    """
    c = 0
    while (c < period):
        s = 0
        c = 0
        data = get_chart_data(symbol, timeframe, period)

        for item in data:
            s += float(item[source])
            c += 1


    return s / period



def get_ma_fms(symbol, timeframe, slow_period, mid_period, fast_period, source='close'):
    """
    Calculate moving average (default by Close). Returns Moving Average value
    :param symbol:
    :param timeframe: Bars timeframe (5,15,30, etc)
    :param period:
    :param source: Default calculate MA by Close. Select Open, High, Close of Low.
    :return: Moving Average value
    """
    c = 0
    while (c < slow_period):
        s = 0
        m = 0
        f = 0
        c = 0
        data = get_chart_data(symbol, timeframe, period)

        for item in data:
            s += float(item[source])
            if (c < mid_period):
                m += float(item[source])
            if (c < fast_period):
                f += float(item[source])
            c += 1

    slow_ma = s / slow_period
    mid_ma = m / mid_period
    fast_ma = f / fast_period
    return slow_ma, mid_ma, fast_ma

def sell_margin_api(symbol, bid, amount):
    res = polo.marginSell(symbol, rate=bid, amount=amount, lendingRate=0.02)  # if you want margin trade
    return res

def get_balance(symbol):
    my_dict = defaultdict(int)
    coin =  symbol.replace("BTC_", "")
    balance = polo.returnAvailableAccountBalances()
    if coin in balance:
        bal_sym = balance["margin"][coin]
    else:
        bal_sym = 0
    #print("I have %s %s!" % (bal_sym, symbol) )
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(bal_sym)

def get_btc_balance(symbol):
    balance = polo.returnTradableBalances()
    #bal_sym = balance[symbol]
    coin_balance = float(balance[symbol]["BTC"])
    relative_balance = coin_balance*0.9  # 2= 50% of current balance
    #print("I have %s %s!" % (balance[symbol]["BTC"], symbol) )
    #print("I have %s %s!" % ( bal_sym["btcValue"], symbol))
    return float(relative_balance)

    #return float(bal_sym["btcValue"])

def get_margin_type(symbol):
    margin = polo.getMarginPosition(currencyPair=symbol)
    margin_type = margin["type"]
    if margin_type != "none":
        print("Margin for %s with position %s" % (symbol, margin_type.upper() ))
    else:
        print("Margin for %s with position %s" % (symbol, margin_type))

    #print("Margin for %s with total %f" % (symbol, margin_total))
    #print("I have %s %s symbol!" % ( balance, symbol))

    return margin_type
    #return margin

def get_margin_balance(symbol):
    coin =  symbol.replace("BTC_", "")
    balance = polo.returnTradableBalances()
    coin_balance = float(balance[symbol][coin])
    relative_balance = coin_balance*0.95  # 2= 50% of current balance
    #print("My malt trade balance = %s at price %f" % (coin, coin_balance))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(relative_balance)

def get_current_margin():
    balance = polo.returnMarginAccountSummary()
    #print("My current margin = %s" % (balance["currentMargin"]))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(balance["currentMargin"])

def exit_buy_margin(ask, symbol):
    res = polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
    print("Res %s at price %f" % (res, ask))
    return res

def exit_sell_margin(bid, symbol):
    res = polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
    print("Res %s at price %f" % (res, bid))
    return res

def exit_close_margin(price, symbol):
    res = polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
    print("Res %s at price %f" % (res, price))
    return res

def get_trade_history(symbol):
    res = polo.returnTradeHistory(currencyPair=symbol, limit=1)  # close margin trade
    print("Res %s " % (res))
    return res

def get_margin_total(symbol):
    margin = polo.getMarginPosition(currencyPair=symbol)
    margin_total = float(margin["total"])
    #print("%s with total %f" % (symbol, margin_total))
    print("%s Total %.0f Amount %.2f Base %.8f " % (symbol, margin_total, float(margin["amount"]), float(margin["basePrice"]) ))

    #{"amount":"40.94717831","total":"-0.09671314",""basePrice":"0.00236190","liquidationPrice":-1,"pl":"-0.00058655", "lendingFees":"-0.00000038","type":"long"}
    return margin_total
    #return margin

def get_net_margin():
    #print("My net balance calculating")
    balance = polo.returnMarginAccountSummary()
    #print("My net balance = %s" % (balance["netValue"]))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(balance["netValue"])


def test_info(symbol):
    slow_ma = poloniexAPI.get_ma(symbol, timeframe=PERIOD_MA_TIME, period=PERIOD_MA_SLOW)
    time.sleep(0.2)  # safe
    fast_ma = poloniexAPI.get_ma(symbol, timeframe=PERIOD_MA_TIME, period=PERIOD_MA_FAST)

    ohlc = poloniexAPI.get_chart_data(symbol, period=PERIOD_MA_SLOW)
    o = ohlc[-1]['open']
    h = ohlc[-2]['high']
    l = ohlc[-2]['low']
    c = ohlc[-2]['close']
    #print('current open = ' + str(o))

    print( str(symbol)+':' + str(c) +' - ' + str(PERIOD_MA_SLOW) + ' ma = ' + str(slow_ma) + ' - ' + str(PERIOD_MA_FAST) + ' ma = ' + str(fast_ma))

def net_margin():
    time.sleep(0.2)  # safe
    print("My net balance calculating")

    balance = polo.returnMarginAccountSummary()
    net_value = float(balance["netValue"])
    print("Net Value = %.5f  " % (net_value))

    current_margin = 100 * float(balance["currentMargin"])
    print("Current Margin = %.2f %s " % (current_margin, "%"))

def trim_position(trim, symbols):
     if trim > 0:
         print('--------------')
         for item in symbols:
             test = item.split('_')[1].lower()
         print("Trimmed position = %s Trim = %s" % (test, str(trim)))

def get_pl(symbol):
    test = polo.getMarginPosition(currencyPair=symbol)
    if abs(float(test["total"])) == 0 :
        ratio = 0
    else:
        ratio = 100 * float(test["pl"])/ abs(float(test["total"]))

    print("PL: %.2f Margin: %.8f Profit: %.6f" % (float(ratio), float(test["total"]), float(test["pl"]) ))

    return ratio
