import sys
import yfinance as yf
import time

class Trading:
    def __init__(self,money,ticker,position):
        self.money = money
        self.ticker = ticker
        self.position = position

    def get_data(self):
        df = yf.download(self.ticker,period='5y',interval='1d')
        return df['Adj Close']
    
    def real_data(self):
        while True:
            df = yf.download(self.ticker,period='1d',interval='1m')
            #time.sleep(5)
            print(df['Adj Close'][-1])

#python3 trading.py

print(Trading(1000,'ETH-USD','long').real_data())