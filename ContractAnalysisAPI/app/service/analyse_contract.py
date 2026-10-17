from app.service.prompt import CONTRACT_ANALYSIS_PROMPT
from app.config import GEMINI_API_KEY
import json
from app.models import ClauseAnalysis, RiskFlag, AnalysisResult
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

async def analyse_contract(contract_id: str, text_content:str):
    prompt= CONTRACT_ANALYSIS_PROMPT.format(contract_text=text_content)

    response = await client.aio.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=4096,
            response_mime_type="application/json" # Forces Gemini to return valid JSON
        )
    )
     
    analysis_data = json.loads(response.text)

    key_clauses = [
        ClauseAnalysis(**clause)
        for clause in analysis_data.get("key_clauses", [])
    ]
    risk_flags = [
        RiskFlag(**risk)
        for risk in analysis_data.get("risk_flags", [])
    ]
    result = AnalysisResult(
        contract_id=contract_id,
        summary = analysis_data.get("summary", ""),
        contract_type=analysis_data.get("contract_type", "Unknown"),
        key_clauses=key_clauses,
        risk_flags=risk_flags,
        overall_risk_level=analysis_data.get("overall_risk_level", "low"),
        recommendations=analysis_data.get("recommendations", []),
    )

    return result