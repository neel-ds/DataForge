from flask import Flask, render_template, request, redirect, jsonify
from utils.preProcess import preProcess
from utils.generateEDA import filterHTML
from utils.trainModel import *
import numpy as np
import pickle

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
        # train, test = splitData(df, target, splitratio)        
        # model = trainModel(train, problem[0], target)
        # model.fit(train.drop(target, axis=1), train[target])
        # print(model.score(test.drop(target, axis=1), test[target]))
        # # save model into pickle file 
        # pickle.dump(model, open('model.pkl', 'wb'))
        return render_template('project.html')
    return redirect('/project')

@app.route('/deploy', methods=['POST'])
def deploy(): 
    if request.method == 'POST':
        # load model from pickle file
        model = pickle.load(open('model.pkl', 'rb'))
        
        # Get the data from the POST request.
        data = request.get_json(force=True)

        # Convert data into 2d np array
        data = np.array(data['params']).reshape(1, -1)

        # Make prediction using model loaded from disk as per the data.
        prediction = model.predict(data)

        return jsonify({'Output': str(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)