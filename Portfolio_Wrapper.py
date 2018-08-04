from Portfolio_Core import Portfolio
from DB_Connect import MySqlConnection


class CronScript:

    def __init__(self, host):
        self.host = host
        self.connection = MySqlConnection(host)

    def save_portfolio(self, portfolio_obj):
        self.connection.portfolio_update(portfolio_obj.name, portfolio_obj.gen_portfolio_data(exp_type='p'))

        pass

    def load_portfolio(self, portfolio_name):
        raw_portfolio = self.connection.portfolio_query(portfolio_name)
        load_port = Portfolio(portfolio_name, '123', raw_portfolio)

        return load_port

    def run_updates(self):

        pass


