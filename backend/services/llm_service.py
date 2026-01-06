"""
LLM Service - Handles communication with Groq API
Ensures structured JSON output with strict feasibility scoring
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load .env only for local development
load_dotenv()


class LLMService:
    """Service for interacting with Groq LLM API"""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it as an environment variable or Streamlit secret."
            )

        self.client = Groq(api_key=api_key)

        self.models_to_try = [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "llama-3.1-405b-reasoning",
            "mixtral-8x7b-32768"
        ]

        self.model = self.models_to_try[0]

    def _get_evaluation_prompt(self, idea_text: str) -> str:
        return f"""
You are an expert startup evaluator and business analyst.

STARTUP IDEA:
{idea_text}

STRICT FEASIBILITY SCORING RULES:

HIGH (75-95):
- Real problem
- Clear target users
- Proven technology
- 6–12 month MVP
- No guaranteed promises
- Low legal/ethical risk

LOW (10-35):
- Impossible tech (mind reading, future prediction)
- Guaranteed success claims
- Astrology / pseudoscience
- Cheating or unethical ideas
- No realistic MVP

IMPORTANT:
- Competition does NOT reduce feasibility
- Buzzwords do NOT increase score
- Impossible ideas MUST score below 40
- Same idea should produce nearly same score every time

RETURN ONLY VALID JSON (NO MARKDOWN):

{{
  "executive_summary": "",
  "problem_statement": "",
  "target_users": "",
  "market_potential": "",
  "technical_feasibility": "",
  "innovation_uniqueness": "",
  "risks_challenges": "",
  "strengths": ["", "", ""],
  "weaknesses": ["", "", ""],
  "improvement_suggestions": ["", "", ""],
  "final_recommendation": "",
  "feasibility_score": 0
}}
"""

    def evaluate_idea(self, idea_text: str) -> dict:
        prompt = self._get_evaluation_prompt(idea_text)

        last_error = None
        response = None

        for model in self.models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional startup evaluator. Respond with JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=2000,
                    response_format={"type": "json_object"}
                )
                self.model = model
                break
            except Exception as e:
                last_error = e
                continue

        if response is None:
            raise Exception(f"All models failed. Last error: {last_error}")

        evaluation = json.loads(response.choices[0].message.content)

        evaluation["strengths"] = list(evaluation.get("strengths", []))[:3]
        evaluation["weaknesses"] = list(evaluation.get("weaknesses", []))[:3]
        evaluation["improvement_suggestions"] = list(
            evaluation.get("improvement_suggestions", [])
        )[:3]

        return evaluation
