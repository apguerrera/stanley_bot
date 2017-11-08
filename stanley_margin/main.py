import poloniexAPI
import time
from Strategy import Strategy
import datetime
import argparse

# region ### GLOBALS

MA_SLOW = 120
MA_MID = 30
MA_FAST = 10
MA_TIME = 120
CONFIRM_TIME = 3
symbols = ['BTC_LTC', 'BTC_XRP', 'BTC_ETH','BTC_FCT','BTC_BTS','BTC_XMR','BTC_DASH','BTC_MAID','BTC_CLAM', 'BTC_STR']
# endregion

def init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM):
    print("MA Period:%f  MA Slow:%f  MA Mid:%f  MA Fast:%f  Confirm:%s " % (PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM))

def strategy_ma(symbol, trim):
    strategy_dict = {
        "time_period": PERIOD_MA_TIME,
        "fast_period": PERIOD_MA_FAST,
        "mid_period": PERIOD_MA_MID,
        "slow_period": PERIOD_MA_SLOW,
        "confirm_period": PERIOD_CONFIRM,
        "trim_count": trim,

    }
    print("%s time_period %s, trim_count %s" % (symbol, str(strategy_dict["time_period"]), str(strategy_dict["trim_count"])))
    return strategy_dict

def current_time():
    current_time = datetime.datetime.now()
    print("Date Time:%s  " % (current_time))

# main
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

    init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM)
    strategy_list = []
    trim = 0

    for item in symbols:
        strategy_list.append(Strategy(item, PERIOD_CONFIRM))

    while True:

        current_time()
        poloniexAPI.net_margin()
        print('--------------')
        # one or more strategies below

        for strategy in strategy_list:
            #strategy_dict = strategy_ma(symbol, trim)
            #trim = strategy.crossover_strategy(strategy_dict)

            #WorkDetails(link, myLists)
            trim = strategy.crossover_strategy(time_period=PERIOD_MA_TIME,fast_period=PERIOD_MA_FAST, mid_period=PERIOD_MA_MID,slow_period=PERIOD_MA_SLOW, confirm_period=PERIOD_CONFIRM, trim_count=trim)
            poloniexAPI.trim_position(trim, symbols)

        #test_info(SYMBOL)
        print('--------------')

        time.sleep(5)
