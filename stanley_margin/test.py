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

# region ### Methods
def calc_margin_alt(price, symbol):
    current_balance = poloniexAPI.returnTradableBalances()  # make it more flexible...
    print("My trade balance = %s at price %f" % (current_balance[symbol], price))

    relative_balance = current_balance / 8  # 50% of current balance
    #relative_balance = 0.1  # my balance = 0, FIX IT!
    amount = relative_balance
    return amount

if __name__ == "__main__":
    strategy_eth = Strategy('BTC_ETH')
    strategy_xrp = Strategy('BTC_XRP')

    while True:


        current_xrp = poloniexAPI.get_margin_balance('BTC_XRP')
        current_btc = poloniexAPI.get_margin_btc_balance('BTC_XRP')
        current_eth = poloniexAPI.get_margin_balance('BTC_ETH')
        current_total = current_eth + current_btc + current_xrp
        print("Balance:%f -- BTC = %f -- ETH = %f -- XRP = %f" % (current_total, current_btc, current_eth, current_xrp))

        symbol = 'BTC_XRP'
        coin =  symbol.replace("BTC_", "")

        last_price = poloniexAPI.get_orderbook(symbol)
        ask = float(last_price['asks'][0][0])*1.001
        bid = float(last_price['bids'][0][0])*0.999



        current_balance = poloniexAPI.polo.returnTradableBalances()  # make it more flexible...

        amount = float(current_balance[symbol][coin])*0.8
        #SYMBOL = 'BTC_ETH'
        print("Sell %s amount = %s at price %s" % (symbol, amount, bid ))
        res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=0.04)  # if you want margin trade
        print("Res %s at price %f" % (res, bid))
        # uncomment to make trades
        #res = poloniexAPI.polo.sell(symbol, bid, amount, orderType='immediateOrCancel')

        #res = poloniexAPI.polo.marginSell(symbol, bid, amount, lendingRate=2.4)  # if you want margin trade
        #print("Res %s at price %f" % (res, bid))


        #strategy_xrp.crossover_strategy(fast_period=PERIOD_MA_FAST, slow_period=PERIOD_MA_SLOW)


        test_info('BTC_ETH')
        test_info('BTC_XRP')
        print('--------------')

        time.sleep(5)
