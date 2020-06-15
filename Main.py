import json
import os
import pandas as pd
from Data_processor import DataLoader
from Model import Model


def main():
    configs = json.load(open('config.json', 'r'))
    if not os.path.exists(configs['data']['save_dir']): os.makedirs(configs['data']['save_dir'])
    if not os.path.exists(configs['model']['save_results']): os.makedirs(configs['model']['save_results'])

    # Extract data from Yahoo finance
    if configs['data']['extraction']:
        DataLoader(configs['data']['tickers'], configs['data']['benchmark'], configs['data']['column'],
                   configs['data']['save_dir']).get_data()

    # Read csv files
    data = pd.read_excel(os.path.join(configs['data']['save_dir'], 'CAC40_stocks.xlsx'), index_col=0)
    benchmark = pd.read_excel(os.path.join(configs['data']['save_dir'], 'CAC40_index.xlsx'), index_col=0)

    # Apply the Modern Portfolio Theory Markowitz
    model = Model(data, benchmark, configs['model']['risk_free_rate'], configs['data']['tickers'], configs['model']['save_results'])
    model.display_ef_with_selected()


if __name__ == '__main__':
    main()
