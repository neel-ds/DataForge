# Importing the pandas library and aliasing it as "pd" for easy reference
import pandas as pd 

# Importing the python in-built library, json.

import json

# Declaring a function named preProcess with df as its argument

def preProcess(df):

    # Initializing an empty list called dropped_columns
    dropped_columns = []

    # Dropping column if more than 50% of the data of the column is null else drop rows and store the dropped columns in a list
    # Looping through each column in the dataframe's columns list

    for col in df.columns:

        # Checking if number of NaN values in the column is greater than half the length of the dataframe

        if df[col].isnull().sum() > len(df)*0.5:

            # Drop the column using drop() method along the column axis (axis=1)
            df = df.drop(col, axis=1)

            # Adding the dropped column name to the dropped_columns list
            dropped_columns.append(col)

        else:

            # If the column has less NaN values, drop the corresponding rows
            df = df.dropna(axis=0)

    # Initialize an empty dictionary called le_data
    le_data = {}

    # Loop through each column which has datatype 'object'
    for col in df.select_dtypes(include='object'):

        # Initialize an empty dictionary called le_dict
        le_dict = {}

        # If number of unique values in the column is greater than 10, skip the current column and move to the next column
        if(len(df[col].unique()) > 10):
            df = df.drop(col, axis=1) # Drop the column using drop() method along the column axis (axis=1)
            dropped_columns.append(col) # Adding the dropped column name to the dropped_columns list
            continue 

        # For each unique value in the column    
        for val in df[col].unique():

            # Check if the value is already present in the le_dict
            if val not in le_dict:
                # If not, add it to the le_dict with its corresponding index as its value
                le_dict[val] = len(le_dict) + 1

        # Add the key-value pair of the column name and its corresponding le_dict to the le_data dictionary  
        le_data[col] = le_dict

        # Replace the original values in the column with their corresponding indexes from le_dict
        df[col] = df[col].replace(le_dict)

    # Add another key-value pair to the le_data dictionary containing a list of all the dropped columns 
    le_data['dropped_columns'] = dropped_columns

    # Open a json file named "encoding.json" in write mode
    with open('encoding.json', 'w') as f:

        # Write the contents of the le_data dictionary as json into the file
        json.dump(le_data, f)

    # Return the cleaned dataframe after pre-processing and encoding all the categorical columns as numerical indices.
    return df 
