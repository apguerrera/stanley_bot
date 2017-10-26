import poloniexAPI
import time
from Strategy import Strategy
import datetime
import argparse

# region ### GLOBALS

MA_SLOW = 80
MA_MID = 30
MA_FAST = 8
MA_TIME = 120
CONFIRM_TIME = 4

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--fast',  default=MA_FAST, type=int)
    parser.add_argument('--mid',  default=MA_MID, type=int)
    parser.add_argument('--slow',  default=MA_SLOW, type=int)
    parser.add_argument('--time',  default=MA_TIME, type=int)
    parser.add_argument('--confirm',  default=CONFIRM_TIME, type=int)
    args = parser.parse_args()

    PERIOD_MA_SLOW = args.slow
    PERIOD_MA_MID = args.mid
    PERIOD_MA_FAST = args.fast
    PERIOD_MA_TIME = args.time
    PERIOD_CONFIRM = args.confirm

    strategy_ltc = Strategy('BTC_LTC', PERIOD_CONFIRM)
    strategy_str = Strategy('BTC_STR', PERIOD_CONFIRM)
    strategy_xrp = Strategy('BTC_XRP', PERIOD_CONFIRM)
    strategy_eth = Strategy('BTC_ETH', PERIOD_CONFIRM)
    strategy_fct = Strategy('BTC_FCT', PERIOD_CONFIRM)
    strategy_bts = Strategy('BTC_BTS', PERIOD_CONFIRM)
    strategy_xmr = Strategy('BTC_XMR', PERIOD_CONFIRM)
    strategy_dash = Strategy('BTC_DASH', PERIOD_CONFIRM)
    strategy_maid = Strategy('BTC_MAID', PERIOD_CONFIRM)
    strategy_doge = Strategy('BTC_DOGE', PERIOD_CONFIRM)
    strategy_clam = Strategy('BTC_CLAM', PERIOD_CONFIRM)

    print("MA Period:%f  MA Slow:%f  MA Mid:%f  MA Fast:%f  Confirm:%s " % (PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM))

    trim = 0

    while True:

        current_time = datetime.datetime.now()
        print("Date Time:%s  " % (current_time))

        # one or more strategies below
        trim = strategy_ltc.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        #trim = strategy_str.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        print("Trim:%s  " % (str(trim)))
        trim = strategy_eth.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM , trim_count=trim)
        print("Trim:%s  " % (str(trim)))

        trim = strategy_xrp.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        print("Trim:%s  " % (str(trim)))
        trim = strategy_dash.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        trim = strategy_bts.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        print("Trim:%s  " % (str(trim)))
        trim = strategy_fct.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        trim = strategy_xmr.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        print("Trim:%s  " % (str(trim)))
        trim = strategy_maid.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        #trim = strategy_doge.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
        trim = strategy_clam.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)


        #test_info(SYMBOL)
        #test_info('BTC_ETH')
        #test_info('BTC_XRP')
        print('--------------')

        time.sleep(5)
