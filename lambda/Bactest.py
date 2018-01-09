


class Portfolio:
    """An abstract base class representing a portfolio of
    positions (including both instruments and cash), determined
    on the basis of a set of signals provided by a Strategy."""

    def __init__(self, symbol, confirm_period, fast_period, mid_period, slow_period):
        self.SYMBOL = symbol
        self.ticket = 0
        self.confirm = confirm_period
        self.initiate = 0
        self.trim = 0
        self.fast_period = fast_period
        self.mid_period = mid_period
        self.slow_period = slow_period
        self.position = "none"

    @abstractmethod
    def generate_positions(self):
        """Provides the logic to determine how the portfolio
        positions are allocated on the basis of forecasting
        signals and available cash."""
        try:
            if self.position == "buy":
                if self.trim > 0:
                    print("%s self trim %.0f " % (self.SYMBOL, self.trim))
                    poloniexAPI.exit_buy_margin(ask, self.SYMBOL)
                    self.trim = self.trim - 1
                    self.ticket = 0

                elif  fast_ma < mid_ma:
                    print("%s self fast_ma < mid_ma %.0f" % (self.SYMBOL, fast_ma < mid_ma ))
                    self.ticket = exit_margin(ask, self.SYMBOL, self.ticket, self.confirm )

                elif fast_ma > slow_ma:
                    print("%s self fast_ma > slow_ma %.0f" % (self.SYMBOL, fast_ma > slow_ma ))
                    if  ask < slow_ma:
                        print("%s self ask < slow_ma %.0f" % (self.SYMBOL, ask < slow_ma))
                        self.ticket = exit_margin(ask, self.SYMBOL, self.ticket, self.confirm )

                    elif  current_margin > 0.50:
                        if fast_ma > mid_ma:
                            if self.ticket < self.confirm:
                                self.ticket = self.ticket + 1
                            else:
                                self.position = "buy"
                                self.ticket = 0
                        else:
                            print("%s alt_converted %f greater than half current_margin %f" % (self.SYMBOL, alt_margin, net_margin))
                            self.ticket = 0
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0

            elif self.position == "buy":
                if self.trim > 0:
                    print("%s self trim %.0f " % (self.SYMBOL, self.trim))
                    self.position = "exit"
                    self.ticket = 0
                    self.trim = self.trim - 1
                elif fast_ma < mid_ma:
                    print("%s self fast_ma > mid_ma %.0f" % (self.SYMBOL,fast_ma > mid_ma ))
                    self.position = "exit"
                    self.ticket = 0
                elif fast_ma > slow_ma:
                    if bid > slow_ma:
                        print("%s self bid > slow_ma %.0f" % (self.SYMBOL, bid > slow_ma ))
                        self.position = "exit"
                        self.ticket = 0
                    elif fast_ma < mid_ma:
                        print("%s self fast_ma < mid_ma %.0f" % (self.SYMBOL, fast_ma < mid_ma ))
                        self.position = "sell"
                        self.ticket = 0
                    else:
                        print("%s alt_converted " % (self.SYMBOL))
                        self.ticket = 0
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0

            elif self.position == "sell":
                if self.trim > 0:
                    print("%s self trim %.0f " % (self.SYMBOL, self.trim))
                    self.position = "exit"
                    self.ticket = 0
                    self.trim = self.trim - 1
                elif fast_ma > mid_ma:
                    print("%s self fast_ma > mid_ma %.0f" % (self.SYMBOL,fast_ma > mid_ma ))
                    self.position = "exit"
                    self.ticket = 0
                elif fast_ma < slow_ma:
                    if bid > slow_ma:
                        print("%s self bid > slow_ma %.0f" % (self.SYMBOL, bid > slow_ma ))
                        self.position = "exit"
                        self.ticket = 0
                    elif fast_ma < mid_ma:
                        print("%s self fast_ma < mid_ma %.0f" % (self.SYMBOL, fast_ma < mid_ma ))
                        self.position = "sell"
                        self.ticket = 0
                    else:
                        print("%s alt_converted " % (self.SYMBOL))
                        self.ticket = 0
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0


            elif self.position == "none":
                self.confirm = confirm_period
                if  bid < slow_ma and fast_ma < slow_ma and fast_ma < mid_ma: # and slow_ma <= mid_ma:
                    if self.ticket < self.confirm:
                        self.ticket = self.ticket + 2
                    else:
                        self.position = "sell"
                        self.ticket = 0
                        print("%s is_sell_open new entry" % (self.SYMBOL ))

                elif  ask > slow_ma and fast_ma > slow_ma and fast_ma > mid_ma: # and slow_ma >= mid_ma:
                    if self.ticket < self.confirm:
                        self.ticket = self.ticket + 2
                    else:
                        self.position = "buy"
                        self.ticket = 0
                        print("%s is_buy_open new entry" % (self.SYMBOL ))
                else:
                    print("%s self ticket %.0f " % (self.SYMBOL, self.ticket))
                    self.ticket = 0

        except:
            self.ticket = 0
            print("%s error 0" % (self.SYMBOL))
            return self.trim

        return self.trim


    @abstractmethod
    def backtest_portfolio(self):
        """Provides the logic to generate the trading orders
        and subsequent equity curve (i.e. growth of total equity),
        as a sum of holdings and cash, and the bar-period returns
        associated with this curve based on the 'positions' DataFrame.

        Produces a portfolio object that can be examined by
        other classes/functions."""
        raise NotImplementedError("Should implement backtest_portfolio()!")
