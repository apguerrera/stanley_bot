import talib
import pandas as pd
import numpy as np
import datetime


def join_string(*args):
    finalStr = ''
    for item in args:
        finalStr += str(item) + ';'
    return finalStr + '\n'


def strategy(lot=1, path='/Users/dvoryashin/PycharmProjects/Crypto/backtesting/BTC_ETH-2016_6_6-2018_1_1.csv'):
    """
    Main function that modelling strategy on historical data
    :param lot: volume of trades
    :param path: path to quotes. Change it please!
    :return: returns nothing. Creates csv Reports in the same folder
    """

    # get quotes
    quotes = pd.read_csv(path, sep=';', names=['close', 'date', 'high', 'low', 'open'], skiprows=1)

    # calculate simple moving average by close prices
    np_real_data = np.array(quotes['close'].values, dtype=float)
    sma = talib.SMA(np_real_data, 10)

    # convert timestamp to datetime from quotes df, to new df
    dates = []
    for elem in quotes['date']:
        dates.append(datetime.datetime.fromtimestamp(elem))

    report = open('totalReport.csv', 'w+')
    report.write('Symbol;OrderType;Lot;DateOpen;PriceOpen;DateClose;PriceClose;Profit\n')
    index = 0
    is_buy_open = False
    is_sell_open = False
    date_open = None
    price_open = 0

    # start cycle by dates that modelling time flow
    for item in dates:
        if index < 1:
            index += 1
            continue

        # Open Sell rules
        last_close = float(quotes['close'][index - 1])
        if is_buy_open and last_close < sma[index - 1]:
            # Close Buy
            if is_buy_open:
                is_buy_open = False
                profit = (float(quotes['open'][index]) - price_open) * lot
                profit = profit - (profit*0.2)  # commission
                rec = join_string('BTC_ETH', 'buy', lot, date_open, price_open, item, quotes['open'][index], profit)
                report.write(rec)
            # Open sell
            is_sell_open = True
            date_open = item
            price_open = float(quotes['open'][index])

        # Open Buy rules
        last_close = float(quotes['close'][index-1])
        if is_buy_open is False and last_close > sma[index-1]:
            # close sell
            if is_sell_open:
                is_sell_open = False
                profit = price_open - float(quotes['open'][index])
                profit = profit - (profit * 0.2)  # commission
                rec = join_string('BTC_ETH', 'sell', lot, date_open, price_open, item, quotes['open'][index], profit)
                report.write(rec)
            # open buy
            is_buy_open = True
            date_open = item
            price_open = float(quotes['open'][index])

        index += 1

    report.close()

open('totalReport.csv', 'w+').close()
strategy()
