from flask import Flask
from flask_cors import CORS

from src import config

from src.routes import api

app = Flask(__name__)

CORS(app)

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
