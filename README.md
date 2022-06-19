# Trading-Eng
Building a **Trading Engine** in **Python**

> List of functions:

- **Trading.IBS()** IBS (Internal Bar Strenght Indicator) is based on the position of the day’s close in relation to the day’s range: it takes a value of 0 if the closing price is the lowest price of the day, and 1 if the closing price is the highest price of the day. The strategy buys at the close when IBS is below 0.2, and sells at the close when IBS exceeds 0.8, liquidating the position at the close

this strategy is referring to this article: http://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/

![](https://github.com/leo-ai-for-trading/Finance-OOP/blob/main/clips/clip-giusta.gif)
