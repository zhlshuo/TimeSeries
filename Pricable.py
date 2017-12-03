from QuotesReader import QuotesReader as QR

class Portfolio:
    
    assets = {}
    
    def exectute(self, instruction):
        instrumentType, ticker, quantity, economics = instruction
        cost = 0
        
        if instrumentType == 'Stock':
            stock = Stock(ticker)
            self.assets[stock] = quantity if stock not in self.assets else quantity + self.assets.get(stock)
            cost = stock.price() * quantity
        elif instrumentType == 'StockOption':
            strike, timeToExp = economics
            stockOption = StockOption(ticker, strike, timeToExp)
            self.assets[stockOption] = quantity if stockOption not in self.assets else quantity + self.assets.get(stockOption)
            cost = stockOption.price() * quantity
        else:
            raise ValueError(instrumentType + ' is not supported now')
            
        return cost

    def price(self):
        total_price = 0
        for asset, quant in self.assets.items():
            total_price += asset.price() * quant
                                      
        return total_price
        
        
class Asset:
    
    def price(self):
        raise ValueError('interface price() need implemented!')
    
    def __eq__(self, other):
        raise ValueError('interface __eq__() need implemented!')
        
    def __hash__(self):
        raise ValueError('interface __eq__() need implemented!')
    
    
class Stock(Asset):
    
    ticker = None
    
    def __init__(self, ticker):
        self.ticker = ticker
    
    def price(self):
        return QR.getQuotes(self.ticker)[0]

    def __eq__(self, other):
        return self.ticker == other.ticker
    
    def __hash__(self):
        return hash(self.ticker)
        

def BlackShcoles(self, strike, timeToExp, riskFreeRate, volatility, spot):
    return 10
    
class StockOption(Asset):
    
    strike = None
    timeToExp = None
    underlying = None
    
    def __init__(self, underlying, strike, timeToExp):
        self.strike = strike
        self.timeToExp = timeToExp
        self.underlying = underlying
    
    def price(self):
        spot = QR.getQuotes(self.underlying)[0]
        return BlackShcoles(self.strike, self.timeToExp, 0.01, 0.01, spot)
    
    def __eq__(self, other):
        return (self.underlying, self.strike, self.timeToExp) == (other.underlying, other.strike, other.timeToExp)
    
    def __hash__(self):
        return hash((self.underlying, self.strike, self.timeToExp))