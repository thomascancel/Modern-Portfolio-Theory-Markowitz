# Modern-Portfolio-Theory-Markowitz
In this project, I used the Modern Portfolio Theory to build the most efficient portfolio with the stocks listed in the CAC40 index.

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

Modern portfolio theory is a financial theory developed in 1952 by Harry Markowitz. It explains how rational investors use diversification to optimise their portfolios and find the best risk-return trade-off. Indeed, if the return of a portfolio is equal to the weighted average of each individual stock's return in the portfolio, it is not the case for the risk. The risk is about how volatile the asset is, if you have more than one stock in your portfolio, then you have to take count of how these stocks movement correlates with each other. The beauty of diversification is that you can even get lower risk than a stock with the lowest risk in your portfolio, by optimising the allocation.

## Results

The data used for this project contains the historical values of the 40 stocks of the CAC40 as well as the value of the index between July 2, 2019 and June 30, 2020 (1 year of historical data). They can be updated by changing the 'extraction' field in the json file. However, be careful when extracting data from Yahoo finance it is possible that rows containing zeros will be added, which will create a dimension error...

### Efficient frontier

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/Portfolio_Optimisation_of_the_CAC40_stocks.png?raw=true)

This graph highlights the advantage of having a diversified portfolio rather than a single stock. In fact, for all stocks except STM.PA, it is possible to build a portfolio that will offer a higher return for a certain level of risk. The efficient frontier provides the lowest risk for a certain return. Therefore, it is logical that the stock with the highest return (STM.PA) belongs to the efficient frontier. 

The maximum sharpe ratio is represented by a red star, the minimum volatility by a green star and the maximum sharpe ratio for a portfolio with weights not exceeding 15% by a blue star. The composition of these portfolios will be studied afterwards. Finally, the CAC40 index has been included (purple star). Thus, we can see that there are a multitude of stock combinations that can beat the CAC40 index.

### Portfolio allocation: maximum sharpe ratio

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/max_sharpe_allocation.png?raw=true)

The maximum sharpe ratio is obtained by creating a portfolio composed of 48.77% STM.PA and 51.23% SAN.PA. The annualised return is then 39% for a risk of 33%. Constraints on weights can be added to obtain a more diversified portfolio.

### Portfolio allocation: maximum sharpe ratio with weights<=15% 

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/max_sharpe_allocation_bis.png?raw=true)

Here I have added as a constraint to my portfolio that the weights cannot be over 15%. This more diversified portfolio offers an annualised return of 27% for a risk of 27%.

### Portfolio allocation: minimum risk

![alt text](https://github.com/thomascancel/Modern-Portfolio-Theory-Markowitz/blob/master/results/min_vol_allocation.png?raw=true)

To create the minimum risk portfolio, we need to increase the diversification. Thus, 8 stocks are needed with weights between 27.72% (SAN.PA) and 0.77% (VIV.PA). In such cases, the annualised return is 4% for a risk of 20%.
