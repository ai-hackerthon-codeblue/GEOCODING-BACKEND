# src/routes.py

import json
from flask import Blueprint, request, jsonify
from firebase_admin import db

from .services import analyze_path_similarity

api = Blueprint('api', __name__)

@api.route('/trainings', methods=['POST'])
def save_training_and_analyze():
    """
    1. React로부터 훈련 데이터를 수신합니다.
    2. Firebase에 원본 데이터를 저장합니다.
    3. Gemini API를 호출하여 경로 유사도를 분석합니다.
    4. 분석 결과를 Firebase에 업데이트합니다.
    """
    data = request.get_json()

    required_fields = ['time_taken_seconds', 'path_to_destination', 'path_back_to_start']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "필수 훈련 데이터 필드가 누락되었습니다."}), 400

    path1_data_str = json.dumps(data['path_to_destination'])
    path2_data_str = json.dumps(data['path_back_to_start'])

    ref = db.reference('/trainings')
    initial_data = {
        **data,
        'timestamp': {".sv": "timestamp"},
        'status': 'analyzing',
        'analysis_data': {}
    }
    new_training_ref = ref.push(initial_data)
    training_id = new_training_ref.key

    analysis_result = analyze_path_similarity(path1_data_str, path2_data_str)

    update_ref = db.reference(f'/trainings/{training_id}')
    update_ref.update({
        'analysis_data': analysis_result,
        'status': 'completed'
    })

    return jsonify({
        "message": "훈련 기록 저장 및 분석 완료",
        "id": training_id,
        "analysis_data": analysis_result
    }), 201

@api.route('/trainings/<training_id>', methods=['GET'])
def get_training_result(training_id):
    """
    특정 훈련 ID에 해당하는 전체 기록을 Firebase에서 조회하여 반환합니다.
    """
    ref = db.reference(f'/trainings/{training_id}')
    training_data = ref.get()

    if training_data:
        return jsonify(training_data), 200
    else:
        return jsonify({"message": "해당 ID의 훈련 기록을 찾을 수 없습니다."}), 404
