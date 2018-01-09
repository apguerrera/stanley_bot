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
def init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM):
    print("MA Period:%f  MA Slow:%f  MA Mid:%f  MA Fast:%f  Confirm:%s " % (PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM))

def current_time():
    current_time = datetime.datetime.now()
    print("Date Time:%s  " % (current_time))

def net_margin():
    net_margin = poloniexAPI.get_net_margin()
    print("Total Margin Balance: %s  " % (net_margin))

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

    #init_strategy(PERIOD_MA_TIME, PERIOD_MA_SLOW, PERIOD_MA_MID, PERIOD_MA_FAST, PERIOD_CONFIRM)
    trim = 0

    while True:

        current_time()
        net_margin()
        #test_info(SYMBOL)

        print('--------------')
        time.sleep(5)
        
