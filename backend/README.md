# Startup Evaluator - Backend

Flask REST API backend for the Startup Evaluator application.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Groq API key

3. **Run the server:**
```bash
python app.py
```

The API will run on `http://localhost:5000`

## API Endpoints

### `POST /evaluate`
Evaluates a startup idea and returns structured analysis.

**Request:**
```json
{
  "idea": "Your startup idea description here"
}
```

**Response:**
```json
{
  "success": true,
  "evaluation": {
    "executive_summary": "...",
    "problem_statement": "...",
    "target_users": "...",
    "market_potential": "...",
    "technical_feasibility": "...",
    "innovation_uniqueness": "...",
    "risks_challenges": "...",
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."],
    "improvement_suggestions": ["...", "..."],
    "final_recommendation": "...",
    "feasibility_score": 75
  }
}
```

### `POST /generate-pdf`
Generates a PDF report from evaluation data.

**Request:**
```json
{
  "evaluation": { ... }
}
```

### `GET /health`
Health check endpoint.

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── services/
│   ├── llm_service.py     # Groq API integration
│   ├── scoring.py         # Feasibility scoring logic
│   └── pdf_generator.py   # PDF report generation
├── utils/
│   └── error_handler.py   # Error handling utilities
├── reports/               # Generated PDF reports
└── requirements.txt       # Python dependencies
```

