import pandas as pd
import numpy as np

def data_load(use_realgdp_squared=False):
    #LOAD DATA FROM CSV FILES
    data_fossilConsumption = pd.read_csv('data/FossilConsumption.csv', parse_dates=['YEAR'])
    data_population = pd.read_csv('data/TotalPopulation.csv', parse_dates=['YEAR'])
    data_agr_va= pd.read_csv('data/Agriculture_forestry_fishing_value_added.csv', parse_dates=['YEAR'])
    data_realgdp = pd.read_csv('data/real_gdp_uruguay.csv', parse_dates=['YEAR'])
    data_totalghg = pd.read_csv('data/Total_GHG_emissions.csv', parse_dates=['YEAR'])

    #DATAFRAME
    for dataframe in [data_fossilConsumption, data_agr_va, data_realgdp, data_totalghg, data_population]:
        dataframe.set_index('YEAR', inplace=True)
    dataframe = pd.DataFrame(index=data_fossilConsumption.index)
    dataframe['totalghg'] = np.log(data_totalghg['VALUE'] / data_population['VALUE'])
    dataframe['fossil'] = np.log(data_fossilConsumption['VALUE'])
    dataframe['agr_va'] = np.log(data_agr_va['VALUE'])
    dataframe['realgdp'] = np.log(data_realgdp['VALUE'] / data_population['VALUE'])
    if use_realgdp_squared:
        dataframe['realgdp_squared'] = dataframe['realgdp'] ** 2
    dataframe.dropna(inplace=True)

    return dataframe

def data_get_kec(df):
    dataframe_kec = pd.DataFrame({
        'totalghg': df['totalghg'],
        'realgdp': df['realgdp'],
        'realgdp_squared': df['realgdp_squared']
    }).dropna()
    return dataframe_kec