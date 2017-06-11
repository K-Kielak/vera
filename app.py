from flask import Flask
from flask import render_template
from flask import request
from neural_network.neural_network_prediction import Prediction

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict')
def vera():
    try:
        url = request.args.get('url')
        prediction = Prediction.is_fake(url)
        if prediction:
            return 'fake'
        else:
            return 'real'
    except Exception:
        return 'error'

app.run()
