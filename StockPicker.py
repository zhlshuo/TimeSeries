from QuotesReader import QuotesReader as QR
import matplotlib.pyplot as plt
import numpy as np
import datetime
from HolidayCalendar import date_range
import Global
import time

class StockPicker:
    
    def EligibleStockList(self):
        raise ValueError('Interface EligibleStockList need implemented')
        
class MACDStockPicker(StockPicker):
    
    stock = None
    
    def EligibleStockList(self):
        # need more sophisticated logic here!!!!
        return [  'EGLE',
                 'AIG',
                 'GOOG',
                 'GOOGL',
                 'ISRG',
                 'CMG',
                 'ICPT',
                 'ANIP',
                 'AZO',
                 'ADS',
                 'ILMN',
                 'GEVO',
                 'HQCL',
                 'CWEI',
                 'BIOD',
                 'IBB',
                 'BAP',
                 'BIIB',
                 'GOLD',
                 'AGN',
                 'BIDU',
                 'ALXN',
                 'EPC',
                 'CPST',
                 'CP',
                 'IEP',
                 'IOC',
                 'GRBK',
                 'DDS'
                 ]
    
if __name__=='__main__':
    tickers = [  'EGLE',
                 'AIG',
                 'GOOG',
                 'GOOGL',
                 'ISRG',
                 'CMG',
                 'ICPT',
                 'ANIP',
                 'AZO',
                 'ADS',
                 'ILMN',
                 'GEVO',
                 'HQCL',
                 'CWEI',
                 'BIOD',
                 'IBB',
                 'BAP',
                 'BIIB',
                 'GOLD',
                 'AGN',
                 'BIDU',
                 'ALXN',
                 'EPC',
                 'CPST',
                 'CP',
                 'IEP',
                 'IOC',
                 'GRBK',
                 'DDS'
                 ]
    QR.init()
    dts = QR.trading_dates
    ticker_quote_pairs = []
    ticker_vol_pairs = []
    
    for ticker in tickers:
        quotes = QR.getQuoteTimeSeries(ticker)
        ticker_quote_pairs.append((ticker, quotes))
        rets = np.diff(np.log(quotes))
        ticker_vol_pairs.append((ticker, np.std(rets)))
    
    print('finish get quotes')
    '''for ticker, quotes in ticker_quote_pairs:
        plt.figure()
        plt.plot(dts[-len(quotes):], quotes)
        plt.ylabel('Quotes')
        plt.title(ticker)'''
        
    '''for ticker, quotes in ticker_quote_pairs:
        
        quotes = quotes[-88:]
        auto_correlation = [quotes.autocorr(i) for i in range(1,21)]
        plt.figure()
        plt.bar([i for i in range(1,21)], auto_correlation, align='center', alpha=0.5)
        plt.xticks([i for i in range(1,21)], [i for i in range(1,21)])
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation of ' + ticker)'''
    
    '''start = time.time()
    
    QR.init()
    tickers = QR.getTickers()
    tickers = ['GOOG']
    
    dts = QR.trading_dates
    start_date = datetime.date(2014,1,3)
    end_date = datetime.date(2015,1,1)
    
    long_term_window  = {ticker:26 for ticker in tickers}
    short_term_window = {ticker:12 for ticker in tickers}
    macd_window       = {ticker:9 for ticker in tickers}
    
    stEMAs      = {ticker:[np.mean(QR.getQuotesAsOf(ticker, start_date, short_term_window[ticker]))] for ticker in tickers}
    ltEMAs      = {ticker:[np.mean(QR.getQuotesAsOf(ticker, start_date, long_term_window[ticker]))] for ticker in tickers}
    MACDs       = {ticker:[stEMAs[ticker][-1] - ltEMAs[ticker][-1]] for ticker in tickers}
    signal_line = {ticker:[stEMAs[ticker][-1] - ltEMAs[ticker][-1]] for ticker in tickers}
    quotes      = {}
    
    dt_range = [dt for dt in date_range(start_date, end_date) if dt.strftime('%Y-%m-%d') in QR.trading_dates]
    
    for dt in dt_range:
        for ticker in tickers:
            Global.Market_Date = dt
            
            # quotes
            quotes[ticker] = QR.getQuoteTimeSeries(ticker)
            
            pre_stema = stEMAs[ticker][-1]
            pre_ltema = ltEMAs[ticker][-1]
            
            st_multiplier = 2./(short_term_window[ticker] + 1)
            lt_multiplier = 2./(long_term_window[ticker] + 1)
            
            close = QR.getQuote(ticker)
            
            st_emv = close * st_multiplier + pre_stema * (1 - st_multiplier)
            lt_emv = close * lt_multiplier + pre_ltema * (1 - lt_multiplier)
            macd   = st_emv - lt_emv
            
            stEMAs[ticker].append(st_emv)
            ltEMAs[ticker].append(lt_emv)
            MACDs[ticker].append(macd)
            
            backward_window = len(MACDs[ticker]) if len(MACDs[ticker]) < macd_window[ticker] else macd_window[ticker]
            signal_line[ticker].append(np.mean(MACDs[ticker][-backward_window:]))
        
    plt.figure()
    plt.plot(dts[-len(quotes['GOOG']):], quotes['GOOG'])
    plt.ylabel('Quotes')
    plt.title('Pattern Seeking')
            
    dt_len = len(stEMAs['GOOG']) if len(stEMAs['GOOG']) < len(ltEMAs['GOOG']) else len(ltEMAs['GOOG'])
    
    plt.figure()
    plt.plot(dts[-dt_len:], stEMAs['GOOG'], dts[-dt_len:], ltEMAs['GOOG'])
    plt.ylabel('EMA')
    plt.title('EMA')
    plt.legend(['$EMA_{st}$','$EMA_{lt}$'])
    
    dt_len = len(MACDs['GOOG']) if len(MACDs['GOOG']) < len(signal_line['GOOG']) else len(signal_line['GOOG'])
    
    plt.figure()
    plt.plot(dts[-dt_len:], MACDs['GOOG'], dts[-dt_len:], signal_line['GOOG'])
    plt.ylabel('MACD')
    plt.title('MACD and Signal Line')
    plt.legend(['MACD','Signal Line'])
    
    plt.show()
    
    end = time.time()
    print('time used:', end - start)    
    print('Done')'''