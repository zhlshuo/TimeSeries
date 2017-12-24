"""
Created on Sun Dec 24 09:00:27 2017

@author: lishuo
"""
from QuotesReader import QuotesReader as QR
import numpy as np
#import datetime
import Global
from StockPicker import MACDStockPicker

class Strategy:
    
    def instruction(self):
        '''
        This function return trading instructions formated as a list of tuples 
        [(InstrumentType, Ticker, Quantity, Economics)], below are examples for stock and options
        [('Stock', 'GOOG', 100, None)] - long 100 GOOG stock
        [('Stock Option', 'GOOG', -100, (500, 60))] - short 100 options of GOOG with Strike 500 and 60 days to expiration
        '''
        raise ValueError('instruction() interface need inplemented for strategy')
        
class MACD(Strategy):
    
    long_term_window  = None
    short_term_window = None
    macd_window       = None
    stEMAs            = None
    ltEMAs            = None
    MACDs             = None
    signal_line       = None
    eligibe_stocks    = None
    
    def __init__(self, start_date=None):
        QR.init()
        
        if start_date is None:
            start_date = Global.Market_Date
        
        self.eligibe_stocks    = MACDStockPicker().EligibleStockList()
        #self.eligibe_stocks    = [MACDStockPicker.stock]
        self.long_term_window  = {ticker:26 for ticker in self.eligibe_stocks}
        self.short_term_window = {ticker:12 for ticker in self.eligibe_stocks}
        self.macd_window       = {ticker:9 for ticker in self.eligibe_stocks}
        self.stEMAs            = {ticker:[np.mean(QR.getQuotesAsOf(ticker, start_date, self.short_term_window[ticker]))] for ticker in self.eligibe_stocks}
        self.ltEMAs            = {ticker:[np.mean(QR.getQuotesAsOf(ticker, start_date, self.long_term_window[ticker]))] for ticker in self.eligibe_stocks}
        self.MACDs             = {ticker:[self.stEMAs[ticker][-1] - self.ltEMAs[ticker][-1]] for ticker in self.eligibe_stocks}
        self.signal_line       = {ticker:[self.stEMAs[ticker][-1] - self.ltEMAs[ticker][-1]] for ticker in self.eligibe_stocks}
    
    def updateTimeWindow(self, ticker):
        # need more sophisticated logic here!!!!
        return (26, 12, 9)
    
    def updateMACD(self):
        for ticker in self.eligibe_stocks:
            self.long_term_window[ticker], self.short_term_window[ticker], self.macd_window[ticker] = self.updateTimeWindow(ticker)
            
            pre_stema = self.stEMAs[ticker][-1]
            pre_ltema = self.ltEMAs[ticker][-1]
            
            st_multiplier = 2./(self.short_term_window[ticker] + 1)
            lt_multiplier = 2./(self.long_term_window[ticker] + 1)
            
            close = QR.getQuote(ticker)
            
            st_emv = close * st_multiplier + pre_stema * (1 - st_multiplier)
            lt_emv = close * lt_multiplier + pre_ltema * (1 - lt_multiplier)
            macd   = st_emv - lt_emv
            
            self.stEMAs[ticker].append(st_emv)
            self.ltEMAs[ticker].append(lt_emv)
            self.MACDs[ticker].append(macd)
            
            backward_window = len(self.MACDs[ticker]) if len(self.MACDs[ticker]) < self.macd_window[ticker] else self.macd_window[ticker]
            self.signal_line[ticker].append(np.mean(self.MACDs[ticker][-backward_window:]))
        
    def instruction(self):
        
        self.updateMACD()
        
        instructions = []
        
        for ticker in self.eligibe_stocks:
            if len(self.MACDs[ticker]) <= self.macd_window[ticker]:
                continue
            
            # if cross over, do transaction
            if self.MACDs[ticker][-1] > self.signal_line[ticker][-1] and self.MACDs[ticker][-2] < self.signal_line[ticker][-2]:
                instructions.append(('Stock', ticker, 500, None))
            elif self.MACDs[ticker][-1] < self.signal_line[ticker][-1] and self.MACDs[ticker][-2] > self.signal_line[ticker][-2]:
                instructions.append(('Stock', ticker, -500, None))
        
        if len(instructions) == 0:
            return None
        
        return instructions