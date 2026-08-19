"""
gemini_helper.py

Wraps calls to the Gemini API. Used ONLY for generating human-friendly
explanations and resource suggestions for a topic that the graph has
ALREADY placed in the correct order. Gemini never decides ordering.

Requires: pip install google-generativeai
Set your API key as an environment variable: GEMINI_API_KEY
(Get one free from https://aistudio.google.com/app/apikey)
"""

import os

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

API_KEY = os.environ.get("GEMINI_API_KEY", "")

if GENAI_AVAILABLE and API_KEY:
    genai.configure(api_key=API_KEY)
    _model = genai.GenerativeModel("gemini-3.6-flash")
else:
    _model = None


def get_topic_explanation(topic_title: str) -> dict:
    """
    Returns a dict: {"explanation": str, "resource": str}
    Falls back to a placeholder if no API key is set, so the app still
    runs end-to-end for demo purposes without requiring a key.
    """
    if _model is None:
        return {
            "explanation": (
                f"[Demo mode - no API key set] {topic_title} is an important "
                f"step on your learning path. Set GEMINI_API_KEY to get a real "
                f"AI-generated explanation here."
            ),
            "resource": "Search for a free course on this topic on YouTube or freeCodeCamp.",
        }

    prompt = f"""Explain the topic "{topic_title}" to a beginner learner in 3-4 sentences.
Then, on a new line starting with "RESOURCE:", suggest ONE specific free online
resource (course, article, or documentation) where they can learn it.
Keep it concise and encouraging."""

    try:
        response = _model.generate_content(prompt)
        text = response.text.strip()

        if "RESOURCE:" in text:
            explanation, resource = text.split("RESOURCE:", 1)
        else:
            explanation, resource = text, "Search for a free course on this topic online."

        return {
            "explanation": explanation.strip(),
            "resource": resource.strip(),
        }
    except Exception as e:
        return {
            "explanation": f"Could not generate explanation ({e}).",
            "resource": "N/A",
        }


def generate_dynamic_quiz_feedback(topic_title: str, correct: bool) -> str:
    """Optional: short encouraging/corrective feedback after a quiz question."""
    if _model is None:
        return "Nice!" if correct else "No worries — this topic will be added to your path."

    prompt = (
        f"In one short encouraging sentence, respond to a learner who just "
        f"{'answered correctly' if correct else 'answered incorrectly'} "
        f"a question about '{topic_title}'."
    )
    try:
        response = _model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Nice!" if correct else "No worries — this topic will be added to your path."
