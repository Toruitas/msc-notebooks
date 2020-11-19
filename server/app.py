from flask import Flask, jsonify, request
from flask_cors import CORS
from fastai import *
from fastai.text.all import *

app = Flask(__name__)
cors = CORS(app)
defaults.device = torch.device('cpu')

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/predict', methods=['POST'])
def predict_controversy():
    json_body = request.json
    prediction = learner.predict(json_body['title'])
    return jsonify({'prediction': prediction[0]})
  
if __name__ == '__main__':
    
    learner = load_learner("final-classifier.pkl")
    app.run(port=8000)