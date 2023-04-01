import pandas as pd
from sklearn.model_selection import train_test_split
from pycaret.regression import setup as setupRegression
from pycaret.classification import setup as setupClassification
from pycaret.regression import compare_models as compareRegressionModels
from pycaret.classification import compare_models as compareClassificationModels

def splitData(df, target, splitratio):
    train, test = train_test_split(df, test_size=int(splitratio)/100, random_state=42, shuffle=True)
    return train, test

def trainModel(df, problem, target):
    if problem == 'Regression':
        setupRegression(data = df, target = target, session_id=123)
        best = compareRegressionModels()
        return best
    elif problem == 'Classification':
        setupClassification(data = df, target = target, session_id=123)
        best = compareClassificationModels()
        return best