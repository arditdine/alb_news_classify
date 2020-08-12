#!/usr/bin/env python
from flask import Flask, request, jsonify, render_template
from news_classify import NewsClassify

model = None
app = Flask(__name__, template_folder='templates')

def load_model():
    global model
    model = NewsClassify(train=True)

@app.route('/', methods=['GET'])
def home_endpoint():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        prediction = model.classify(request.form.get('article'))
        return jsonify({'result': str(prediction)})

    return 'Hello Analyzer'

if __name__ == '__main__':
    load_model() # load model at the beginning once only
    app.run(host='0.0.0.0', port=5000)