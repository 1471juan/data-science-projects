from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen

#Use variables on their level(not on differences)
#JOHANSEN COINTEGRATION TEST
def Johansen_cointegration(df): 
    model = coint_johansen(df, det_order=0, k_ar_diff=1)
    print(model)
    print("Statistic value:", model.lr1)
    print("Critical values (95%):", model.cvt[:, 1])

#DICKEY FULLER
def adf(serie,a):
    result = adfuller(serie, regression=a)
    tag = ['statistic', 'p-value', 'lags', 'obs']
    for value, q in zip(result[:4], tag):
        print(f'{q:20}: {value:.4f}')
    print('\n critical vlaue:')
    for x, value in result[4].items():
        print(f' Level {x:>4} : {value:.4f}')
    #AIC
    print(f'\nAIC: {result[5]:.4f}')

#ENGLE-GRANGER
def E_G_cointegration(serie1,serie2):
    result = coint(serie1, serie2, trend='c')
    stat, p, c = result
    print(f'trace statistic: {stat:.4f}')
    print(f'p-value: {p:.4f}')
    print('critical values:')
    print(c)