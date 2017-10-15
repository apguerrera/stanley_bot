import requests
import time
import poloniex  # pip3 install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.3.zip

from passwords import PRIVATE_API_KEY, PRIVATE_SECRET_KEY
from collections import defaultdict

api_key = PRIVATE_API_KEY
secret_key = PRIVATE_SECRET_KEY

polo = poloniex.Poloniex(api_key, secret_key)


# ### Methods
def get_orderbook(symbol='BTC_ETH'):
    r = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair=' + symbol + '&depth=1')
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
    r = requests.get(req)
    res = r.json()
    if 'error' in res:
        raise ValueError(str(res) + ' e.g. 5,15,30,60 etc...')
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
    print("Margin for %s with position %s" % (symbol, margin_type))

    #print("Margin for %s with total %f" % (symbol, margin_total))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return margin_type
    #return margin

def get_margin_balance(symbol):
    coin =  symbol.replace("BTC_", "")
    balance = polo.returnTradableBalances()
    coin_balance = float(balance[symbol][coin])
    relative_balance = coin_balance*0.90  # 2= 50% of current balance

    print("My malt trade balance = %s at price %f" % (coin, coin_balance))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(relative_balance)

def get_current_margin():

    balance = polo.returnMarginAccountSummary()
    print("My current margin = %s" % (balance["currentMargin"]))
    #print("I have %s %s symbol!" % ( balance, symbol))
    return float(balance["currentMargin"])
