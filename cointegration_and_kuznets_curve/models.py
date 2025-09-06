from statsmodels.tsa.vector_ar.vecm import VECM

#VECM is automatically run at first difference(use variables at level)
def model_VECM(df):
    #I used 'lo' because I see some series have a trend.
    vecm = VECM(df, k_ar_diff=1, coint_rank=1, deterministic='lo')
    vecm_fit = vecm.fit()
    print(vecm_fit.summary())
    return vecm_fit

