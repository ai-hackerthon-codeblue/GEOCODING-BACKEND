# AI-Hackerthon-CodeBlue Geocoding Backend

## 개요

본 프로젝트는 AI 해커톤 CodeBlue의 지오코딩 백엔드 서버입니다. 사용자의 이동 경로를 기록하고, Gemini API를 활용하여 출발 경로와 복귀 경로의 유사도를 분석하여 '복귀 경로 오차율'을 계산하고 분석 요약을 제공합니다.

## 주요 기능

* **경로 데이터 저장**: 사용자의 출발 및 복귀 경로 좌표, 소요 시간 등 훈련 데이터를 Firebase Realtime Database에 저장합니다.
* **경로 유사도 분석**: Google Gemini API를 사용하여 두 경로의 지리적 유사도를 분석하고, '복귀 경로 오차율'과 분석 요약을 생성합니다.
* **분석 결과 조회**: 저장된 훈련 기록 및 분석 결과를 ID를 통해 조회할 수 있습니다.

## 프로젝트 구조

* **app.py**: Flask 애플리케이션을 실행하는 메인 파일입니다.
* **src/config.py**: Firebase 및 Gemini API 클라이언트를 초기화하고 관련 설정을 관리합니다.
* **src/routes.py**: API 엔드포인트를 정의하고 요청을 처리합니다.
* **src/services.py**: Gemini API를 호출하여 경로 유사도를 분석하는 비즈니스 로직을 포함합니다.
* **.env**: Firebase 및 Gemini API 키 등 환경 변수를 저장하는 파일입니다.
* **service_keys/serviceAccountKey.json**: Firebase Admin SDK 인증을 위한 서비스 계정 키 파일입니다.

## API 엔드포인트

### `POST /api/trainings`

* **설명**: 새로운 훈련 기록을 저장하고 경로 유사도 분석을 요청합니다.
* **요청 본문 (JSON)**:
    ```json
    {
      "time_taken_seconds": 600,
      "path_to_destination": [
        {"latitude": 37.5665, "longitude": 126.9780},
        ...
      ],
      "path_back_to_start": [
        {"latitude": 37.5665, "longitude": 126.9780},
        ...
      ]
    }
    ```
* **성공 응답 (201 Created)**:
    ```json
    {
      "message": "훈련 기록 저장 및 분석 완료",
      "id": "-Nq...w",
      "analysis_data": {
        "error_rate": 15.78,
        "analysis_summary": "전반적으로 복귀 경로를 잘 유지했으나, 특정 구간에서 약 50m의 이탈이 발생했습니다."
      }
    }
    ```

### `GET /api/trainings/<training_id>`

* **설명**: 특정 훈련 ID에 해당하는 전체 기록을 조회합니다.
* **URL 매개변수**: `training_id` (Firebase에서 생성된 고유 ID)
* **성공 응답 (200 OK)**:
    ```json
    {
      "time_taken_seconds": 600,
      "path_to_destination": [...],
      "path_back_to_start": [...],
      "timestamp": 1678886400000,
      "status": "completed",
      "analysis_data": {
        "error_rate": 15.78,
        "analysis_summary": "..."
      }
    }
    ```
* **실패 응답 (404 Not Found)**:
    ```json
    {
      "message": "해당 ID의 훈련 기록을 찾을 수 없습니다."
    }
    ```

## 시작 가이드

1.  **Firebase 설정**:
    * Firebase 프로젝트를 생성하고 Realtime Database를 활성화합니다.
    * Firebase Admin SDK를 위한 서비스 계정 키(`serviceAccountKey.json`)를 발급받아 `service_keys` 디렉토리에 저장합니다.

2.  **Gemini API 설정**:
    * Google AI Studio에서 Gemini API 키를 발급받습니다.

3.  **환경 변수 설정**:
    * `.env` 파일을 생성하고 아래와 같이 Firebase 및 Gemini 정보를 입력합니다.
        ```
        FIREBASE_CRED_PATH=service_keys/serviceAccountKey.json
        FIREBASE_DATABASE_URL=https://<your-firebase-project-id>.firebaseio.com
        GEMINI_API_KEY=<your-gemini-api-key>
        ```

4.  **의존성 설치 및 실행**:
    ```bash
    pip install Flask firebase-admin python-dotenv google-generativeai flask-cors
    python app.py
    ```