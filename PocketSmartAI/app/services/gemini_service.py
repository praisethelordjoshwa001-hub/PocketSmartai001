import json
from google import genai
from google.genai import types
from app.config import settings

def _client():
    if not settings.gemini_api_key or not settings.ai_enabled: return None
    return genai.Client(api_key=settings.gemini_api_key)

def _extract_json(text):
    if not text: return None
    text = text.strip().replace("```json", "").replace("```", "").strip()
    try: return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try: return json.loads(text[start:end+1])
            except json.JSONDecodeError: return None
    return None

SCHEMA = {"type":"object","properties":{
    "title":{"type":"string"},"summary":{"type":"string"},
    "tips":{"type":"array","items":{"type":"string"}},
    "recommendations":{"type":"array","items":{"type":"object","properties":{
        "name":{"type":"string"},"category":{"type":"string"},"estimated_price":{"type":"number"},
        "reason":{"type":"string"},"platform":{"type":"string"}},"required":["name","category","estimated_price","reason","platform"]}}},
    "required":["title","summary","tips","recommendations"]}

def generate_recommendation(planner, user_data, image_bytes=None, mime_type=None):
    client = _client()
    if not client: return None
    prompt = f"""You are PocketSmart AI, a budget-aware lifestyle recommendation assistant.
Planner: {planner}
User data:
{json.dumps(user_data, indent=2)}
Create practical recommendations that respect the total budget. Do not claim live prices or availability; prices are estimates.
Use Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO where sensible. For jewelry, use visible outfit colors/style from an uploaded image only as an input; do not identify the person.
Return only JSON matching the supplied schema."""
    contents = [prompt]
    if image_bytes and mime_type:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    try:
        response = client.models.generate_content(
            model=settings.gemini_model, contents=contents,
            config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=SCHEMA, temperature=0.4, max_output_tokens=2500)
        )
        return _extract_json(response.text)
    except Exception:
        return None
