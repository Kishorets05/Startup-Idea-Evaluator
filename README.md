# 🚀 Startup Evaluator

An AI-powered web application that evaluates startup ideas and provides comprehensive, structured analysis with visual analytics and downloadable PDF reports.

🌐 **Live Demo**: [https://startup-idea-evaluator-engine.streamlit.app/](https://startup-idea-evaluator-engine.streamlit.app/)

## 📋 Features

- **AI-Powered Analysis**: Uses Groq LLM to analyze startup ideas
- **Structured Evaluation**: 11 comprehensive evaluation sections
- **Strict Feasibility Scoring**: Accurate scoring algorithm (0-100) based on practical feasibility
- **Visual Analytics**: Interactive radar charts and component breakdowns
- **PDF Reports**: Professional downloadable evaluation reports
- **Multiple Interfaces**: 
  - Modern Streamlit application (recommended)
  - React frontend with Flask backend
  - Standalone HTML with Python HTTP server
- **Caching**: Consistent results - same idea always returns same score
- **RESTful API**: Clean Flask backend architecture

## 🏗️ Project Structure

```
startup/
├── backend/              # Flask REST API
│   ├── app.py           # Main Flask application
│   ├── services/        # Business logic services
│   │   ├── llm_service.py
│   │   ├── scoring.py
│   │   └── pdf_generator.py
│   ├── utils/           # Utility functions
│   └── requirements.txt
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.js
│   ├── index.html       # Standalone HTML version
│   └── package.json
│
├── streamlit_app.py     # Streamlit application (recommended)
├── requirements_streamlit.txt  # Streamlit dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key
- (Optional) Node.js 16+ for React frontend

### Option 1: Streamlit Application (Recommended) ⭐

**🌐 Try it online**: [https://startup-idea-evaluator-engine.streamlit.app/](https://startup-idea-evaluator-engine.streamlit.app/)

The easiest way to run the application with a modern, professional UI.

1. **Install Streamlit dependencies:**
```bash
pip install streamlit plotly groq python-dotenv reportlab
```

2. **Configure environment variables:**
   - Create `.env` file in `backend/` directory (or use Streamlit secrets)
   - Add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

3. **Run the Streamlit app:**
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- Modern card-based UI with custom styling
- Interactive radar charts
- PDF download functionality
- Caching for consistent results
- Dark mode support

### Option 2: Flask Backend + React Frontend

1. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
# Create .env file with GROQ_API_KEY
python app.py
```
Backend runs on `http://localhost:5000`

2. **Frontend Setup:**
```bash
cd frontend
npm install
npm start
```
Frontend runs on `http://localhost:3000`

### Option 3: Standalone HTML (No Node.js Required)

1. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
# Create .env file with GROQ_API_KEY
python app.py
```
Backend runs on `http://localhost:5000`

2. **Frontend Setup:**
```bash
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000` in your browser

**Note:** Update `frontend/index.html` line 441 to use `http://localhost:5000` for local backend.

## 📊 Evaluation Components

The application evaluates startup ideas across 11 dimensions:

1. **Executive Summary** - Overview of the idea
2. **Problem Statement** - Problem being solved
3. **Target Users** - Customer segment analysis
4. **Market Potential** - Market size and opportunity
5. **Technical Feasibility** - Technical requirements
6. **Innovation & Uniqueness** - Competitive differentiation
7. **Risks & Challenges** - Potential obstacles
8. **Strengths** - Key advantages
9. **Weaknesses** - Areas of concern
10. **Improvement Suggestions** - Actionable recommendations
11. **Final Recommendation** - Overall assessment

## 🎯 Scoring Algorithm

Feasibility score (0-100) is calculated using **strict feasibility criteria**, not creativity or novelty.

### Scoring Rules

**High Feasibility (75-95)** - ONLY if ALL criteria are met:
- ✅ Solves a **real, existing problem** faced today
- ✅ Has a **clearly defined target user** or customer
- ✅ Uses **currently available and proven technology**
- ✅ Has a **realistic MVP path within 6-12 months**
- ✅ Does **NOT promise guaranteed outcomes**
- ✅ Has **low ethical, legal, and regulatory risk**

**Low Feasibility (10-35)** - If ANY criteria is met:
- ❌ Claims scientifically impossible or unproven capabilities (mind reading, exact exam prediction, guaranteed profits, future prediction)
- ❌ Promises guaranteed success or exact outcomes
- ❌ Is vague, abstract, or lacks a concrete execution plan
- ❌ Enables or encourages cheating, manipulation, or unethical behavior
- ❌ Has no realistic MVP or validation path

### Important Rules

- **Competition does NOT reduce feasibility** - it only affects differentiation
- **Buzzwords** like "AI", "blockchain", or "quantum" do NOT increase scores unless tied to clear implementation
- **Violations** of scientific, ethical, or legal constraints cap the score below 40
- **Consistent scoring** - same idea receives nearly the same score every time (caching enabled)

### Weighted Components

- **Problem Clarity** (20%)
- **Market Size & Demand** (25%)
- **Technical Feasibility** (20%)
- **Innovation Level** (15%) - Competition doesn't reduce this
- **Scalability** (10%)
- **Risk Level** (10%)

## 🔌 API Endpoints

**Deployed Streamlit App:** [https://startup-idea-evaluator-engine.streamlit.app/](https://startup-idea-evaluator-engine.streamlit.app/)

**Deployed API:** `https://startup-idea-evaluator-bryf.onrender.com`

### `POST /evaluate`
Evaluates a startup idea.

**Request:**
```json
{
  "idea": "Your startup idea description"
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

### `GET /health`
Health check endpoint.

## 🛠️ Technologies Used

### Backend
- **Flask** - Web framework (REST API)
- **Groq** - LLM API client
- **ReportLab** - PDF generation
- **python-dotenv** - Environment management

### Frontend Options
- **Streamlit** - Modern Python-based UI (recommended)
- **React** - JavaScript UI framework
- **Plotly** - Interactive charts (Streamlit)
- **Chart.js** - Data visualization (React)
- **ReportLab** - PDF generation

### Key Features
- **Caching** - In-memory cache for consistent results
- **Error Handling** - Comprehensive error management
- **Modular Architecture** - Clean separation of concerns

## 📝 Code Quality

- Clean separation of concerns
- Modular service architecture
- Comprehensive error handling
- Environment variable configuration
- Consistent scoring with caching
- Interview-ready codebase

## 🔍 Scoring Accuracy

The scoring system is designed to be **strict and accurate**:

- **Impossible ideas** (mind reading, future prediction, exam question prediction) score **10-15**
- **Feasible business ideas** (attendance systems, HR management, SaaS platforms) score **75-90**
- **Unethical ideas** (cheating, manipulation, guaranteed profits) score **10-35**
- **Violations** (scientific/ethical/legal) are capped at **35** (below 40)

The system uses multiple detection layers to ensure accurate scoring:
1. Keyword detection in idea text
2. Evaluation text analysis
3. Hard caps for violations
4. Boost for proven business models with standard tech

## 🎓 Use Cases

- College final-year projects
- Hackathons
- Internship and placement interviews
- Startup idea validation
- Business plan development

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for aspiring entrepreneurs**

