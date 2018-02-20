from alpha_vantage import timeseries
import logging
from pandas import DataFrame


class Security:

    def __init__(self, ticker, amount, basis):
        self.ticker = ticker
        self.amount = amount
        self.basis_amount = basis
        self.price = float()
        self.position = float()
        self.alloc = float()
        self.net_growth = float()

        self.stockdata = {}
        self.metadata = {}

    def update(self):
        ts = timeseries.TimeSeries(key='BJH24BB02HP22I6I')
        data, metadata = ts.get_intraday(self.ticker)
        self.stockdata = data
        self.metadata = metadata

        self.price = list(self.stockdata.values())[len(list(self.stockdata.values())) - 1]['4. close']
        self.position = self.price * self.amount
        self.net_growth = (self.position-self.basis_amount)/self.basis_amount

    def buy(self, amount=int(), price=int()):
        self.amount += amount
        self.basis_amount += price*amount
        self.update()

    def sell(self, amount=int(), price=int()):
        self.amount -= amount
        # Currently using basic weighted avg. assigning, can switch to indv. matching in time
        self.basis_amount -= (price*amount/self.position) * self.basis_amount
        self.update()

    def assign_real_alloc(self, port_total):
        self.alloc = self.position/port_total

    def gen_data_export(self, ex_type='j'):
        # TODO write data exporter in Stock Class
        if ex_type == 'j':
            j = {'ticker': self.ticker,



            }
            return j

        elif ex_type == 'p':
            p = DataFrame()
            return p
        else:
            logging.error('[Error] Improper export type chosen (choose between p or j)')

    def change_target_alloc(self, percentage):
        pass

