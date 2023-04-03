from flask import Flask, render_template, request, redirect, jsonify
from utils.preProcess import preProcess
from utils.generateEDA import filterHTML
from utils.trainModel import *
import numpy as np
import pickle
import json
import requests as req
from pandas_profiling import ProfileReport
from utils.test import test

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/report')
def report():
    return render_template('analytics.html')


@app.route('/edaReport')
def edareport():
    return render_template('report.html')


@app.route('/check')
def check():
    return render_template('test.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        filterHTML(df)
        return render_template("report.html")
    return redirect('/project')

# Endpoint to create a ml model using pycaret


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        file = request.files['file']
        target = request.form['target']
        splitratio = request.form['splitratio']
        problem = request.form.getlist('problem')
        df = pd.read_csv(file)
        df = preProcess(df)
        print(df.columns)
        train, test = splitData(df, target, splitratio)
        model = trainModel(train, problem[0], target)
        model.fit(train.drop(target, axis=1), train[target])
        print(model.score(test.drop(target, axis=1), test[target]))
        # save model into pickle file
        pickle.dump(model, open('model.pkl', 'wb'))
        return render_template('project.html')
    return redirect('/project')


@app.route('/deploy', methods=['POST'])
def deploy():
    if request.method == 'POST':
        # load model from pickle file
        model = pickle.load(open('model.pkl', 'rb'))

        # Get the data from the POST request.
        data = request.get_json(force=True)

        # Get the values from json file, preprocess it using encoding.json and convert it into numpy array
        df = pd.DataFrame(data, index=[0])

        # Read encoding.json file
        with open('encoding.json', 'r') as f:
            le_data = json.load(f)

        # Drop columns which were dropped during training
        df = df.drop(le_data['dropped_columns'], axis=1)

        # Perform label encoding according to le_data
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].replace(le_data[col])

        # Convert dataframe into 2d numpy array
        data = df.to_numpy()

        # Make prediction using model loaded from disk as per the data.
        prediction = model.predict(data)

        return jsonify({'Output': str(prediction[0])})


if __name__ == '__main__':
    app.run(debug=True)
