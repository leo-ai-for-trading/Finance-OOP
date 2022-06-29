# Trading-Eng
Building a **Trading Engine** in **Python**

> List of functions:

```
  Trading.IBS()
```
- ***IBS (Internal Bar Strenght Indicator)*** is based on the position of the day’s close in relation to the day’s range: it takes a value of 0 if the closing price is the lowest price of the day, and 1 if the closing price is the highest price of the day. The strategy buys at the close when IBS is below 0.2, and sells at the close when IBS exceeds 0.8, liquidating the position at the close

this strategy is referring to this article: http://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/

![](https://github.com/leo-ai-for-trading/Trading-Eng/blob/main/clips/clip-giusta.gif)
![](https://github.com/leo-ai-for-trading/Trading-Eng/blob/main/clips/ibs.performance.png)

```
Trading.performance_report():
```
- create a **SQL** databes where you can find a detailed report of the strategy performance
![](https://github.com/leo-ai-for-trading/Trading-Eng/blob/main/clips/performance%20table.png)

```
Trading.Cutler_RSI()
``` 
- ***Cutler’s RSI*** indicator that shows how the IBS effect can be used to boost returns of a swing trading strategy while significantly decreasing the number of trades needed.
Cutler’s RSI at time t is calculated as follows:
![](https://github.com/leo-ai-for-trading/Trading-Eng/blob/main/clips/cutler.png)

```
Trading.volatility_ratio()
```
- computing ***volatility ratio*** between two different time periods in order to implement buy/sell signal
```
Trading.arbitrage()
```
- developed ***abritrage*** strategy[^1] between *$GLD* and *$SLV* 
![](https://github.com/leo-ai-for-trading/Trading-Eng/blob/main/clips/newplot.png)
[^1]: the strategy was implemented with 5 years historical data by using *yfinance* api
