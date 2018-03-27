import poloniexAPI
import time
from Strategy import Strategy
import datetime
import argparse

# region ### GLOBALS

MA_SLOW = 100   # 120
MA_MID = 30    # 30
MA_FAST = 10    # 15
MA_TIME = 120
CONFIRM_TIME = 3

#symbols = ['BTC_LTC', 'BTC_XRP', 'BTC_ETH','BTC_FCT','BTC_BTS','BTC_XMR','BTC_DASH','BTC_MAID','BTC_CLAM', 'BTC_STR' ]

symbol_parm = {
            "BTC_XRP": [110, 30, 10, 120] # 20171228
            #"BTC_XRP": [60, 30, 10, 30]
            , "BTC_LTC": [200, 50, 16, 120]
            , "BTC_ETH": [110, 35, 12, 120]
            , "BTC_FCT": [140, 50, 14, 120]
            , "BTC_STR": [250, 55, 20, 120]
            #, "BTC_STR": [120, 30, 15, 30]

            , "BTC_MAID": [120, 60, 15, 120]
            #, "BTC_XMR": [220, 100, 20, 120]
            , "BTC_XMR": [180, 60, 18, 120]

            , "BTC_BTS": [90, 30, 15, 120]
            #, "BTC_DASH": [MA_SLOW, MA_MID, MA_FAST, MA_TIME]
            , "BTC_CLAM": [140, 70, 18, 120]
            #, "BTC_DOGE": [MA_SLOW, MA_MID, MA_FAST, MA_TIME]
        }

# endregion
symbols = []
for key in symbol_parm:
    symbols.append(key)

print(symbol_parm)

def init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM):
    print("MA Period:%f  MA Slow:%f  MA Mid:%f  MA Fast:%f  Confirm:%s " % (PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM))

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
    parser.add_argument('--trim',  default=0, type=int)
    parser.add_argument('--kill',  default='null', type=str)


    args = parser.parse_args()

    PERIOD_MA_SLOW = args.slow
    PERIOD_MA_MID = args.mid
    PERIOD_MA_FAST = args.fast
    PERIOD_MA_TIME = args.time
    PERIOD_CONFIRM = args.confirm
    trim = args.trim
    kill_symbol = args.kill

    if any(kill_symbol in s for s in symbols):
        matching = [s for s in symbols if kill_symbol in s]
        for symbol in matching :
            print("Kill ticket close: %s" % (str(symbol)))
            res = poloniexAPI.polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
            print("Res %s" % (res))
    elif kill_symbol.lower() == "all":
        for symbol in symbols :
            print("Kill ticket close: %s" % (str(symbol)))
            res = poloniexAPI.polo.closeMarginPosition(currencyPair=symbol)  # close margin trade
            print("Res %s" % (res))
            time.sleep(10)

    init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM)
    strategy_list = []


    for item in symbols:
        strategy_list.append(Strategy(item, PERIOD_CONFIRM))

    while True:
        current_time()
        time.sleep(2)
        try:
            poloniexAPI.net_margin()
            print('--------------')
            time.sleep(10)
            # one or more strategies below
            for strategy in strategy_list:
                #strategy_dict = strategy_ma(symbol, trim)
                #trim = strategy.crossover_strategy(strategy_dict)
                symbol = strategy.get_symbol()
                #WorkDetails(link, myLists)
                trim = strategy.crossover_strategy(
                    slow_period=symbol_parm[symbol][0]
                    , mid_period=symbol_parm[symbol][1]
                    , fast_period=symbol_parm[symbol][2]
                    , time_period=symbol_parm[symbol][3]
                    , confirm_period=PERIOD_CONFIRM
                    , trim_count=trim)
                #poloniexAPI.trim_position(trim, symbols)
                #poloniexAPI.api_test()
                print('---')
                time.sleep(1)


        except:
            print('Kill on exit main')

        print('--------------')
