# Modern-Portfolio-Theory-Markowitz
In this project, I use modern portfolio theory to build the most efficient portfolio with the 40 stocks listed in the CAC40 index.

## Requirements
Here are the versions of the librairies I used for this project.

* Python 3.7
* Pandas 1.0.3
* Numpy 1.18.2
* yfinance 0.1.54
* Matplotlib 2.2.2
* Scipy 1.4.1
* Seaborn 0.10.1

## Modern Portfolio Theory

Modern portfolio theory is a financial theory developed in 1952 by Harry Markowitz. It explains how rational investors use diversification to optimize their portfolios and find the best risk-return trade-off. Indeed, if the return of a portfolio is equal to the weighted average of each individual stock's return in the portfolio, it is not the case for the risk. The risk is about how volatile the asset is, if you have more than one stock in your portfolio, then you have to take count of how these stocks movement correlates with each other. The beauty of diversification is that you can even get lower risk than a stock with the lowest risk in your portfolio, by optimising the allocation.

## Results

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/Portfolio_Optimization_of_the_CAC40_stocks.png?raw=true)

This graph highlights the advantage of having a diversified portfolio rather than a single stock. In fact, for all stocks except STM.PA, it is possible to build a portfolio that will offer a higher return for a certain level of risk. The efficient frontier provides the lowest risk for a certain return. Therefore, it is logical that the stock with the highest return (STM.PA) belongs to the efficient frontier. 

The maximum sharpe ratio is represented by a red star, the minimum volatility by a green star and the maximum sharpe ratio for a portfolio with weights not exceeding 15% by a blue star. The composition of these portfolios will be studied afterwards. Finally, the CAC40 index has been included (purple star). Thus, we can see that there are a multitude of stock combinations that can beat the CAC40 index.

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/max_sharpe_allocation.png?raw=true)

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/max_sharpe_allocation_bis.png?raw=true)

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/min_vol_allocation.png?raw=true)
