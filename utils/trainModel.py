# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split 
from pycaret.regression import setup as setupRegression # Importing regression specific setup from pycaret library
from pycaret.classification import setup as setupClassification # Importing classification specific setup from pycaret library
from pycaret.regression import compare_models as compareRegressionModels # Importing function to compare regression models from pycaret library 
from pycaret.classification import compare_models as compareClassificationModels # Importing function to compare classification models from pycaret library

# Function to split data into training and testing sets
def splitData(df, splitratio):
    """
    Splits the input dataframe into training and testing sets based on the given split ratio.
    
    Parameters:
        - df : input dataframe to be split
        - splitratio : percentage of data to be used for testing
        
    Returns:
        - train : subset of dataframe used for training the model
        - test : subset of dataframe used for testing the model
    """
    train, test = train_test_split(df, test_size=int(splitratio)/100, random_state=42, shuffle=True)
    return train, test

# Function to train machine learning model using pycaret  library
def trainModel(df, problem, target):
    """
    Function used for training machine learning model based on the type of problem
    
    Parameters:
        - df : input dataframe 
        - problem : type of problem i.e. Regression or Classification
        - target : target variable to be predicted
        
    Returns:
        - best : Optimal trained model based on comparison between different models
    """
    if problem == 'Regression':
        setupRegression(data = df, target = target, session_id=123) # Setting up the environment and training models
        best = compareRegressionModels() # Comparing regression models to get the best model with optimal hyperparameters
        return best
    elif problem == 'Classification':
        setupClassification(data = df, target = target, session_id=123) # Setting up the environment and training models
        best = compareClassificationModels() # Comparing classification models to get the best model with optimal hyperparameters
        return best