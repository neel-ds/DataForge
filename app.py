from flask import Flask, render_template, request, redirect
from utils.removeNull import removeNull
from utils.generateEDA import filterHTML
from utils.trainModel import *
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/deploy')
def deploy():
    return render_template('deploy.html')

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
        df = removeNull(file)
        X_train, X_test, y_train, y_test = splitData(df, target, splitratio)
        print(X_train.columns)
        model = trainModel(X_train, X_test, y_train, y_test, problem[0], target)
        model.fit(X_train, y_train)
        print(model.score(X_test, y_test))
        print(model.predict(np.array([1,1,0,150,276,0,0,112,1,0.6,1,1,1]).reshape(1, -1)))
        return render_template('project.html')
    return redirect('/project')

if __name__ == '__main__':
    app.run(debug=True)