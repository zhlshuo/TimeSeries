from QuotesReader import QuotesReader as QR
import numpy as np

class VarCovarVaR:
    
    notional         = None
    portfolio        = None
    time_window      = None
    VaR_95           = None
    VaR_99           = None
        
    def __init__(self, portfolio, time_window=252):
        self.notional         = 0
        self.portfolio        = portfolio
        self.time_window      = time_window
        
    def portfolio_std_dev(self):
        returns = []
        weights = []
        
        for asset, quantity in self.portfolio.items():
            prices = QR.getQuotes(asset.ticker, self.time_window)
            returns.append([np.log(prices[i+1]/prices[i]) for i in range(len(prices)-1)])
            weights.append(QR.getQuote(asset.ticker) * quantity)
            self.notional += QR.getQuote(asset.ticker) * quantity
            
        cov = np.cov(returns)
        weights = np.array(weights)
        weights = weights/np.sum(weights)
        
        return np.sqrt(weights.dot(cov).dot(weights.T))
        
    def calculate(self):
        std_dev = self.portfolio_std_dev()
        
        self.VaR_95  = self.notional * std_dev * (-1.96)
        self.VaR_99  = self.notional * std_dev * (-2.576)
    
    def print_text(self):
        print('Value at risk with 95% confidence:', self.VaR_95)
        print('Value at risk with 99% confidence:', self.VaR_99)