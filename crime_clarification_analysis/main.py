import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from plot import *

def load_data():
    #this dataset is not utf-8, but ISO-8859-1 (latin1)
    return pd.read_csv('data/Delitos_denunciados.csv', encoding='latin1')

def process_data(df:pd.DataFrame):
    #turn dates into datetime64 type
    df['FECHA']=pd.to_datetime(df['FECHA'], format='%d.%m.%Y')
    #turn gender column to values (0 male, 1 female)
    for i, value in enumerate(df['SEXO']):
        if value=='HOMBRE':
            df.loc[i,'SEXO'] = 0
        else:
            df.loc[i,'SEXO'] = 1

    #turn clarified column to values(0 the case was not clarified, 1 the case was clarified)
    for i, value in enumerate(df['ACLARADO']):
        if value=='SIN ACLARAR':
            df.loc[i,'ACLARADO'] = 0
        else:
            df.loc[i,'ACLARADO'] = 1

    #merge all departments except Montevideo
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].apply(
        lambda x: x if x in ['MONTEVIDEO'] else 'OTROS'
    )

    #turn into dummies
    cols = ['TIPO','MES','MOTIVO_APARENTE','DEPARTAMENTO']
    df = pd.get_dummies(df, columns=cols, drop_first=True)
    dummy_cols = [c for c in df.columns if any(c.startswith(col+'_') for col in cols)]
    df[dummy_cols] = df[dummy_cols].astype(int)
    
    return df

def drop_columns(df, col):
    return df.drop(columns=col)

def model_probit_1(df):
    y = df['ACLARADO'].astype(int)
    X = df.drop(columns=['ACLARADO', 'ID_VICTIMA', 'FECHA'])
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    X = sm.add_constant(X)
    print(X)
    model = sm.Probit(y, X).fit()
    return model

def model_probit_2(df):
    #define regressors
    y = df['ACLARADO'].astype(int)
    X = df.drop(columns=['ACLARADO', 'ID_VICTIMA', 'FECHA'])
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    #check columns with problems
    perfect_pred_vars = []
    for col in X.columns:
        cross_tab = pd.crosstab(X[col], y)
        if (cross_tab == 0).any(axis=None): 
            perfect_pred_vars.append(col)
        
    #print(perfect_pred_vars)
    #drop them, except for "EDADCALC"
    X= X.drop(columns=['TIPO_A CLIENTE DE CAJERO / BANCO', 'TIPO_A TAXIS'])

    #split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    #constatn
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)
    
    #estimate model
    model = sm.Probit(y_train, X_train).fit()
    print(model.summary())
    
    #predict
    y_pred_prob = model.predict(X_test)

    #if the probability is higher than 50%, we predict 1, otherwise, we predict 0.
    y_pred = (y_pred_prob >= 0.5).astype(int)
    #print(y_pred_prob)
    #print(y_pred)
    
    #performance
    print("accuracy:", accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    return model

def model_probit_3(df):

    df['SEXO_x_VIOLENCIA'] = df['SEXO'] * df['MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS']
    df['EDADCALC'] = pd.to_numeric(df['EDADCALC'], errors='coerce').fillna(0)
    df['EDADCALC_sq'] = df['EDADCALC'].astype(int) ** 2

    y = df['ACLARADO'].astype(int)
    X = df.drop(columns=['ACLARADO', 'ID_VICTIMA', 'FECHA'])
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    perfect_pred_vars = []
    for col in X.columns:
        cross_tab = pd.crosstab(X[col], y)
        if (cross_tab == 0).any(axis=None): 
            perfect_pred_vars.append(col)
    #print(perfect_pred_vars)
    X= X.drop(columns=['TIPO_A CLIENTE DE CAJERO / BANCO', 'TIPO_A TAXIS'])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)
    
    model = sm.Probit(y_train, X_train).fit()
    print(model.summary())
    
    y_pred_prob = model.predict(X_test)

    y_pred = (y_pred_prob >= 0.5).astype(int)
    
    print("accuracy:", accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    return model

def model_show_marginal_effects(model):
    model_me = model.get_margeff(at='overall', method='dydx')     
    print(model_me.summary())
    model_me_dummy = model.get_margeff(at='overall', method='dydx', dummy=True)
    print(model_me_dummy.summary())

def main():
    #Load data
    data=load_data()

    #Get data
    #print(data)
    #print(data.dtypes)

    #Get column names
    #print(data.columns)

    #print(list(data['TIPO']))

    #Process data
    data = process_data(data)
    data = drop_columns(data,['MENORESCINICIOPROC','TRIMESTRE', 'DIA_SEMANA', 'HORA','AÑO','PROCESADOS', 'ARMAREC', 'LUGAR','NACIONALIDAD','REL_VICT_AGRES','JURISDICCION','ANTECEDENTESPORESTUPEFACIENTES','ANTECEDENTES'])

    #Plot variables
    #plot_count(data)
    #plot_victim_sex(data)
    #plot_count_by_SEXO(data)
    #plot_count_by_EDADCALC(data)
    #plot_cases_per_hour(data)
    #plot_count_by_HORA(data)
    #plot_antecedentes_aclarado(data)

    #Print column names
    #print(list(data.columns))
    #print(data.dtypes)

    #Models
    #print(model_probit_1(data).summary())

    #model=model_probit_2(data)
    #model_show_marginal_effects(model)
    
    model_2=model_probit_3(data)
    model_show_marginal_effects(model_2)




if __name__ == "__main__":
    main()