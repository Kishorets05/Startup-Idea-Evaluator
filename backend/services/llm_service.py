"""
LLM Service - Handles communication with Groq API
Ensures structured JSON output with prompt guardrails
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the backend directory
# __file__ is in services/llm_service.py, so parent.parent is backend/
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Compatibility patch for groq/httpx issue
try:
    import httpx
    # Patch httpx.Client to handle proxies parameter if needed
    _original_init = httpx.Client.__init__
    def _patched_init(self, *args, **kwargs):
        # Remove 'proxies' if it exists and httpx version doesn't support it
        if 'proxies' in kwargs:
            # Convert proxies to transport if needed for newer httpx
            proxies_val = kwargs.pop('proxies', None)
            if proxies_val and hasattr(httpx, 'Proxy'):
                # Handle proxies differently for newer httpx versions
                pass
        return _original_init(self, *args, **kwargs)
    
    # Only patch if the version is problematic
    if hasattr(httpx, '__version__') and int(httpx.__version__.split('.')[0]) >= 0:
        try:
            httpx.Client.__init__ = _patched_init
        except:
            pass
except:
    pass

from groq import Groq


class LLMService:
    """Service for interacting with Groq LLM API"""
    
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please check backend/.env file.")
        
        self.client = Groq(api_key=api_key)
        # Updated to use available model (llama-3.1-70b-versatile was decommissioned)
        # Try models in order of preference with fallback
        self.models_to_try = [
            "llama-3.1-8b-instant",      # Fast, commonly available
            "llama-3.3-70b-versatile",   # Newer 70B model
            "llama-3.1-405b-reasoning",  # Large reasoning model
            "mixtral-8x7b-32768"        # Alternative model
        ]
        self.model = self.models_to_try[0]  # Default to first model
    
    def _get_evaluation_prompt(self, idea_text: str) -> str:
        """
        Constructs a structured prompt with guardrails to ensure JSON output
        """
        prompt = f"""You are an expert startup evaluator and business analyst. Analyze the following startup idea and provide a comprehensive evaluation.

STARTUP IDEA:
{idea_text}

EVALUATION CRITERIA - STRICT FEASIBILITY SCORING:

HIGH FEASIBILITY (75-95) - ONLY if ALL criteria met:
- Solves a REAL, EXISTING problem faced today
- Has a CLEARLY DEFINED target user or customer (not "everyone")
- Uses CURRENTLY AVAILABLE and PROVEN technology
- Has a REALISTIC MVP path within 6-12 months
- Does NOT promise guaranteed outcomes
- Has LOW ethical, legal, and regulatory risk

LOW FEASIBILITY (10-35) - If ANY criteria met:
- Claims scientifically IMPOSSIBLE or unproven capabilities (mind reading, exact exam prediction, guaranteed profits, future prediction)
- Promises guaranteed success or exact outcomes
- Is vague, abstract, or lacks a concrete execution plan
- Enables or encourages cheating, manipulation, or unethical behavior
- Has no realistic MVP or validation path

IMPORTANT RULES:
- Competition does NOT reduce feasibility; it only affects differentiation
- Buzzwords like "AI", "blockchain", or "quantum" must NOT increase scores unless tied to clear implementation
- If an idea violates scientific, ethical, or legal constraints, cap the score below 40 regardless of other strengths
- Evaluate ideas strictly using these rules

INSTRUCTIONS:
1. Analyze the idea thoroughly across all required dimensions
2. PRIORITIZE PRACTICAL FEASIBILITY over innovation buzzwords
3. Be CRITICAL and REALISTIC - if the idea is technically impossible, clearly state this
4. CRITICAL: Ideas that claim to "read human thoughts" or "read minds" are SCIENTIFICALLY IMPOSSIBLE and should score 15-20. Current brain-computer interfaces can detect basic signals but CANNOT decode specific thoughts or read minds in real-time.
5. CRITICAL: Ideas that claim to "predict the future" (career success, financial growth, life happiness, life outcomes) are IMPOSSIBLE and should score 0-30. The future cannot be predicted with certainty.
6. CRITICAL: Ideas using astrology, horoscopes, birth charts, or fortune telling are PSEUDOSCIENCE and should score 0-30. These are not scientifically valid.
7. CRITICAL: Using "quantum computing", "blockchain", or "AI" for impossible tasks (predictions, mind reading) does NOT make them possible. These are buzzwords misapplied to impossible tasks.
8. CRITICAL: Analyzing brain signals, facial expressions, voice tone, or social media CANNOT read thoughts or predict future outcomes. These can only provide current insights, not mind reading or future predictions.
9. Focus on whether the idea can be built TODAY with EXISTING technology in 6-12 months
10. Provide ONLY valid JSON output - no markdown, no extra text
11. Do NOT hallucinate metrics or data - use reasonable estimates based on the idea description
12. Be objective and balanced - penalize unrealistic/impossible ideas appropriately
13. Ensure all fields are filled with meaningful content
14. If the idea requires technology that doesn't exist (e.g., reading thoughts, reading dreams, time travel, teleportation), mark technical feasibility as very low

REQUIRED OUTPUT FORMAT (JSON only):
{{
  "executive_summary": "A 2-3 sentence overview of the startup idea and its potential",
  "problem_statement": "Clear description of the problem being solved",
  "target_users": "Description of the target customer segment",
  "market_potential": "Assessment of market size and opportunity",
  "technical_feasibility": "Analysis of technical requirements and feasibility",
  "innovation_uniqueness": "Evaluation of how innovative and unique the idea is",
  "risks_challenges": "Key risks and challenges the startup may face",
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"],
  "improvement_suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  "final_recommendation": "Overall recommendation and next steps",
  "feasibility_score": 0
}}

