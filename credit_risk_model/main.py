import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import sklearn.model_selection._split as skl
from sklearn.metrics import accuracy_score, classification_report


def data_process(data):
    categorical=['credithistory', 'savings', 'property', 'job', 'purpose', 'employmentsince', 
                 'personalstatus', 'otherdebtors', 'otherinstallmentplans', 
                 'existingcredits', 'housing','telephone','status', 'foreignworker']
    to_drop=['credit']
    data=data.drop(columns=to_drop)
    for col in categorical:
        data[col] = data[col].astype(str)

    data=pd.get_dummies(data,columns=categorical,drop_first=True)
    for i,value in enumerate(data['creditrisk']):
        if value==1:
            data.loc[i,'creditrisk']=0
        else:
            data.loc[i,'creditrisk']=1
    #print(data['creditrisk'])
    return data
    
def model_1(data:pd.DataFrame):
    y=data['creditrisk'].astype(int)
    X=data.drop('creditrisk',axis=1).astype(int)
    
    X = X.apply(pd.to_numeric, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')
    X_train, X_test, y_train, y_test = skl.train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    #print("shape:", X.shape[1])
    model=RandomForestClassifier(n_estimators=500, max_features=5, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("accuracy:", accuracy_score(y_test, y_pred))
    print( classification_report(y_test, y_pred))
    #return model

def model_2(data:pd.DataFrame):
    y=data['creditrisk'].astype(int)
    X=data.drop('creditrisk',axis=1).astype(int)
    
    X = X.apply(pd.to_numeric, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')
    X_train, X_test, y_train, y_test = skl.train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    acc = []
    for seed in range(10):
        X_train, X_test, y_train, y_test = skl.train_test_split(
            X, y, test_size=0.2, random_state=seed, stratify=y
        )
        model = RandomForestClassifier(n_estimators=500, max_features=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc.append(accuracy_score(y_test, y_pred))

    print("average accuracy:", sum(acc)/10)
    print("std:", np.std(acc))

def main():
    data = pd.read_csv('data/german.csv')
    #print(data)
    #print(list(data.columns))
    
    data_processed=data_process(data)
    #print(list(data.dtypes))

    model_1(data_processed)
    model_2(data_processed)

    

if __name__=="__main__":
    main()