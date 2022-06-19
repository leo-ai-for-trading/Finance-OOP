import yfinance as yf
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


class Trading:
    def __init__(self,money):
        self.money = money   #int(input("Insert the amount of money you want to invest: "))
        self.ticker = "ETH-USD"   #str(input("Insert the ticker: "))
        #self.position = str(input("Insert Long or Short: "))
    
    def get_data(self):
        data = pd.DataFrame(data=yf.download(self.ticker,period='max',interval='1d'))
        #data = data.reset_index()       
        return data

    def IBS(self):
        data = self.get_data()
        data['IBS'] = (data['Close']-data['Low'])/(data['High']-data['Low'])
        #building trading strategy
        #if IBS < 0.2 buy elif IBS > 0.8 sell
        data['entry'] = np.where( data.IBS < 0.2,data['Close'],data['Open'])
        data['exit'] = np.where(data.IBS > 0.8, data['Close'], data['Open'])
        data['position'] = np.where(data.IBS < 0.2, 1, 0)
        data['stock'] = (self.money/data['Close'])
        data['profit'] = np.where(data.exit != 0,(data['Close']-data['entry']),0)
        data['trade'] = (data.exit - data.entry) * data.stock
        data['gain'] = (data.position * data.trade)
        data['equity'] = data.gain.cumsum()
        data['gain'] = np.where(data.gain != 0, data.gain,np.nan)
    
        plt.figure(figsize=(8,4),dpi=100)
        plt.plot(data.equity, color='green',linewidth=1.0)
        plt.xlabel("Period")
        plt.ylabel("Profit-Loss")
        plt.title("Strategy Performance")
        plt.legend()
        plt.show()

        
        return plt.show()

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
            df = df.append(dummy.iloc[-1]).dropna() 
            #return df



#python3 trading.py
Trading(money=10000).IBS()

