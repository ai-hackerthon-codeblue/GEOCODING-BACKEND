import json
import random
from google.genai import types
from .config import client, GEMINI_MODEL

def create_analysis_prompt(path1_data: str, path2_data: str) -> str:
    """Gemini에게 보낼 분석 프롬프트를 생성합니다."""
    path1_summary = path1_data[:300] + "..." if len(path1_data) > 300 else path1_data
    path2_summary = path2_data[:300] + "..." if len(path2_data) > 300 else path2_data

    return f"""
당신은 사용자의 경로 기억력과 공간 지각 능력을 정밀하게 분석하는 AI 전문가입니다.

당신의 핵심 임무는 '경로 1(목적지로 가는 길)'과 '경로 2(출발지로 돌아오는 길)'의 GPS 좌표 데이터를 비교하여, 사용자가 얼마나 정확하게 왔던 길을 되돌아갔는지를 평가하는 것입니다.

### 분석 지침

1.  **경로 역순 비교**: '경로 2'가 '경로 1'의 좌표 순서를 얼마나 정확하게 역으로 따라가는지 분석합니다. 경로의 전체적인 형태, 길이, 방향성, 주요 분기점에서의 선택이 일치하는지를 종합적으로 고려해야 합니다.

2.  **analysis_summary (분석 요약) 작성**:
    * **매우 유사할 경우 (오차율 0-15%)**: "복귀 경로는 최초 경로를 매우 정확하게 역순으로 따라 이동했습니다. 특히 주요 변곡점에서도 높은 일치율을 보여 뛰어난 공간 기억력과 방향 감각을 보여줍니다." 와 같이 긍정적인 평가를 한국어로 작성합니다.
    * **부분적으로 다를 경우 (오차율 15-50%)**: "초반 경로는 대체로 일치했으나, 특정 지점부터 경로가 달라지기 시작했습니다. 되돌아오는 길에 일부 구간에서 다른 길을 택했지만 전체적인 방향성은 유지했습니다." 와 같이 구체적인 이탈 지점이나 경향을 언급하며 한국어로 작성합니다.
    * **완전히 다를 경우 (오차율 50% 이상)**: "복귀 경로는 최초 경로와 지리적으로 전혀 다른 경로를 따랐습니다. 이는 경로를 기억하기보다는 새로운 길을 탐색하여 복귀한 것으로 분석됩니다." 와 같이 명확한 차이점을 한국어로 작성합니다.

3.  **error_rate (오차율) 계산**:
    * 두 경로의 불일치 정도를 `0.0`에서 `100.0` 사이의 실수(float) 값으로 계산합니다.
    * `0.0`은 '경로 2'가 '경로 1'을 완벽하게 역순으로 따라간 이상적인 경우입니다.
    * `100.0`은 두 경로가 전혀 관련 없는, 완전히 다른 경로인 경우입니다.

### 출력 형식

**결과는 반드시 아래의 JSON 형식으로만 응답해야 합니다.** 다른 설명이나 텍스트, Markdown 코드 블록 표시 없이 순수한 JSON 객체 하나만 반환하십시오.

{{
  "analysis_summary": "<string_detailed_analysis_in_korean>",
  "error_rate": <float_error_rate_between_0_and_100>
}}

### 실제 분석 데이터
경로 1: {path1_data}
경로 2: {path2_data}
"""

def analyze_path_similarity(path1_data_str: str, path2_data_str: str) -> dict:
    """Gemini API를 사용하여 경로 유사도를 분석하거나, 실패 시 Mock 데이터를 생성합니다."""
    if not client:
        print("Gemini 클라이언트가 초기화되지 않았습니다. Mock 데이터로 대체합니다.")
        # TODO: Replace with actual geocoding distance calculation
        return {
            "error_rate": round(random.uniform(5.0, 20.0), 2),
            "analysis_summary": "Gemini 클라이언트 미초기화. 임시 분석 요약을 제공합니다. (실제 분석 아님)"
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

        gemini_analysis = json.loads(analysis_json_str)

        # TODO: Replace with actual geocoding distance calculation
        # Placeholder for error_rate calculation
        calculated_error_rate = round(random.uniform(5.0, 20.0), 2)

        return {
            "error_rate": calculated_error_rate,
            "analysis_summary": gemini_analysis.get("analysis_summary", "분석 요약 없음.")
        }

    except Exception as e:
        print(f"Gemini 분석 오류 발생: {e}. Mock 데이터로 대체합니다.")
        # TODO: Replace with actual geocoding distance calculation
        return {
            "error_rate": round(random.uniform(5.0, 20.0), 2),
            "analysis_summary": f"분석 오류: {e}. 임시 분석 요약을 제공합니다. (실제 분석 아님)"
        }
