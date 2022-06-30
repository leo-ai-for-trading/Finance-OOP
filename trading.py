
import yfinance as yf
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import datetime 
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.stattools import adfuller



class Trading:
    def __init__(self):
        self.money = 1000 #int(input("Insert the amount of money you want to invest: "))
        self.ticker = 'eth-usd' #str(input("Insert the ticker: "))
        self.ticker = self.ticker.upper()
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
        data['daily_return'] = data.gain.pct_change()

        return data

    def Cutler_RSI(self):
        data = self.IBS()
        n = len(data['Close'])
        data['U_t'] = np.where((data['Close'].diff(1) > 0),data['Close'].diff(1),0) 
        data['D_t'] = -1*np.where((data['Close'].diff(1) < 0),data['Close'].diff(1),0)
        for i in range(n-1):
            data['RS_t'] = ((1/n)*(data['U_t'][i]+data['U_t'][i+1])) / ((1/n)*(data['D_t'][i]+data['D_t'][i+1]))
        data['cutler_rsi'] = np.where(sum(data['D_t']) == 0,100,(100-(100/1+data['RS_t'])))
        #long if rsi < 10; maintain position while rsi <= 40; long if IBS <= 0.5
        #data['strategy']
        
        return print(data)

    def arbitrage(self):
        x = 'GLD'
        y = 'SLV'
        X = yf.download(x,period='max')['Close']
        Y = yf.download(y,period='max')['Close']
        df = pd.DataFrame({x:X,y:Y},index=None)
        df = df.dropna()
        df['ratio'] = df.GLD/df.SLV
        df['log_ret'] = np.log10(df.ratio)
        #df = df.loc[:,['Date','Close']]
        #df.columns = []
        fig = px.density_heatmap(df.corr(),x= x, y=y) 
        res = (adfuller(df.ratio))
        return res

    @staticmethod
    def volatility_ratio(ticker,period1,period2):
        '''
        @ticker: ticker in lower letter 
        @period1: must be greater than 60 day
        @period2: must be greater than 60 days
        '''
        ticker = ticker.upper()
        x = pd.DataFrame(data=yf.download(ticker,period=period1,interval='1d'))
        x = x.drop(['Volume'],axis=1)
        x['mean_price'] = x.mean(axis=1)
        y = pd.DataFrame(data=yf.download(ticker,period=period2,interval='1d'))
        y = y.drop(['Volume'],axis=1)
        y['mean_price'] = y.mean(axis=1)
        vol_ratio = (x['mean_price'].mean()) / y['mean_price'].mean()

        return f'the volatility ratio of {ticker} between the period of {period1} and period of {period2} is: {vol_ratio}'

    #performance report
    def percent_win(self,strategy):
        return round((strategy.profit[strategy.profit > 0].count()/strategy.profit.count() * 100),2)

    def avg_gain(self,strategy):
        return round(strategy.profit[strategy.profit > 0].mean(),2)
    
    def max_gain(self,strategy):
        return round(strategy.profit.max(),2)
    
    def max_gain_date(self,strategy):
        return strategy.profit.idxmax()
    
    def max_loss(self,strategy):
        return round(min(strategy.profit.min(),2))
    
    def max_loss_date(self,strategy):
        return strategy.profit.idxmin()
    
    def sharpe_ratio(self,strategy):
        return strategy.daily_return.mean()/strategy.daily_return.std()

    def performance_report(self):
        strategy = self.IBS()
        d = {"Performance_Report":['Profit','Operations','Percent Winning Trades',
        'Percent Losing Trades','Max Gain', 'Average Gain','Max Loss', 'Sharpe Ratio'],
        'Result':[sum(strategy.profit),sum(strategy.position),self.percent_win(strategy),
        100-self.percent_win(strategy),
        self.max_gain(strategy),self.avg_gain(strategy),self.max_loss(strategy),
        self.sharpe_ratio(strategy)]}
        
        df = pd.DataFrame(d,columns=["Performance_Report",'Result'])
        conn = sqlite3.connect('perf_db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS performance (Performance_Report text, Result number)')
        conn.commit()
        df = df.to_sql('performance',conn, if_exists='replace',index=False)

        #c.execute('''
        #SELECT * FROM performance
        #''')
        #for r in c.fetchall():
        #    print(r)
        
        return df 

    #graphic perfomance
    def plot_performance(self,strategy):
        plt.figure(figsize=(8,4),dpi=100)
        plt.plot(strategy.equity, color='green',linewidth=1.0)
        plt.xlabel("Period")
        plt.ylabel("Profit-Loss")
        plt.title("Strategy Performance")
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


#streamlit run trading.py
#python3 trading.py
print(Trading().volatility_ratio('eth-usd','3mo','1y'))
#Trading.plot_performance(self=Trading,strategy=a)
