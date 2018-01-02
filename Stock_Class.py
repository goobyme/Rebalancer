from alpha_vantage import timeseries


class Security:

    def __init__(self, ticker, amount):
        self.ticker = ticker
        self.sharecount = amount
        self.stockdata = {}
        self.metadata = {}
        self.update()

    def update(self):
        ts = timeseries.TimeSeries(key='BJH24BB02HP22I6I')
        data, metadata = ts.get_intraday(self.ticker)
        self.stockdata = data
        self.metadata = metadata

    def buy(self, amount):
        self.sharecount += amount
        self.update()

    def sell(self, amount):
        self.sharecount -= amount
        self.update()

    def changealloc(self, percentage):
        pass


google = Security('MSFT', 100)
print(google.stockdata)
