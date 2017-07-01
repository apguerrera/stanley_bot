import poloniexAPI
import time
from Strategy import Strategy

# region ### GLOBALS
PERIOD_MA_SLOW = 120
PERIOD_MA_FAST = 20
SYMBOL = 'BTC_ETH'
# endregion


def test_info(symbol):
    slow_ma = poloniexAPI.get_ma(symbol, timeframe=5, period=PERIOD_MA_SLOW)
    time.sleep(0.1)  # safe
    fast_ma = poloniexAPI.get_ma(symbol, timeframe=5, period=PERIOD_MA_FAST)

    ohlc = poloniexAPI.get_chart_data(symbol, period=PERIOD_MA_SLOW)
    o = ohlc[-1]['open']
    h = ohlc[-2]['high']
    l = ohlc[-2]['low']
    c = ohlc[-2]['close']
    #print('current open = ' + str(o))
    #print('lash high = ' + str(h))
    #print('lash low = ' + str(l))
    #print('lash close = ' + str(c))
    print( str(symbol)+':' + str(c) +' - ' + str(PERIOD_MA_SLOW) + ' ma = ' + str(slow_ma) + ' - ' + str(PERIOD_MA_FAST) + ' ma = ' + str(fast_ma))


if __name__ == "__main__":
    strategy_eth = Strategy('BTC_ETH')
    strategy_xrp = Strategy('BTC_XRP')

    while True:
        #test_info(SYMBOL)
        test_info('BTC_ETH')
        test_info('BTC_XRP')
        print('--------------')

        current_btc = poloniexAPI.get_balance('BTC')
        #current_eth = poloniexAPI.get_balance('ETH')
        #current_xrp = poloniexAPI.get_balance('XRP')
        #current_total = poloniexAPI.get_btc_balance('BTC') + poloniexAPI.get_btc_balance('ETH') + poloniexAPI.get_btc_balance('XRP')
        #print("Balance:%f -- BTC = %f -- ETH = %f -- XRP = %f" % (current_total, current_btc, current_eth, current_xrp))

        # one or more strategies below
        #strategy_eth.crossover_strategy(fast_period=PERIOD_MA_FAST, slow_period=PERIOD_MA_SLOW)
        #strategy_xrp.crossover_strategy(fast_period=PERIOD_MA_FAST, slow_period=PERIOD_MA_SLOW)

        time.sleep(5)
