"""
Startup Evaluator - Flask Backend
Main application entry point
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os
import hashlib
from services.llm_service import LLMService
from services.scoring import ScoringService
from services.pdf_generator import PDFGenerator
from utils.error_handler import handle_errors

# Load environment variables from backend/.env
backend_dir = Path(__file__).parent
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize services
llm_service = LLMService()
scoring_service = ScoringService()
pdf_generator = PDFGenerator()

# Cache for evaluations (in-memory, persists for server lifetime)
# Key: hash of normalized idea text, Value: full evaluation result
evaluation_cache = {}


def normalize_idea_text(idea_text: str) -> str:
    """
    Normalize idea text for consistent caching
    - Strip whitespace
    - Convert to lowercase
    - Remove extra spaces
    """
    return ' '.join(idea_text.strip().lower().split())


def get_cache_key(idea_text: str) -> str:
    """
    Generate a cache key from idea text
    Uses SHA256 hash for consistent key generation
    """
    normalized = normalize_idea_text(idea_text)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Startup Evaluator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health (GET) - Health check",
            "evaluate": "/evaluate (POST) - Evaluate startup idea",
            "generate_pdf": "/generate-pdf (POST) - Generate PDF report"
        },
        "note": "This is the API backend. Access the frontend at http://localhost:3000"
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Startup Evaluator API is running"})


@app.route('/evaluate', methods=['POST'])
def evaluate_startup():
    """
    Main evaluation endpoint
    Accepts startup idea text and returns structured evaluation
    Uses caching to ensure same idea always returns same result
    """
    try:
        # Validate input
        data = request.get_json()
        if not data or 'idea' not in data:
            return jsonify({
                "error": "Missing 'idea' field in request body"
            }), 400
        
        idea_text = data['idea'].strip()
        if not idea_text:
            return jsonify({
                "error": "Idea text cannot be empty"
            }), 400
        
        # Check cache first
        cache_key = get_cache_key(idea_text)
        if cache_key in evaluation_cache:
            # Return cached result
            cached_evaluation = evaluation_cache[cache_key]
            return jsonify({
                "success": True,
                "evaluation": cached_evaluation,
                "cached": True
            }), 200
        
        # Cache miss - perform evaluation
        # Get LLM evaluation
        evaluation = llm_service.evaluate_idea(idea_text)
        
        # Calculate feasibility score (pass idea_text for impossible idea detection)
        score = scoring_service.calculate_score(evaluation, idea_text)
        evaluation['feasibility_score'] = score
        
        # If score is very low, add explicit note about impossibility
        if score <= 10:
            if 'technical_feasibility' in evaluation:
                evaluation['technical_feasibility'] = (
                    "This idea is technically impossible with current or foreseeable technology. "
                    "The required technology does not exist and may not be possible. " +
                    evaluation.get('technical_feasibility', '')
                )
        
        # Get component scores for visualization
        component_scores = scoring_service.get_component_scores(evaluation)
        evaluation['component_scores'] = component_scores
        
        # Store in cache for future requests
        evaluation_cache[cache_key] = evaluation
        
        # Return structured response
        return jsonify({
            "success": True,
            "evaluation": evaluation,
            "cached": False
        }), 200
        
    except Exception as e:
        return handle_errors(e)


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Generate PDF report from evaluation
    """
    try:
        data = request.get_json()
        if not data or 'evaluation' not in data:
            return jsonify({
                "error": "Missing 'evaluation' field in request body"
            }), 400
        
        evaluation = data['evaluation']
        pdf_path = pdf_generator.generate_report(evaluation)
        
        # Return PDF as base64 or file path
        # For simplicity, we'll return the path and let frontend handle download
        return jsonify({
            "success": True,
            "pdf_path": pdf_path
        }), 200
        
    except Exception as e:
        return handle_errors(e)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

