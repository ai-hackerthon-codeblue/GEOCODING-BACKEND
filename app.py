# app.py

from flask import Flask
from flask_cors import CORS

# 설정 및 서비스 초기화 (Firebase, Gemini)
# 이 import 문이 routes보다 먼저 와야 초기화가 완료됩니다.
from src import config

# API 블루프린트 임포트
from src.routes import api

# 1. Flask 앱 초기화
app = Flask(__name__)

# 2. CORS 활성화
CORS(app)

# 3. 블루프린트 등록
# URL 접두사 /api로 모든 라우트를 등록합니다.
app.register_blueprint(api, url_prefix='/api')

# --- 앱 실행 ---
if __name__ == '__main__':
    # 외부에서 접근 가능하도록 host='0.0.0.0' 설정
    app.run(debug=True, host='0.0.0.0', port=5000)
