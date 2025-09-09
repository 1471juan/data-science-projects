from data import data_load, data_get_kec
from tests import adf, Johansen_cointegration
from models import model_VECM
from plot import *

def main():
    #Load data
    df = data_load(False)
    #df_kec = data_get_kec(df)
    
    #plot_variable(df, 'realgdp')

    adf(df['totalghg'].diff().dropna(),'c')
    adf(df['fossil'].diff().dropna(),'c')
    adf(df['agr_va'].diff().dropna(),'c')
    adf(df['realgdp'].diff().dropna(),'c')
 
    Johansen_cointegration(df)
    model_VECM(df)
    #plot_irf(model_VECM(df), 0.1)

    #Johansen_cointegration(df_kec)
    #plot_k_curve(df_kec, 10.019)

if __name__ == "__main__":
    main()
