import datetime
import time

import openpyxl
import pandas

from Stock_Class import Security as SC
from Data_Reader import FileReader
from Mail_Machine import MailMachine


class Portfolio:

    def __init__(self, name, email, file_path):
        """Initializes data and runs setup method which creates stock objects to populate portfolio obj"""
        """"Meta Data Attributes"""
        self.name = name
        self.email = email
        self.time_last_update = str()

        """"Stock Data Attributes (much of data is within SC objects within stock_list)"""
        self.stock_list = list()
        self.total_position = float()

        self.set_up(FileReader(file_path))

    def set_up(self, raw_data):
        self.stock_list = [SC(stock_proto['Name'], stock_proto['Amount'], stock_proto['Basis'])
                           for stock_proto in raw_data]

        self.update_portfolio_data()

    def update_portfolio_data(self):
        for stock in self.stock_list:
            stock.update()
        self.total_position = sum(stock.position for stock in self.stock_list)
        for stock in self.stock_list:
            stock.assign_real_alloc(self.total_position)

        self.time_last_update = datetime.datetime.fromtimestamp(time.time()).isoformat()

    def rebalancer(self):

        pass

    def set_alloc(self):
        pass

    def display_alloc(self):

        for stock in self.stock_list:
            print('{}')

    def mail(self, raw_message):
        mm = MailMachine(raw_message, self.email)
        mm.mailman()

    def save_portfolio(self):
        pass

    def create_report(self):
        pass


# TODO Build outer code structure. Program needs to open itself every week and send email if needed then sleep again
# TODO Build inherited classes for alternate ideal allocations, or some other means of introducing differing alloc
