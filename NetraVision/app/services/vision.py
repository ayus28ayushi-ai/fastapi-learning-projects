import base64
from google import genai
import json
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

CROP_ANALYSIS_PROMPT = """
    You are an expert agricultural scientist specializing in crop disease detection.
Analyze this image of a crop/plant and provide a detailed disease assessment.

Provide your analysis as a JSON object with exactly this structure:

{
"crop_detected": "Name of the crop or plant visible in the image",
"severity": "healthy" or "mild" or "moderate" or "severe" or "critical",
"diseases": [
        {
            "name": "Disease name",
            "confidence": 0.0 to 1.0,
            "description": "Brief description of the disease and visible symptoms"
        }
    ],
"treatments": [
        {
            "treatment_name": "Name of treatment",
            "treatment_type": "organic" or "chemical" or "preventive",
            "instructions": "Step by step treatment instructions",
            "urgency": "immediate" or "within_week" or "seasonal"
        }
    ],
    "overall_health": "One sentence summary of plant health",
    "additional_notes": "Any other observations or recommendations"
}
"""

async def analyze_image(image_content: bytes, content_type: str):
    interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {
            "type": "text", 
            "text": CROP_ANALYSIS_PROMPT
        },
        {
            "type": "image",
            "data": base64.b64encode(image_content).decode('utf-8'),
            "mime_type": content_type
        }
    ]
    )

    # cleaning up to prevent value error
    if not interaction.output_text:
        raise ValueError("Model returned an empty response, check whether the image is correct.")
    raw_text = interaction.output_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

    return json.loads(raw_text)  # parses a json formatted string and converts to correponding python data structure