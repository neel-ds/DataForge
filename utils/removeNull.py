import pandas as pd 

def removeNull(file):
    df = pd.read_csv(file)
    df = df.dropna(axis=0)
    return df