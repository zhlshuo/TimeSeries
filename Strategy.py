from QuotesReader import QuotesReader as QR
import numpy as np
import datetime
import Global
from HolidayCalendar import date_range

class Strategy:
    
    def instruction(self):
        '''
        This function return trading ninstructions formated as a tuple 
        (InstrumentType, Ticker, Quantity, Economics), below are examples for stock and options
        ('Stock', 'GOOG', 100, None) - long 100 GOOG stock
        ('Stock Option', 'GOOG', -100, (500, 60)) - short 100 options of GOOG with Strike 500 and 60 days to expiration
        '''
        raise ValueError('instruction() interface need inplemented for strategy')
        
class MACD(Strategy):
    
    ticker            = None
    long_term_window  = None
    short_term_window = None
    macd_window       = None
    stEMAs            = None
    ltEMAs            = None
    MACDs             = None
    signal_line       = None
    
    def __init__(self, ticker='GOOG', long_term_window=26, short_term_window=12, macd_window=9, start_date=None):
        QR.init()
        
        if start_date is None:
            start_date = Global.Market_Date
        
        self.ticker            = ticker
        self.long_term_window  = long_term_window
        self.short_term_window = short_term_window
        self.macd_window       = macd_window
        self.stEMAs            = [np.mean(QR.getQuotesAsOf(ticker, start_date, self.short_term_window))]
        self.ltEMAs            = [np.mean(QR.getQuotesAsOf(ticker, start_date, self.long_term_window))]
        self.MACDs             = [self.stEMAs[-1] - self.ltEMAs[-1]]
        self.signal_line       = [self.stEMAs[-1] - self.ltEMAs[-1]]
    
    def updateMACD(self):
        pre_stema = self.stEMAs[-1]
        pre_ltema = self.ltEMAs[-1]
        
        st_multiplier = 2./(self.short_term_window + 1)
        lt_multiplier = 2./(self.long_term_window + 1)
        
        close = QR.getQuote(self.ticker)
        
        st_emv = close * st_multiplier + pre_stema * (1 - st_multiplier)
        lt_emv = close * lt_multiplier + pre_ltema * (1 - lt_multiplier)
        macd   = st_emv - lt_emv
        
        self.stEMAs.append(st_emv)
        self.ltEMAs.append(lt_emv)
        self.MACDs.append(macd)
        
        backward_window = len(self.MACDs) if len(self.MACDs) < self.macd_window else self.macd_window
        self.signal_line.append(np.mean(self.MACDs[-backward_window:]))
        
    def instruction(self):
        
        self.updateMACD()
        
        if len(self.MACDs) <= self.macd_window:
            return None
        
        # if cross over, do transaction
        if self.MACDs[-1] > self.signal_line[-1] and self.MACDs[-2] < self.signal_line[-2]:
            return ('Stock', self.ticker, 100, None)
        elif self.MACDs[-1] < self.signal_line[-1] and self.MACDs[-2] > self.signal_line[-2]:
            return ('Stock', self.ticker, -100, None)
        else:
            return None