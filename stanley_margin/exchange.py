import poloniexAPI
import time
from ExchangeStrategy import ExchangeStrategy
import datetime
import argparse

# region ### GLOBALS

symbol_parm = { "BTC_ZRX": 2
            , "BTC_STEEM": 1
            , "BTC_SC": 1
            , "BTC_STRAT": 2
            , "BTC_REP": 2
            , "BTC_ZEC": 2
            , "BTC_GNO": 1
            , "BTC_GNT": 2

        }
# endregion
symbols = []
for key in symbol_parm:
    symbols.append(key)

print(symbols)

def current_time():
    current_time = datetime.datetime.now()
    print("Date Time:%s  " % (current_time))

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--trim',  default=0, type=int)
    parser.add_argument('--kill',  default='null', type=str)

    args = parser.parse_args()

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

    strategy_list = []

    for item in symbols:
        strategy_list.append(ExchangeStrategy(item, PERIOD_CONFIRM))

    while True:
        current_time()
        time.sleep(0.2)
        try:
            poloniexAPI.net_margin()
            print('--------------')

            # one or more strategies below
            for strategy in strategy_list:
                #strategy_dict = strategy_ma(symbol, trim)
                #trim = strategy.crossover_strategy(strategy_dict)
                symbol = strategy.get_symbol()
                #WorkDetails(link, myLists)
                trim = strategy.hodl_strategy(
                    slow_period=symbol_parm[symbol][0]
                    , mid_period=symbol_parm[symbol][1]
                    , fast_period=symbol_parm[symbol][2]
                    , time_period=symbol_parm[symbol][3]
                    , confirm_period=PERIOD_CONFIRM
                    , trim_count=trim)
                #poloniexAPI.trim_position(trim, symbols)
                #poloniexAPI.api_test()

        except:
            print('Kill on exit main')

        print('--------------')
        time.sleep(1)
