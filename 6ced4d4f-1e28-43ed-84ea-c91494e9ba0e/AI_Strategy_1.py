from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"] # Example ticker, can be changed or expanded

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day" # Daily data; can be adjusted as needed

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate MACD and Signal line values
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            if macd_data is None:
                log(f"No MACD data for {ticker}")
                continue

            # Assuming `macd_data` contains MACD line under 'MACD' and signal line under 'signal'
            macd_line = macd_data['MACD']
            signal_line = macd_data['signal']
            
            # Check for recent crossover; threshold can be adjusted or decision logic changed
            if len(macd_line) > 0 and len(signal_line) > 0:
                if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                    log(f"MACD line crossed above Signal line for {ticker}")
                    allocation_dict[ticker] = 1.0 / len(self.tickers) # Full allocation divided among tickers
                else:
                    log(f"No MACD cross above Signal for {ticker} or MACD is below Signal")
                    allocation_dict[ticker] = 0  # Zero allocation if no crossover or MACD is below Signal
            else:
                log(f"Insufficient MACD or Signal data for {ticker}")
        return TargetAllocation(allocation_dict)