import poloniexAPI
import time
from Strategy import Strategy
import datetime

# region ### GLOBALS
<<<<<<< HEAD
PERIOD_MA_SLOW = 120
=======
PERIOD_MA_SLOW = 140
>>>>>>> origin/master
PERIOD_MA_MID = 40
PERIOD_MA_FAST = 20
PERIOD_MA_TIME = 15
SYMBOL = 'BTC_ETH'
# endregion


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
    #print('lash high = ' + str(h))
    #print('lash low = ' + str(l))
    #print('lash close = ' + str(c))
    print( str(symbol)+':' + str(c) +' - ' + str(PERIOD_MA_SLOW) + ' ma = ' + str(slow_ma) + ' - ' + str(PERIOD_MA_FAST) + ' ma = ' + str(fast_ma))


if __name__ == "__main__":
    strategy_ltc = Strategy('BTC_LTC')
    strategy_str = Strategy('BTC_STR')
    strategy_xrp = Strategy('BTC_XRP')
    strategy_eth = Strategy('BTC_ETH')
    strategy_fct = Strategy('BTC_FCT')
    strategy_bts = Strategy('BTC_BTS')
    strategy_xmr = Strategy('BTC_XMR')
    strategy_dash = Strategy('BTC_DASH')
    strategy_maid = Strategy('BTC_MAID')
    strategy_doge = Strategy('BTC_DOGE')
    strategy_clam = Strategy('BTC_CLAM')

    current_btc = poloniexAPI.get_btc_balance('BTC_XRP')
    current_str = poloniexAPI.get_balance('BTC_STR')
    current_eth = poloniexAPI.get_balance('BTC_ETH')
    current_xrp = poloniexAPI.get_balance('BTC_XRP')
    current_ltc = poloniexAPI.get_balance('BTC_LTC')
    current_fct = poloniexAPI.get_balance('BTC_FCT')
    current_bts = poloniexAPI.get_balance('BTC_BTS')
    current_xmr = poloniexAPI.get_balance('BTC_XMR')
    current_dash = poloniexAPI.get_balance('BTC_DASH')
    current_maid = poloniexAPI.get_balance('BTC_MAID')
    current_doge = poloniexAPI.get_balance('BTC_DOGE')
    current_clam = poloniexAPI.get_balance('BTC_CLAM')

    current_total =  (current_btc + current_eth + current_xrp + current_ltc + current_fct + current_str +
            current_bts + current_xmr + current_dash + current_maid + current_doge + current_clam )
    #print("Balance:%f -- BTC = %f -- ETH = %f -- XRP = %f" % (current_total, current_btc, current_eth, current_xrp))
    print("Current Total Balance:%f  " % (current_btc))
    print("MA Period:%f  MA Slow:%f  MA Mid:%f  MA Fast:%f  " % (PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST))


    while True:

        current_time = datetime.datetime.now()
        print("Date Time:%s  " % (current_time))

        # one or more strategies below
        strategy_ltc.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_str.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_eth.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_xrp.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_dash.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_bts.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_fct.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_xmr.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
<<<<<<< HEAD
        time.sleep(5)
        strategy_maid.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_doge.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        time.sleep(5)
        strategy_clam.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)

=======
        strategy_maid.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_doge.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
        strategy_clam.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW)
>>>>>>> origin/master
        #test_info(SYMBOL)
        #test_info('BTC_ETH')
        #test_info('BTC_XRP')
        print('--------------')

        time.sleep(5)
