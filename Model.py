import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as sco
import seaborn as sns
from matplotlib.ticker import PercentFormatter


class Model:
    """A class for appying the Modern Portfolio Theory"""

    def __init__(self, data, benchmark, risk_free_rate, tickers, dir):
        self.data = data
        self.nb_stocks = data.shape[1]
        self.mean_returns = data.mean()
        self.cov_matrix = data.cov()
        self.benchmark = benchmark
        self.mean_benchmark = benchmark.mean()
        self.risk_free_rate = risk_free_rate
        self.tickers = tickers
        self.dir = dir

    def portfolio_annualised_performance(self, weights):
        returns = np.sum(self.mean_returns * weights) * self.data.shape[0]
        std = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights))) * np.sqrt(self.data.shape[0])
        return std, returns

    def neg_sharpe_ratio(self, weights):
        p_var, p_ret = self.portfolio_annualised_performance(weights)
        return -(p_ret - self.risk_free_rate) / p_var

    def max_sharpe_ratio(self, w_min, w_max):
        num_assets = self.nb_stocks
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (w_min, w_max)
        bounds = tuple(bound for asset in range(num_assets))
        result = sco.minimize(self.neg_sharpe_ratio, num_assets * [1. / num_assets, ],
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def portfolio_volatility(self, weights):
        return self.portfolio_annualised_performance(weights)[0]

    def min_variance(self):
        num_assets = self.nb_stocks
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = sco.minimize(self.portfolio_volatility, num_assets * [1. / num_assets, ],
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def efficient_return(self, target):
        num_assets = self.nb_stocks

        def portfolio_return(weights):
            return self.portfolio_annualised_performance(weights)[1]

        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        result = sco.minimize(self.portfolio_volatility, num_assets * [1. / num_assets, ], method='SLSQP',
                              bounds=bounds, constraints=constraints)
        return result

    def efficient_frontier(self, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.efficient_return(ret))
        return efficients

    def display_ef_with_selected(self):
        max_sharpe = self.max_sharpe_ratio(0.0, 1.0)
        sdp, rp = self.portfolio_annualised_performance(max_sharpe['x'])
        max_sharpe_allocation = pd.DataFrame(max_sharpe.x, index=self.data.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]

        max_sharpe_bis = self.max_sharpe_ratio(0.0, 0.15)
        sdp_bis, rp_bis = self.portfolio_annualised_performance(max_sharpe_bis['x'])
        max_sharpe_allocation_bis = pd.DataFrame(max_sharpe_bis.x, index=self.data.columns, columns=['allocation'])
        max_sharpe_allocation_bis.allocation = [round(i * 100, 2) for i in max_sharpe_allocation_bis.allocation]

        min_vol = self.min_variance()
        sdp_min, rp_min = self.portfolio_annualised_performance(min_vol['x'])
        min_vol_allocation = pd.DataFrame(min_vol.x, index=self.data.columns, columns=['allocation'])
        min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]

        an_vol = np.std(self.data) * np.sqrt(self.data.shape[0])
        an_rt = self.mean_returns * self.data.shape[0]
        an_vol_bench = np.std(self.benchmark) * np.sqrt(self.benchmark.shape[0])
        an_rt_bench = self.mean_benchmark * self.benchmark.shape[0]

        print("-" * 80)
        print("Individual Stock Returns and Volatility\n")
        for i, txt in enumerate(self.data.columns):
            print(txt, ":", "annualised return", round(an_rt[i], 2), ", annualised volatility:", round(an_vol[i], 2))
        print("-" * 80)
        print("CAC40 Index Returns and Volatility\n")
        print("Annualised Return:", round(an_rt_bench, 2))
        print("Annualised Volatility:", round(an_vol_bench, 2))
        print("-" * 80)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        print("Annualised Return:", round(rp, 2))
        print("Annualised Volatility:", round(sdp, 2))
        print("\n")
        print(max_sharpe_allocation)
        print("-" * 80)
        print("Maximum Sharpe Ratio Portfolio Allocation with weights <= 15%\n")
        print("Annualised Return:", round(rp_bis, 2))
        print("Annualised Volatility:", round(sdp_bis, 2))
        print("\n")
        print(max_sharpe_allocation_bis)
        print("-" * 80)
        print("Minimum Volatility Portfolio Allocation\n")
        print("Annualised Return:", round(rp_min, 2))
        print("Annualised Volatility:", round(sdp_min, 2))
        print("\n")
        print(min_vol_allocation)
        print("-" * 80)

        fig, ax = plt.subplots(figsize=(11, 7))
        ax.scatter(an_vol, an_rt, marker='o', s=20)

        for i, txt in enumerate(self.data.columns):
            ax.annotate(txt, (an_vol[i], an_rt[i]), xytext=(10, 0), textcoords='offset points')
        ax.scatter(sdp, rp, marker='*', color='r', s=100, label='Maximum Sharpe ratio')
        ax.scatter(sdp_bis, rp_bis, marker='*', color='c', s=100, label='Maximum Sharpe ratio bis')
        ax.scatter(sdp_min, rp_min, marker='*', color='g', s=100, label='Minimum volatility')
        ax.scatter(an_vol_bench, an_rt_bench, marker='*', color='m', s=100, label='CAC40 Index')

        target = np.linspace(rp_min, round(an_rt.max(),2), 100)
        efficient_portfolios = self.efficient_frontier(target)
        ax.plot([p['fun'] for p in efficient_portfolios], target, linestyle='-.', color='black',
                label='efficient frontier')
        plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_title('Portfolio Optimisation with Individual Stocks')
        ax.set_xlabel('annualised volatility')
        ax.set_ylabel('annualised returns')
        ax.legend(labelspacing=0.8)
        plt.savefig(os.path.join(self.dir, 'Portfolio_Optimisation_of_the_CAC40_stocks.png'), bbox_inches='tight', dpi=400)

        plt.figure(figsize=(14, 10))
        sns.set_style("darkgrid")
        my_range = range(1, len(max_sharpe_allocation.index) + 1)
        my_color = np.where(max_sharpe_allocation['allocation'] != 0, 'orange', 'skyblue')
        my_size = np.where(max_sharpe_allocation['allocation'] != 0, 70, 30)
        plt.hlines(y=my_range, xmin=0, xmax=max_sharpe_allocation['allocation']/100, color=my_color, alpha=0.4)
        plt.scatter(max_sharpe_allocation['allocation']/100, my_range, color=my_color, s=my_size, alpha=1)
        plt.yticks(my_range, max_sharpe_allocation.index)
        plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
        plt.title("Portfolio allocation max sharpe ratio")
        plt.xlabel('Weights')
        plt.ylabel('Stocks')
        plt.savefig(os.path.join(self.dir, 'max_sharpe_allocation.png'), bbox_inches='tight', dpi=400)

        plt.figure(figsize=(14, 10))
        sns.set_style("darkgrid")
        my_range = range(1, len(max_sharpe_allocation_bis.index) + 1)
        my_color = np.where(max_sharpe_allocation_bis['allocation'] != 0, 'orange', 'skyblue')
        my_size = np.where(max_sharpe_allocation_bis['allocation'] != 0, 70, 30)
        plt.hlines(y=my_range, xmin=0, xmax=max_sharpe_allocation_bis['allocation']/100, color=my_color, alpha=0.4)
        plt.scatter(max_sharpe_allocation_bis['allocation']/100, my_range, color=my_color, s=my_size, alpha=1)
        plt.yticks(my_range, max_sharpe_allocation_bis.index)
        plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
        plt.title("Portfolio allocation max sharpe ratio for weight less than 15%")
        plt.xlabel('Weights')
        plt.ylabel('Stocks')
        plt.savefig(os.path.join(self.dir, 'max_sharpe_allocation_bis.png'), bbox_inches='tight', dpi=400)

        plt.figure(figsize=(14, 10))
        sns.set_style("darkgrid")
        my_range = range(1, len(min_vol_allocation.index) + 1)
        my_color = np.where(min_vol_allocation['allocation'] != 0, 'orange', 'skyblue')
        my_size = np.where(min_vol_allocation['allocation'] != 0, 70, 30)
        plt.hlines(y=my_range, xmin=0, xmax=min_vol_allocation['allocation']/100, color=my_color, alpha=0.4)
        plt.scatter(min_vol_allocation['allocation']/100, my_range, color=my_color, s=my_size, alpha=1)
        plt.yticks(my_range, min_vol_allocation.index)
        plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
        plt.title("Portfolio allocation min volatility")
        plt.xlabel('Weights')
        plt.ylabel('Stocks')
        plt.savefig(os.path.join(self.dir, 'min_vol_allocation.png'), bbox_inches='tight', dpi=400)