from flask import Flask, render_template, request, redirect
from utils.removeNull import removeNull
from utils.generateEDA import filterHTML

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

if __name__ == '__main__':
    app.run(debug=True)