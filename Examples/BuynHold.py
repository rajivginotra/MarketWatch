# region imports
from AlgorithmImports import *
# endregion

class HipsterYellowGreenSeahorse(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetEndDate(2022, 5,12)
        
        self.SetTimeZone("Asia/Calcutta")
        self.SetAccountCurrency("INR")
        self.SetCash(100000)  # Set Strategy Cash
        self.Portfolio.Cash

        self.sbin = self.AddEquity("SBIN", Resolution.Hour, Market.India).Symbol
        self.SetBenchmark("SBIN")
        self.SetBrokerageModel(BrokerageName.Zerodha, AccountType.Margin)
        
        self.entryTicket = None
        self.stopMarketTicket = None

        self.entryTime = datetime.min
        self.stopMarketOrderFillTime = datetime.min
        self.highestPrice = 0

    def OnData(self, data: Slice):
        if (self.Time - self.stopMarketOrderFillTime).days < 30:
            return
        
        price = self.Securities[self.sbin].Price

        if not self.Portfolio.Invested and not self.Transactions.GetOpenOrders(self.sbin):
            quantity = self.CalculateOrderQuantity(self.sbin, 0.9)
            self.entryTicket = self.LimitOrder(self.sbin, quantity, price, "Entry order")
            self.entryTime = self.Time
            self.Log("Enter into Limit order @" + str(price))

        # Move the limit price if not filled by more than 1 day
        if (self.Time - self.entryTime).days > 1 and self.entryTicket.Status != OrderStatus.Filled:
            self.entryTime = self.Time
            updateFields = UpdateOrderFields()
            updateFields.LimitPrice =  price
            self.entryTicket.Update(updateFields)
            self.Log("Limit order not filled, updating it with new price @" + str(price))

        #Move up the trailing stoploss
        if self.stopMarketTicket is not None and self.Portfolio.Invested:
            if price > self.highestPrice:
                self.highestPrice = price
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = price * 0.95
                self.stopMarketTicket.Update(updateFields)
                self.Log("Updated trailing stop loss @" + str(updateFields.StopPrice))

    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status != OrderStatus.Filled:
            return 
        
        # Send the stoploss if entry limit order is filled
        if self.entryTicket is not None and self.entryTicket.OrderId == orderEvent.OrderId:
            self.stopMarketTicket = self.StopMarketOrder(self.sbin, self.entryTicket.QuantityFilled, 
                                                    self.entryTicket.AverageFillPrice * 0.95)
            self.Log("Updating initial stop loss @" + str(self.entryTicket.AverageFillPrice * 0.95))

    
        #save fill time of stop loss order
        if self.stopMarketTicket is not None and self.stopMarketTicket.OrderId == orderEvent.OrderId:
            self.stopMarketOrderFillTime  = self.Time
            self.highestPrice = 0
