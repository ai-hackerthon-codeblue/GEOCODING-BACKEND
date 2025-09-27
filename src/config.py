# src/config.py

import os
import firebase_admin
from firebase_admin import credentials
from google import genai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# --- Firebase Admin SDK 초기화 ---
try:
    FIREBASE_CRED_PATH = os.environ.get("FIREBASE_CRED_PATH")
    if not FIREBASE_CRED_PATH or not os.path.exists(FIREBASE_CRED_PATH):
        raise FileNotFoundError(f"Firebase key file not found at: {FIREBASE_CRED_PATH}")

    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ.get("FIREBASE_DATABASE_URL")
    })
    print("Firebase Admin SDK 초기화 완료.")
except Exception as e:
    print(f"Firebase 초기화 오류: {e}")
    # 프로덕션 환경에서는 앱 실행을 중지해야 합니다.

# --- Gemini API 클라이언트 초기화 ---
try:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

    # genai.configure(api_key=GEMINI_API_KEY)
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Gemini API 클라이언트 초기화 완료.")
except Exception as e:
    print(f"Gemini API 초기화 오류: {e}")
    client = None # API 키가 없어도 앱이 실행되도록 None으로 설정

# --- Gemini 분석 프롬프트 및 설정 ---
GEMINI_MODEL = 'gemini-1.5-flash'
