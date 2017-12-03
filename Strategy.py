from QuotesReader import QuotesReader as QR
import numpy as np

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
    
    long_term_window  = 26
    short_term_window = 12
    
    def instruction(self):
        lt_mv = np.mean(QR.getQuotes('GOOG', self.long_term_window))
        st_mv = np.mean(QR.getQuotes('GOOG', self.short_term_window))
        #diff  =st_mv - lt_mv
        
        if st_mv > lt_mv:
            return ('Stock', 'GOOG', 100, None)
        else:
            return ('Stock', 'GOOG', -100, None)