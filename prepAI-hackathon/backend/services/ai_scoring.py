
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Attempt to load Gemini
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("Warning: google-generativeai not installed.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = None
if HAS_GEMINI and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        print("Gemini API Configured Successfully.")
    except Exception as e:
        print(f"Error configuring Gemini: {e}")

def score_answer(user_answer: str, expected_answer: str) -> dict:
    """
    Scores the user answer.
    If Gemini API is available, uses it for intelligent grading.
    Otherwise, falls back to basic keyword matching.
    """
    
    # --- GEMINI AI PATH ---
    if model:
        try:
            prompt = f"""
            You are an expert technical interviewer. Evaluate the candidate's answer for accuracy, depth, and communication.
            
            **Context/Task:** {expected_answer}
            **Candidate Answer:** {user_answer}
            
            If the answer is irrelevant or empty, give 0.
            
            Return ONLY a valid JSON object (no markdown formatting) with these integer keys (0-100) and a string feedback:
            {{
                "technical_score": <int>,
                "behavioral_score": <int>,
                "comm_score": <int>,
                "readiness_score": <int>,
                "feedback": "<short constructive feedback, max 2 sentences>"
            }}
            """
            
            response = model.generate_content(prompt)
            result_text = response.text
            
            # Clean up potential markdown code blocks ```json ... ```
            clean_json = re.sub(r'```json\s*|\s*```', '', result_text).strip()
            
            scores = json.loads(clean_json)
            
            # Ensure all keys exist
            return {
                "technical_score": scores.get("technical_score", 0),
                "behavioral_score": scores.get("behavioral_score", 0),
                "comm_score": scores.get("comm_score", 0),
                "readiness_score": scores.get("readiness_score", 0),
                "feedback": scores.get("feedback", "No feedback provided.")
            }
            
        except Exception as e:
            print(f"Gemini Scoring Failed: {e}. Falling back to keyword matching.")
            # Fall through to default logic

    # --- FALLBACK LOGIC (Keyword Matching) ---
    if not expected_answer or len(expected_answer.split()) == 0:
        return {
            "technical_score": 0,
            "behavioral_score": 70,
            "comm_score": 68,
            "readiness_score": 30,
            "feedback": "No context provided to score against."
        }

    user_words = set(user_answer.lower().split())
    expected_words = set(expected_answer.lower().split())
    
    if not expected_words:
        similarity = 0
    else:
        similarity = len(user_words & expected_words) / len(expected_words)
    
    if similarity > 1: similarity = 1
    
    # Bonus for effort
    if len(user_answer) > 20 and similarity < 0.2:
        similarity += 0.2

    technical = int(similarity * 100)
    behavioral = 85 
    comm = 90
    readiness = int(0.5 * technical + 0.3 * behavioral + 0.2 * comm)
    
    return {
        "technical_score": technical,
        "behavioral_score": behavioral,
        "comm_score": comm,
        "readiness_score": readiness,
        "feedback": "Good effort! (Graded via Keyword Matching - Add Gemini Key for AI grading)"
    }
