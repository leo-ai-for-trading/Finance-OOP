import sys
import yfinance as yf
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Trading:
    def __init__(self):
        self.money = int(input("Insert the amount of money you want to invest: "))
        #self.ticker = str(input("Insert the ticker: "))
        #self.position = str(input("Insert Long or Short: "))

    def get_data(self):
        df = yf.download(self.ticker,period='5y',interval='1d')
        return df['Adj Close']
    
    def real_data(self):
        while True:
            df = yf.download(self.ticker,period='1d',interval='1m')
            #time.sleep(5)
            print(f"actual price of {self.ticker} is:  {str(df['Adj Close'][-1])}")

    def pairs(self):
        first_ticker = (input("Insert the first ticker: "))
        second_ticker = (input("Insert the second ticker: "))
        tickers = [first_ticker.upper(), second_ticker.upper()]
        first = yf.download(first_ticker,period='7d',interval='1m')['Close']
        second = yf.download(second_ticker,period='7d',interval='1m')['Close']
        df = pd.DataFrame(data={tickers[0]:first,tickers[1]:second})
        df = df.dropna()
        df['ratio'] = df.iloc[:,0]/df.iloc[:,1]
        while True:    
            ff = yf.download(tickers[0],period='7d',interval='1m')['Close']
            ss = yf.download(tickers[1],period='7d',interval='1m')['Close']
            dummy = pd.DataFrame(data={tickers[0]:ff,tickers[1]:ss,'ratio':ff/ss})
            dummy = dummy.dropna()
            df = df.append(dummy.iloc[-1]).dropna() #,ignore_index=True)
            #df['ratio'] = df['ratio'].append([dummy.iloc[-1,0]/dummy.iloc[-1,1]]).dropna()
            #df['ratio'].append([ff[-1].item()/ss[-1].item()])
            print(df)
            time.sleep(5)
            #return df
            
    
    def continous_plot(self):
        df = self.pairs()
        #animate function
        plt.cla()
        #plt.plot(df.index,df.iloc[:,0],label=df.columns[0]+' price')
        plt.plot(df.index,df['ratio'],label='price ratio between: ' + df.columns[0] + ' and '+df.columns[1])

        plt.legend(loc='upper right')
        plt.tight_layout()
        ani = FuncAnimation(plt.gcf(), self.continous_plot, interval=1000*60)

        return ani,plt.tight_layout(),plt.show()
        

#python3 trading.py
print(Trading().pairs())
