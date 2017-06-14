from flask import Flask
from flask import render_template
from flask import request
from flask.ext.cors import CORS, cross_origin
from neural_network.neural_network_prediction import Prediction

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict')
@cross_origin()
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

if __name__ == '__main__':
    app.run(debug=True)