IMPORTANT:
- Return ONLY the JSON object, no markdown formatting
- feasibility_score should be an integer between 0-100 (you will provide initial estimate)
- Be ACCURATE and STRICT with the score - FOLLOW THESE RULES EXACTLY:
  * 10-35: LOW FEASIBILITY - Ideas that:
    - Claim scientifically impossible capabilities (mind reading, exact exam prediction, guaranteed profits, future prediction)
    - Promise guaranteed success or exact outcomes
    - Are vague, abstract, or lack concrete execution plan
    - Enable cheating, manipulation, or unethical behavior
    - Have no realistic MVP or validation path
  * 36-50: Moderate feasibility - Some issues but partially feasible
  * 51-74: Good feasibility - Solves real problem but may have some limitations
  * 75-95: HIGH FEASIBILITY - ONLY if ALL criteria met:
    - Solves real, existing problem
    - Clear target user
    - Uses proven technology
    - Realistic 6-12 month MVP path
    - No guaranteed promises
    - Low ethical/legal risk
  * 96-100: Reserved for exceptional cases only
- CRITICAL RULES:
  * Ideas claiming impossible capabilities (mind reading, exact exam prediction, guaranteed profits, future prediction) MUST score 10-35
  * Ideas promising guaranteed success or exact outcomes MUST score 10-35
  * Ideas that enable cheating, manipulation, or unethical behavior MUST score 10-35
  * Ideas that violate scientific, ethical, or legal constraints MUST be capped below 40
  * Competition does NOT reduce feasibility - only affects differentiation
  * Buzzwords ("AI", "blockchain", "quantum") do NOT increase scores unless tied to clear implementation
  * Standard business software (attendance, HR, payroll, CRM, SaaS) using proven tech should score 75-90
  * Ideas with real problem, clear target, proven tech, 6-12 month MVP path should score 75-95
  * Be CONSISTENT - same idea should receive nearly the same score every time
- All string fields should be 1-3 sentences
- Arrays should have 3 items each
- Be specific and actionable in your analysis
- If the idea is impossible (e.g., reading dreams, mind control, time travel, predicting future), give a low score (0-30) and explain why in technical_feasibility
- If the idea uses standard, proven technology (mobile/web apps, standard APIs), clearly state this in technical_feasibility and give appropriate scores

Now provide the JSON evaluation:"""
        
        return prompt
    
    def evaluate_idea(self, idea_text: str) -> dict:
        """
        Evaluates a startup idea using LLM and returns structured JSON
        
        Args:
            idea_text: The startup idea description
            
        Returns:
            dict: Structured evaluation with all required fields
        """
        try:
            prompt = self._get_evaluation_prompt(idea_text)
            
            # Try models in order until one works
            last_error = None
            for model in self.models_to_try:
                try:
                    # Call Groq API
                    # Use low temperature (0.1) for more deterministic, consistent results
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional startup evaluator. Always respond with valid JSON only, no markdown formatting."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.1,  # Low temperature for consistency (was 0.7)
                        max_tokens=2000,
                        response_format={"type": "json_object"}  # Force JSON output
                    )
                    # If successful, update default model and break
                    self.model = model
                    break
                except Exception as e:
                    last_error = e
                    # If model not found, try next one
                    if "model" in str(e).lower() or "decommissioned" in str(e).lower():
                        continue
                    else:
                        # Other error, re-raise
                        raise
            else:
                # All models failed
                raise Exception(f"All models failed. Last error: {str(last_error)}")
            
            # Extract and parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Clean response (remove markdown code blocks if any)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            evaluation = json.loads(response_text)
            
            # Validate required fields
            required_fields = [
                "executive_summary", "problem_statement", "target_users",
                "market_potential", "technical_feasibility", "innovation_uniqueness",
                "risks_challenges", "strengths", "weaknesses",
                "improvement_suggestions", "final_recommendation"
            ]
            
            for field in required_fields:
                if field not in evaluation:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure arrays are lists and handle type conversions
            def ensure_list(value, default=[]):
                """Convert value to list if it's not already a list"""
                if value is None:
                    return default
                if isinstance(value, list):
                    return value
                if isinstance(value, str):
                    # Try to parse as JSON array if it's a string representation
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list):
                            return parsed
                    except:
                        pass
                    # If it's a plain string, return as single-item list
                    return [value] if value.strip() else default
                # For other types, convert to string and wrap in list
                return [str(value)]
            
            evaluation["strengths"] = ensure_list(evaluation.get("strengths"), [])
            evaluation["weaknesses"] = ensure_list(evaluation.get("weaknesses"), [])
            evaluation["improvement_suggestions"] = ensure_list(evaluation.get("improvement_suggestions"), [])
            
            # Ensure all string fields are actually strings
            string_fields = [
                "executive_summary", "problem_statement", "target_users",
                "market_potential", "technical_feasibility", "innovation_uniqueness",
                "risks_challenges", "final_recommendation"
            ]
            for field in string_fields:
                value = evaluation.get(field)
                if value is not None and not isinstance(value, str):
                    evaluation[field] = str(value)
            
            return evaluation
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error evaluating idea with LLM: {str(e)}")

