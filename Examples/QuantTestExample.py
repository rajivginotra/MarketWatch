# region imports
from AlgorithmImports import *
# endregion

class HipsterRedKoala(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2022, 5,12)
        
        self.SetAccountCurrency("INR")
        self.SetCash(100000)  # Set Strategy Cash

        
        tcs = self.AddEquity("TCS", Resolution.Daily, Market.India)
        self.tcs = tcs.Symbol
        self.SetBenchmark("TCS")
        self.SetBrokerageModel(BrokerageName.Zerodha, AccountType.Margin)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time

                
    def OnData(self, data: Slice):
        if not self.tcs in data:
            return
        #current_price = data.Bars[self.tcs].Close
        price = data[self.tcs].Close
        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.tcs, 1)
                self.Log("Buy TCS @ " + str(price))
                self.entryPrice = price
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.1 > price:
            self.Liquidate(self.tcs)
            self.Log("Sell TCS @" + str(price))
            self.nextEntryTime = self.Time + self.period
