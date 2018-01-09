import poloniexAPI
import time
from Strategy import Strategy
import datetime

# region ### GLOBALS
PERIOD_MA_SLOW = 120
PERIOD_MA_MID = 40
PERIOD_MA_FAST = 20
PERIOD_MA_TIME = 15
SYMBOL = 'BTC_ETH'
# endregion



if __name__ == "__main__":



    while True:

        current_time = datetime.datetime.now()
        print("Date Time:%s  " % (current_time))
        current_btc = str(poloniexAPI.get_chart_data('BTC_XRP', 5, 15))
        print("Count BTC:%s  " % (current_btc))


        #test_info(SYMBOL)
        #test_info('BTC_ETH')
        #test_info('BTC_XRP')
        print('--------------')

        time.sleep(5)
