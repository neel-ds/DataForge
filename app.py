# Import necessary Flask modules
from flask import Flask, render_template, request, redirect, jsonify

# Importing user-defined python files with specific functions
from utils.preProcess import preProcess
from utils.generateEDA import filterHTML
from utils.trainModel import *

# Import pickle library to save ml models in disk
import pickle

# Import json library for encoding of categorical data into numerical data
import json

# Initializing a Flask instance called app with __name__=__main__
app = Flask(__name__)


# Route for home page (index.html)
@app.route('/')
def hello_world():
    return render_template('index.html')


# Route for project page
@app.route('/project')
def project():
    return render_template('project.html')


# Route for analytics page
@app.route('/report')
def report():
    return render_template('analytics.html')


# Route for generating EDA report
@app.route('/edaReport')
def edareport():
    return render_template('report.html')


# Route to create a pandas profiling report after loading the dataset from csv
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        # Reading the uploaded CSV file
        file = request.files['file']
        df = pd.read_csv(file)

        # Generating html file for EDA report
        filterHTML(df)

        # Return the report HTML
        return render_template("report.html")
    
    # Redirects to project page if the request method is GET
    return redirect('/project')


# Endpoint for creating a machine learning model using pycaret
@app.route('/train', methods=['GET', 'POST'])
def train():
    # If the request method is POST, execute the following
    if request.method == 'POST':

        # Reading the uploaded CSV file and target column
        file = request.files['file']
        target = request.form['target']

        # Splitting ratio of dataset into training set and testing set
        splitratio = request.form['splitratio']

        # Classification or regression based on problem type selected by user
        problem = request.form.getlist('problem')

        # Reading the csv file as pandas dataframe
        df = pd.read_csv(file)

        # Performing pre-processing of data
        df = preProcess(df)

        # Printing the columns of pre-processed dataframe
        print(df.columns)

        # Splitting the pre-processed dataframe into train and test sets
        train, test = splitData(df, target, splitratio)

        # Training the model on train set
        model = trainModel(train, problem[0], target)

        # Fitting the model on train set
        model.fit(train.drop(target, axis=1), train[target])

        # Evaluating the model's accuracy on test set
        print(model.score(test.drop(target, axis=1), test[target]))

        # Saving the trained model into a pickle file named "model.pkl"
        pickle.dump(model, open('model.pkl', 'wb'))

        # Return the project HTML template
        return render_template('project.html')
    
    # Redirects to project page if the request method is GET
    return redirect('/project')


# Endpoint for deploying the machine learning model for predictions
@app.route('/deploy', methods=['POST'])
def deploy():
    # If the request method is POST, execute the following
    if request.method == 'POST':
 
        # Load the machine learning model from the pickle file named "model.pkl"
        model = pickle.load(open('model.pkl', 'rb'))

        # Get the data from the POST request as JSON
        data = request.get_json(force=True)

        # Convert the received JSON data into pandas dataframe with 1 row
        df = pd.DataFrame(data, index=[0])

        # Read encoding.json file which gives information about how the categorical data has been encoded into numerical data
        with open('encoding.json', 'r') as f:
            le_data = json.load(f)

        # Drop all dropped columns from training phase in case of categorical data
        df = df.drop(le_data['dropped_columns'], axis=1)

        # Replace the categorical data according to the encoding values stored in encoding.json file
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].replace(le_data[col])

        # Convert dataframe into 2D numpy array
        data = df.to_numpy()

        # Predict the output with the loaded model on the converted numpy array based on the input given by the user
        prediction = model.predict(data)

        # Return the output in JSON format
        return jsonify({'Output': str(prediction[0])})


if __name__ == '__main__':
    app.run(debug=True) # Starting the app and running it in debug mode. 