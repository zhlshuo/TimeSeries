"""
Created on Sun Dec 24 09:00:27 2017

@author: lishuo
"""
import pandas as pd
import Global

class QuotesReader:
    
    quotes = None
    volumes = None
    trading_dates = None
    
    @staticmethod
    def init():
        if QuotesReader.quotes is None:
            raw_quotes = pd.read_csv('../stock_quotes.csv', header=0)
            QuotesReader.quotes = pd.pivot_table(raw_quotes, values='Close', index='Date', columns='Symbol')
            QuotesReader.quotes = QuotesReader.quotes.fillna(method='bfill')
            QuotesReader.trading_dates = QuotesReader.quotes.index.tolist()
            
            QuotesReader.volumes = pd.pivot_table(raw_quotes, values='Volume', index='Date', columns='Symbol')
            QuotesReader.volumes = QuotesReader.volumes.fillna(method='bfill')
    
    @staticmethod
    def getVolume(ticker):
        indexes = QuotesReader.volumes.index.tolist()
        try:
            loc     = indexes.index(Global.Market_Date.strftime('%Y-%m-%d'))
        except:
            print('Volume for ' + ticker + ' is missing on', Global.Market_Date)
            return 0
        
        return QuotesReader.volumes.iloc[loc][ticker]
    
    @staticmethod
    def getAllQuotesAsDF():
        return QuotesReader.quotes
    
    @staticmethod
    def getTickers():
        return QuotesReader.quotes.columns.tolist()
    
    @staticmethod
    def getQuoteTimeSeries(ticker):
        return QuotesReader.quotes[ticker]

    @staticmethod
    def getQuote(ticker):
        
        indexes = QuotesReader.quotes.index.tolist()
        try:
            loc     = indexes.index(Global.Market_Date.strftime('%Y-%m-%d'))
        except:
            print('Price for ' + ticker + ' is missing on', Global.Market_Date)
            return 0
        
        return QuotesReader.quotes.iloc[loc][ticker]
    
    @staticmethod
    def getQuotes(ticker, backward=1):
        indexes = QuotesReader.quotes.index.tolist()
        try:
            loc     = indexes.index(Global.Market_Date.strftime('%Y-%m-%d'))
        except:
            print('Price for ' + ticker + ' is missing on', Global.Market_Date)
            return [0]
        
        return QuotesReader.quotes.iloc[loc-backward:loc][ticker].tolist()
    
    @staticmethod
    def getQuotesAsOf(ticker, date, backward=1):
        indexes = QuotesReader.quotes.index.tolist()
        try:
            loc     = indexes.index(date.strftime('%Y-%m-%d'))
        except:
            print('Price for ' + ticker + ' is missing on', date)
            return [0]
        
        return QuotesReader.quotes.iloc[loc-backward:loc][ticker].tolist()
    
    @staticmethod
    def getQuotesByDateRange(ticker, start_date, end_date=None):
        indexes = QuotesReader.quotes.index.tolist()
        try:
            loc     = indexes.index(start_date.strftime('%Y-%m-%d'))
        except:
            print('Price for ' + ticker + ' is missing on', Global.Market_Date)
            return [0]
        
        if end_date is None:
            return QuotesReader.quotes.iloc[loc][ticker].tolist()
        
        days = (end_date - start_date).days
        return QuotesReader.quotes.iloc[loc:loc + days][ticker].tolist()
    
    
if __name__=='__main__':
    QuotesReader.init()
    import datetime as dt
    Global.Market_Date = dt.date(2017, 8, 1)
    df = QuotesReader().getAllQuotesAsDF()
    quotes = QuotesReader.getQuotes('GOOG', 60)