import pandas as pd

def preProcess(df): 
    # Drop column if more than 50% of data of column is null else drop rows
    df = df.dropna(axis=1, thresh=len(df)*0.5)
    df = df.dropna(axis=0)

    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() < (0.3 * df.shape[0]):
            df = pd.concat([df, pd.get_dummies(df[col], prefix=col)], axis=1)
            df.drop(columns=[col], inplace=True)
        else:
            df.drop(columns=[col], inplace=True)
    
    return df