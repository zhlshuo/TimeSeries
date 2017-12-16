class StockPicker:
    
    def EligibleStockList(self):
        raise ValueError('Interface EligibleStockList need implemented')
        
class MACDStockPicker(StockPicker):
    
    def EligibleStockList(self):
        # need more sophisticated logic here!!!!
        return ['GOOG']