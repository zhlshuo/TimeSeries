import matplotlib.pyplot as plt
import datetime
from HolidayCalendar import date_range
import Global
from Pricable import Portfolio
from QuotesReader import QuotesReader as QR
from TransactionCost import TransactionCost as TC

class BackTester:
    
    debug_info = []
    
    # Daily Mark to Market PNL
    PNLs           = [1000000]
    cash_flows     = [1000000]
    portfolio_vals = [0]

    instructions = []
    dt_range     = []
    
    strategy = None

    start_date = None
    end_date   = None
        
    def __init__(self, strategy, start_date=datetime.date(2005,1,1), end_date=datetime.date(2015,1,1)):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        QR.init()
        TC.init()
        
    def back_test(self):
        portfolio     = Portfolio()
        # for simplicity, if quote is not available at that date, we assume it is not a trading date
        self.dt_range = [dt for dt in date_range(self.start_date, self.end_date) if dt.strftime('%Y-%m-%d') in QR.trading_dates]
        
        for dt in self.dt_range:
            
            Global.Market_Date = dt
            
            instruction = self.strategy.instruction()
            self.instructions.append(instruction)
            
            # calculatet the cash flows and portfolio value saperately, PNL will be the sum of these two
            if instruction is None:
                self.cash_flows.append(self.cash_flows[-1])
            else:
                cost = portfolio.exectute(instruction)
                self.cash_flows.append(self.cash_flows[-1] - cost)  
            
            self.portfolio_vals.append(portfolio.price())
            
            new_pnl = self.cash_flows[-1] + self.portfolio_vals[-1]
            
            self.PNLs.append(new_pnl)
            
            self.debug_info.append((dt, instruction, self.cash_flows[-1], self.portfolio_vals[-1], self.PNLs[-1]))
    
    def plot(self):
        plt.plot(self.dt_range, self.PNLs[1:])
        plt.ylabel('PNL')
        plt.title('Strategy Back-Testing')
        plt.show()