import pandas as pd
import json

def preProcess(df): 

    # Drop column if more than 50% of data of column is null else drop rows and store the dropped columns in a list
    dropped_columns = []
    for col in df.columns:
        if df[col].isnull().sum() > len(df)*0.5:
            df = df.drop(col, axis=1)
            dropped_columns.append(col)
        else:
            df = df.dropna(axis=0)

    le_data = {}
    for col in df.select_dtypes(include='object'):
        le_dict = {}
        if(len(df[col].unique()) > 10):
            df = df.drop(col, axis=1)
            dropped_columns.append(col)
            continue
        for val in df[col].unique():
            if val not in le_dict:
                le_dict[val] = len(le_dict) + 1
        le_data[col] = le_dict
        
        df[col] = df[col].replace(le_dict)

    le_data['dropped_columns'] = dropped_columns

    with open('encoding.json', 'w') as f:
        json.dump(le_data, f)    

    return df