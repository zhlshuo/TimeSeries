from QuotesReader import QuotesReader as QR

class TransactionCost():
    
    execution_fee = None
    market_impact = None
    
    @staticmethod
    def init():
        # execution fee might be decided by volume, basis point... for simplicity, we assume it is by deal, so it is a constant
        if TransactionCost.execution_fee is None or TransactionCost.market_impact is None:
            TransactionCost.execution_fee = 100
            TransactionCost.market_impact = 10000
        
    @staticmethod
    def calculate(ticker, volume):
        return volume/QR.getVolume(ticker) * TransactionCost.market_impact + TransactionCost.execution_fee