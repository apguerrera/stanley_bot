import poloniexAPI
import time
from Strategy import Strategy

# region ### GLOBALS
PERIOD_MA_SLOW = 120
PERIOD_MA_MID = 60
PERIOD_MA_FAST = 20
PERIOD_MA_TIME = 5
SYMBOL = 'BTC_ETH'
# endregion


def test_info(symbol):
    slow_ma = poloniexAPI.get_ma(symbol, timeframe=5, period=PERIOD_MA_SLOW)
    time.sleep(0.2)  # safe
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
    strategy_ltc = Strategy('BTC_LTC')
    strategy_str = Strategy('BTC_STR')
    strategy_eth = Strategy('BTC_ETH')
    strategy_xrp = Strategy('BTC_XRP')
    strategy_fct = Strategy('BTC_FCT')

    while True:


        current_btc = poloniexAPI.get_btc_balance('BTC_XRP')
        current_eth = poloniexAPI.get_balance('BTC_ETH')
        current_xrp = poloniexAPI.get_balance('BTC_XRP')
        current_ltc = poloniexAPI.get_balance('BTC_LTC')
        current_fct = poloniexAPI.get_balance('BTC_FCT')
        current_total =  current_btc + current_eth + current_xrp + current_ltc + current_fct
        #print("Balance:%f -- BTC = %f -- ETH = %f -- XRP = %f" % (current_total, current_btc, current_eth, current_xrp))
        print("Balance:%f  " % (current_btc))

        # one or more strategies below
        strategy_ltc.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_str.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_eth.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_xrp.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_fct.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)

        #test_info(SYMBOL)
        #test_info('BTC_ETH')
        test_info('BTC_XRP')
        print('--------------')

        time.sleep(5)
