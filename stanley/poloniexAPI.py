import requests
import time
import poloniex  # pip3 install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.3.zip

from passwords import PRIVATE_API_KEY, PRIVATE_SECRET_KEY

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
    data = get_chart_data(symbol, timeframe, period)
    s = 0
    for item in data:
        s += float(item[source])
    return s / period


def get_balance(symbol):
    balance = polo.returnAvailableAccountBalances()
    bal_sym = balance["exchange"]

    print("I have %s %s!" % (balance[symbol], symbol) )
    print("I have %s %s!" % ( bal_sym[symbol], symbol))
    return float(bal_sym[symbol])

def get_btc_balance(symbol):
    balance = polo.returnCompleteBalances(account='exchange')
    bal_sym = balance[symbol]

    #print("I have %s %s!" % (balance[symbol], symbol) )
    #print("I have %s %s!" % ( bal_sym[symbol], symbol))
    return float(bal_sym["btcValue"])
