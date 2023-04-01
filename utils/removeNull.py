import pandas as pd 
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif

def removeNull(file):
    df = pd.read_csv(file)
    df = df.dropna(axis=0)
    # find mutual columns
    print(df.columns)
    return df

def findMutualColumns(X_train, y_train):
    most_mutual = mutual_info_regression(X_train, y_train)
                                                                                      