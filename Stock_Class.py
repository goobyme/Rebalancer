import logging
from pandas import Series
from alpha_vantage import timeseries


class Security:

    def __init__(self, ticker=str(), amount=float(), basis=float()):
        self.ticker = ticker
        self.amount = amount
        self.basis_amount = basis
        self.quote = float()
        self.position = float()
        self.alloc = float()
        self.net_growth = float()
        self.target_alloc = float()
        self.deviation_from_target = float()

        self.stockdata = {}
        self.metadata = {}

    def update(self, api=True):
        if api:
            ts = timeseries.TimeSeries(key='BJH24BB02HP22I6I')
            data, metadata = ts.get_intraday(self.ticker)
            self.stockdata = data
            self.metadata = metadata
            self.quote = float(list(self.stockdata.values())[len(list(self.stockdata.values())) - 1]['4. close'])

        self.position = self.quote * self.amount
        if self.basis_amount == 0:
            self.basis_amount = self.position
        self.net_growth = (self.position-self.basis_amount)/self.basis_amount

    def buy(self, amount=int(), price=int()):
        self.amount += amount
        if price > 0:
            self.basis_amount += price*amount
            self.update()
        else:
            self.update()
            self.basis_amount += self.quote*amount
            self.update(api=False)

    def sell(self, amount=int(), price=int()):
        # Currently using basic weighted avg. assigning, can switch to indv. matching in time
        if price > 0:
            self.amount -= amount
            self.basis_amount -= (price*amount/self.position) * self.basis_amount
            self.update()
        else:
            self.update()
            self.amount -= amount
            self.basis_amount -= (self.quote*amount/self.position) * self.basis_amount
            self.update(api=False)

    def assign_real_alloc(self, port_total):
        self.alloc = self.position/port_total

    def gen_data_export(self, ex_type='j'):
        j = {'ticker': self.ticker, 'amount': self.amount, 'basis_amount': self.basis_amount,
             'quote': self.quote, 'position': self.position, 'alloc': self.alloc, 'net_growth': self.net_growth,
             'target_alloc': self.target_alloc, 'alloc_deviation': self.deviation_from_target}
        if ex_type == 'j':
            return j
        elif ex_type == 'p':
            p = Series(list(j.values()), index=j.keys(), name=self.ticker)
            return p
        else:
            logging.error('[Error] Improper export type chosen (choose between "p"andas or "j"son)')

    def change_target_alloc(self, percentage):
        pass

