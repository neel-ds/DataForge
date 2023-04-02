from flask import Flask, render_template, request, redirect, jsonify
from utils.preProcess import preProcess
from utils.generateEDA import filterHTML
from utils.trainModel import *
import numpy as np
import pickle
import json
import requests as req

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        df = removeNull(file)
        filterHTML(df)
        return render_template('report.html')
    return redirect('/project')

#Endpoint to create a ml model using pycaret
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

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        params = {}
        labels = []
        values = []
        for key in request.form.keys():
            if key.startswith('param-label-'):
                label = request.form[key]
                labels.append(label)
            elif key.startswith('param-value-'):
                value = request.form[key]
                values.append(value)
        for i in range(len(labels)):
            params[labels[i]] = values[i]

        json_data = json.dumps(params)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        url = 'http://127.0.0.1:5000/deploy'

        response = req.post(url, data=json_data, headers=headers)

        print(response.text)

        return render_template('deploy.html', params=params)

    return render_template('deploy.html')

if __name__ == '__main__':
    app.run(debug=True)