from flask import Flask
from flask_cors import CORS

# 설정 및 서비스 초기화
from src import config

# 라우트 및 소켓 핸들러 임포트
from src.routes import api
from src.simulation import socketio

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio.init_app(app, cors_allowed_origins="*")

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
