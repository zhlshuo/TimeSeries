import matplotlib.pyplot as plt
import datetime
from HolidayCalendar import date_range
import Global
from Pricable import Portfolio
from QuotesReader import QuotesReader as QR

class BackTester:
    
    # Daily Mark to Market PNL
    PNLs = [1000000]

    instructions = []
    portfolios   = []
    dt_range     = []
    
    strategy = None

    start_date = None
    end_date   = None
        
    def __init__(self, strategy, start_date=datetime.date(2005,1,1), end_date=datetime.date(2015,1,1)):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        QR.init()
        
    def back_test(self):
        portfolio     = Portfolio()
        self.dt_range = date_range(self.start_date, self.end_date)
        
        for dt in self.dt_range:
            Global.Market_Date = dt
            
            instruction = self.strategy.instruction()
            self.instructions.append(instruction)
            
            cost = portfolio.exectute(instruction)
            self.portfolios.append(portfolio)
    
            old_pnl = self.PNLs[-1]
            new_pnl = old_pnl - cost + portfolio.price()
            self.PNLs.append(new_pnl)
    
    def plot(self):
        plt.plot(self.dt_range, self.PNLs[1:])
        plt.ylabel('PNL')
        plt.title('Strategy Back-Testing')
        plt.show()