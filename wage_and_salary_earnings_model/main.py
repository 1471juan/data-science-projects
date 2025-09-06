import pandas as pd
import numpy as np
import statsmodels.api as sm

def data_load(str):
    return pd.read_csv(f'data/{str}')

def data_process(df):
    #merge categories
    df['A_HGA_merged'] = pd.cut(df['A_HGA'],bins=[0, 39, 43, 46], labels=[0, 1, 2], right=True).astype(int)
    df['PRDTRACE_merged'] = np.where(df['PRDTRACE'] == 1, 1, 0)
    df['A_MARITL_merged'] = np.where(df['A_MARITL'].isin([1, 2, 3]), 1, 0)
    
    #drop 
    #df=df.drop(columns=['A_MJIND'])

    #dummies
    data = pd.get_dummies(df, columns=["A_SEX","PRDTRACE_merged","PRCITSHP", "A_HGA_merged", "A_MARITL_merged",
            "A_HRLYWK", "WORKYN", "ERN_SRCE", "CAP_YN", "ED_YN",
            "FIN_YN", "CSP_YN", "HEA",'A_MJIND'], drop_first=True)
    
    #drop columns 
    data=data.drop(columns=['PRDTRACE','A_HGA','A_MARITL','A_AGE_SQ'])

    #columns to numeric
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.dropna()
    #print(list(data.dtypes))

    #convert bools to int
    bool_cols = data.select_dtypes(include='bool').columns
    data[bool_cols] = data[bool_cols].astype(int)

    #transformations
    #data['A_AGE_cube'] = data['A_AGE'] * data['A_AGE_SQ']
    #interactions 
    #data['A_AGE_H_NUMPER_INT'] = data['A_AGE'] * data['H_NUMPER']

    return data

def model(df):
    y = df['WSAL_VAL_log']
    X = df.drop(columns=['WSAL_VAL_log','WSAL_VAL'])
    X=sm.add_constant(X)
    model_1 = sm.OLS(y, X).fit()
    print(model_1.summary())
    return model_1,y,X

def get_vif(var:str,df):
    y = df[var]
    X = df.drop(columns=[var])
    mdl=sm.OLS(y,X).fit()
    return 1/(1-mdl.rsquared)

def get_vars_highVIF(X,n):
    var_high_vif=[]
    for v in X.columns:
        vif=get_vif(v, X)
        if vif>n: 
            print(f'VIF FOR {v} is {vif}')
            var_high_vif.append(v)
    return var_high_vif

def get_F_multi(df,m_nr, to_drop):
    #m_nr: not restricted model
    #to_drop: array with the variables to test=0 on null hypothesis
    data=df.drop(columns=[col for col in to_drop if col in df.columns])
    m_r,y,X=model(data)
    q=len(to_drop)
    n=m_nr.nobs
    k=len(m_nr.params)
    print(f'q: {q}')
    print(f'n-k-1: {n-k-1}')
    A=(m_nr.rsquared-m_r.rsquared)/q
    B=(1-m_nr.rsquared)/(n-k-1)
    return A/B

def main():
    #load data
    df = data_load('data_cleaned.csv')

    #print(df)

    #process data
    df=data_process(df)

    #model
    model_1,y,X=model(df)

    #F test
    print(get_F_multi(df,model_1,[f'PRCITSHP_{i}' for i in range(2, 6)]))

    #get VIF for every variable
    print(get_vars_highVIF(X,10))

if __name__ == "__main__":
    main()