from Backtester import BackTester
from Strategy import MACD
import datetime as dt
import time
from RiskManagement.VaR import VarCovarVaR

if __name__ == '__main__':

    start = time.time()
    
    start_date = dt.date(2005, 1, 3)
    end_date   = dt.date(2015, 1, 1)
    
    macd = MACD(start_date = start_date)
    
    backtester = BackTester(macd, start_date, end_date)
    backtester.back_test()
    backtester.plot()

    VaR = VarCovarVaR(backtester.portfolio.assets)
    VaR.calculate()
    VaR.print_text()

    end = time.time()
    print('time used:', end - start)    
    print('Done')