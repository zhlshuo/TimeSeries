from Backtester import BackTester
from Strategy import MACD
import datetime as dt
import time
from RiskManagement.VaR import VarCovarVaR
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':

    start = time.time()
    
    start_date = dt.date(2005, 1, 3)
    #end_date   = dt.date(2016, 10, 19)
    end_date   = dt.date(2016, 11, 1)
    
    macd = MACD(start_date = start_date)
    
    backtester = BackTester(macd, start_date, end_date)
    backtester.back_test()
    backtester.plot()

    VaR = VarCovarVaR(backtester.portfolio.assets)
    print(backtester.portfolio.price())
    VaR.calculate()
    VaR.print_text()
    
    dts = backtester.dt_range
    rets = np.diff(np.log(backtester.PNLs))
    yearly_ret = np.mean(rets) * 252
    yearly_vol = np.var(rets)**0.5 * np.power(252, .5)
    
    sharp_ratio = yearly_ret / yearly_vol
    
    print('sharp ratio:',sharp_ratio)
    print('yearly return:',yearly_ret)
    print('yearly vol:',yearly_vol)
    
    plt.plot(dts,rets)
    plt.ylabel('Return')
    plt.title('Return')
    
    macds   = backtester.strategy.MACDs
    signals = backtester.strategy.signal_line
    for ticker, macd in macds.items():
        macd = pd.Series(macd[-88:])
        signal = pd.Series(signals[ticker][-88:])
        diff = macd - signal
        auto_correlation = [diff.autocorr(i) for i in range(1,21)]
        plt.figure()
        plt.bar([i for i in range(1,21)], auto_correlation, align='center', alpha=0.5)
        plt.xticks([i for i in range(1,21)], [i for i in range(1,21)])
        plt.ylabel('Autocorrelation')
        plt.title(ticker + ': Autocorrelation of difference between MACD and Signal line')
    
    end = time.time()
    print('time used:', end - start)    
    print('Done')