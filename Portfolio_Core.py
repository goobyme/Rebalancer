import datetime
import time
import logging

import pandas

from Stock_Class import Security
from Mail_Machine import MailMachine
import Data_Reader


class Portfolio:

    def __init__(self, name, email, file_path):
        """Initializes data and runs setup method which creates stock objects to populate portfolio obj"""
        """"Meta Data Attributes"""
        self.name = name
        self.email = email
        self.time_last_update = str()

        """"Stock Data Attributes (much of data is within SC objects within stock_list)"""
        self.stock_list = [Security()]
        self.total_position = float()
        self.portfolio_basis = float()
        self.net_gainloss = float()
        self.positions_table = pandas.DataFrame()

        self.set_up(Data_Reader.FileReader(file_path))

    """Methods for attribute set-up and creation/updating"""
    def set_up(self, raw_data):
        """Instantiates set of stocks from json output from Data_Reader.FileReader"""
        self.stock_list = [Security(stock_proto['Name'], stock_proto['Amount'], stock_proto['Basis'])
                           for stock_proto in raw_data]
        self.update_portfolio_data()

    def update_portfolio_data(self, api=True):
        """Updates entire portfolio data. First iterates updates for stock objects then creates portfolio attributes
        API parameter used to determine if update is for stock info, or just for portfolio data (no API ping)"""
        if api:
            for stock in self.stock_list:
                stock.update(api=True)
        self.total_position = sum(stock.position for stock in self.stock_list)
        self.portfolio_basis = sum(stock.basis_amount for stock in self.stock_list)
        for stock in self.stock_list:
            stock.assign_real_alloc(self.total_position)

        self.gen_portfolio_data()
        self.time_last_update = datetime.datetime.fromtimestamp(time.time()).isoformat()

    def gen_portfolio_data(self, exp_type=''):
        """Generates pandas table to summarize portfolio data. Also capable of exporting data as DataFrame or Json"""
        display_list = [stock.gen_data_export('p') for stock in self.stock_list]
        self.positions_table = pandas.concat(display_list, axis=1).T
        if exp_type == 'p':
            return self.positions_table
        elif exp_type == 'j':
            json_positions = [stock.gen_data_export('j') for stock in self.stock_list]
            return json_positions
        elif exp_type:
            logging.error('[Error] Need to input proper export type argument "p"andas or "j"son or blank for no export')

    def set_target_alloc(self, input_method='i'):
        if input_method == 'i':
            for stock in self.stock_list:
                stock.assign_target_alloc(input(
                    '{} has current allocation of {} with a position of {} and net gain of {}. Set Target Alloc:'
                    .format(stock.ticker, stock.alloc, stock.position, stock.net_growth)), self.total_position)
        elif input_method == 'f':
            # TODO build data reader method for reading target alloc from file
            Data_Reader
        else:
            logging.error('[Error] Need to input proper input method argument "i"nput or "f"ile')

    """Methods for portfolio manipulation (ie buys, sell, add, remove and rebalance)"""
    def init_transaction(self, ticker, amount, trans_type, price=0):
        for number, stock in enumerate(self.stock_list):
            if ticker == stock.ticker:
                s = stock
                break
            elif number == len(self.stock_list) - 1:
                logging.debug('[Warning] Ticker not found')
                return None
            else:
                continue
        if trans_type == 'b':
            s.buy(amount, price)
            self.update_portfolio_data(api=False)
        elif trans_type == 's':
            s.sell(amount, price)
            self.update_portfolio_data(api=False)
        else:
            logging.error('[Error] Need to input proper transaction type argument "b"uy or "s"ell)')

    def add_new_stock(self, ticker, amount, basis=0):
        stock = Security(ticker, amount, basis)
        stock.update()
        self.stock_list.append(stock)
        self.update_portfolio_data(api=False)

    def remove_stock(self, ticker):
        for stock in self.stock_list:
            if stock.ticker == ticker:
                self.stock_list.remove(stock)
                self.update_portfolio_data(api=False)
                break
            else:
                continue

    def rebalancer(self, threshold=0.1):
        dev_above = [stock.deviation_portfolio for stock in self.stock_list if stock.deviation_portfolio > 0]
        dev_below = [stock.deviation_portfolio for stock in self.stock_list if stock.deviation_portfolio < 0]
        assert sum(dev_above) == sum(dev_below)

        reports = list()
        if sum(dev_above) > threshold:
            for stock in self.stock_list:
                position_change = stock.deviation_stock*stock.position
                ammount_change = position_change/stock.quote
                if position_change > 0:
                    transaction = 'SELL'
                elif position_change < 0:
                    transaction = 'BUY'
                else:
                    transaction = 'PASS'
                reports.append({
                    'ticker': stock.ticker,
                    'position': stock.position,
                    'quote': stock.quote,
                    'real_alloc': stock.alloc,
                    'target_alloc': stock.target_alloc,
                    'deviation_port': stock.deviation_portfolio,
                    'deviation_pos': stock.deviation_stock,
                    'transaction': transaction,
                    'position_change': position_change,
                    'amount_change': ammount_change
                })

            return self.mail(reports)
        else:
            return None

    """Methods for exporting data"""
    def mail(self, raw_message):
        mm = MailMachine(raw_message, self.email)
        return mm.send()

    def create_report(self):
        self.positions_table.to_csv('{}_portfolio {}.csv'.format(self.name, self.time_last_update))


# TODO Build outer code structure. Program needs to open itself every week and send email if needed then sleep again
# TODO Build inherited classes for alternate ideal allocations, or some other means of introducing differing alloc
