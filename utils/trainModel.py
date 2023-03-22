import pandas as pd
from sklearn.model_selection import train_test_split
from pycaret.regression import *
from pycaret.classification import *

def splitData(df, target, splitratio):
    X = df.drop(target, axis=1)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=int(splitratio)/100, random_state=42)
    return X_train, X_test, y_train, y_test

def trainModel(X_train, X_test, y_train, y_test, problem, target):
    print(problem)
    if problem == 'Regression':
        exp_reg101 = setup(data = X_train.reset_index(), target = target, session_id=123)
        best = compare_models()
        return best
    elif problem == 'Classification':
        exp_clf101 = setup(data = X_train, target = y_train, session_id=123)
        best = compare_models()
        return best