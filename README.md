# 🚀 Startup Evaluator

An AI-powered web application that evaluates startup ideas and provides comprehensive, structured analysis with visual analytics and downloadable PDF reports.

## 📋 Features

- **AI-Powered Analysis**: Uses Groq LLM to analyze startup ideas
- **Structured Evaluation**: 11 comprehensive evaluation sections
- **Feasibility Scoring**: Weighted scoring algorithm (0-100)
- **Visual Analytics**: Interactive radar charts
- **PDF Reports**: Downloadable evaluation reports
- **Modern UI**: Beautiful, responsive React frontend
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
└── frontend/            # React frontend
    ├── src/
    │   ├── components/  # React components
    │   └── App.js
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Groq API key

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
   - Create `.env` file in `backend/` directory
   - Add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

4. **Run the Flask server:**
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run the development server:**
```bash
npm start
```

Frontend will run on `http://localhost:3000`

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

Feasibility score (0-100) is calculated using weighted factors:

- **Problem Clarity** (20%)
- **Market Size & Demand** (25%)
- **Technical Feasibility** (20%)
- **Innovation Level** (15%)
- **Scalability** (10%)
- **Risk Level** (10%)

## 🔌 API Endpoints

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
- **Flask** - Web framework
- **Groq** - LLM API client
- **ReportLab** - PDF generation
- **python-dotenv** - Environment management

### Frontend
- **React** - UI framework
- **Chart.js** - Data visualization
- **jsPDF** - PDF generation
- **Axios** - HTTP client

## 📝 Code Quality

- Clean separation of concerns
- Modular service architecture
- Comprehensive error handling
- Environment variable configuration
- Interview-ready codebase

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

