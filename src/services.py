# src/services.py

import json
import random
from google.genai import types
from .config import client, GEMINI_MODEL

def create_analysis_prompt(path1_data: str, path2_data: str) -> str:
    """Gemini에게 보낼 분석 프롬프트를 생성합니다."""
    path1_summary = path1_data[:300] + "..." if len(path1_data) > 300 else path1_data
    path2_summary = path2_data[:300] + "..." if len(path2_data) > 300 else path2_data

    return f"""
당신은 공간 지각 능력 평가 전문가입니다.
'경로 1'은 갈 때의 경로 좌표 리스트이며, '경로 2'는 되돌아올 때의 경로 좌표 리스트입니다.
두 경로의 **지리적 유사도**를 분석하여 **'복귀 경로 오차율'**을 계산하고 분석 요약을 제공해야 합니다.
오차율은 0%에 가까울수록 정확하게 복귀한 것을 의미하며, 두 경로의 지리적 거리 차이 및 이탈 정도를 종합적으로 고려해야 합니다.

### 입력 데이터 형식
경로 좌표는 위도(latitude)와 경도(longitude) 쌍의 리스트로 제공됩니다.

### 요구 사항
1.  **결과는 반드시 아래의 JSON 형식으로만 응답**하십시오. 다른 텍스트나 설명 없이 JSON 객체만 반환해야 합니다.
2.  `error_rate`는 오차율 (float, 소수점 둘째 자리까지) 입니다.
3.  `analysis_summary`는 주요 오차 발생 지점 또는 전반적인 수행 능력에 대한 **한국어 요약**입니다.

### 출력 JSON 형식
{{
  "error_rate": <float_value>,
  "analysis_summary": "<string_summary_in_korean>"
}}

### 실제 데이터 (JSON String)
경로 1: {path1_data}
경로 2: {path2_data}
"""

def analyze_path_similarity(path1_data_str: str, path2_data_str: str) -> dict:
    """Gemini API를 사용하여 경로 유사도를 분석하거나, 실패 시 Mock 데이터를 생성합니다."""
    if not client:
        print("Gemini 클라이언트가 초기화되지 않았습니다. Mock 데이터로 대체합니다.")
        return {
            "error_rate": round(random.uniform(10.0, 50.0), 2),
            "analysis_summary": "Gemini 클라이언트 미초기화. 임시 오차율을 제공합니다. (실제 분석 아님)"
        }

    try:
        prompt = create_analysis_prompt(path1_data_str, path2_data_str)
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        analysis_json_str = response.text.strip()
        # 응답이 Markdown 코드 블록으로 감싸져 오는 경우, 순수 JSON만 추출
        if analysis_json_str.startswith("```json"):
            analysis_json_str = analysis_json_str[7:-3].strip()
        return json.loads(analysis_json_str)

    except Exception as e:
        print(f"Gemini 분석 오류 발생: {e}. Mock 데이터로 대체합니다.")
        return {
            "error_rate": round(random.uniform(10.0, 50.0), 2),
            "analysis_summary": f"분석 오류: {e}. 임시 오차율을 제공합니다. (실제 분석 아님)"
        }
