"""
Startup Evaluator - Streamlit Application
Modern, professional UI for startup idea evaluation
"""

import streamlit as st
import sys
from pathlib import Path
import hashlib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add backend directory to path
backend_dir = Path(__file__).parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from services.llm_service import LLMService
from services.scoring import ScoringService
from services.pdf_generator import PDFGenerator

# Page configuration
st.set_page_config(
    page_title="Startup Evaluator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for theming */
    :root {
        --primary-color: #667eea;
        --primary-dark: #5568d3;
        --secondary-color: #764ba2;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --radius: 12px;
        --radius-lg: 16px;
    }
    
    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --bg-primary: #111827;
            --bg-secondary: #1f2937;
            --border-color: #374151;
        }
    }
    
    /* Main container */
    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Card component */
    .card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .card-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .card-content {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 3rem;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .score-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    /* Section divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success-color);
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning-color);
    }
    
    .badge-danger {
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger-color);
    }
    
    /* List styles */
    .evaluation-list {
        list-style: none;
        padding: 0;
    }
    
    .evaluation-list li {
        padding: 0.75rem;
        margin: 0.5rem 0;
        background: var(--bg-secondary);
        border-radius: var(--radius);
        border-left: 3px solid var(--primary-color);
    }
    
    /* Button styles */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Fix button text wrapping */
    .stButton > button > div {
        white-space: nowrap !important;
        overflow: visible !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        white-space: nowrap;
        min-height: 44px;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: var(--radius);
        border: 2px solid var(--border-color);
        padding: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric styling */
    .stMetric {
        background: var(--bg-secondary);
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid var(--border-color);
    }
    
    /* Loading spinner */
    .spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--bg-secondary);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def get_services():
    """Initialize and cache services"""
    try:
        llm_service = LLMService()
        scoring_service = ScoringService()
        pdf_generator = PDFGenerator()
        return llm_service, scoring_service, pdf_generator
    except Exception as e:
        st.error(f"Error initializing services: {str(e)}")
        st.info("Please ensure GROQ_API_KEY is set in backend/.env file")
        return None, None, None

# Cache for evaluations
if 'evaluation_cache' not in st.session_state:
    st.session_state.evaluation_cache = {}

def normalize_idea_text(idea_text: str) -> str:
    """Normalize idea text for consistent caching"""
    return ' '.join(idea_text.strip().lower().split())

def get_cache_key(idea_text: str) -> str:
    """Generate cache key from idea text"""
    normalized = normalize_idea_text(idea_text)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def get_score_color(score: int) -> str:
    """Get color based on score"""
    if score >= 70:
        return "#10b981"  # Green
    elif score >= 50:
        return "#f59e0b"  # Orange
    else:
        return "#ef4444"  # Red

def create_radar_chart(component_scores: dict) -> go.Figure:
    """Create radar chart for component scores"""
    categories = list(component_scores.keys())
    values = list(component_scores.values())
    
    # Format category names
    formatted_categories = [cat.replace('_', ' ').title() for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=formatted_categories,
        fill='toself',
        name='Score',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                linecolor='rgba(0, 0, 0, 0.1)'
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def main():
    """Main application"""
    llm_service, scoring_service, pdf_generator = get_services()
    
    if llm_service is None or scoring_service is None or pdf_generator is None:
        st.stop()
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>🚀 Startup Evaluator</h1>
        <p class="hero-subtitle">AI-Powered Startup Idea Analysis & Feasibility Scoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'show_evaluation' not in st.session_state:
        st.session_state.show_evaluation = False
    if 'current_idea' not in st.session_state:
        st.session_state.current_idea = ""
    if 'idea_text' not in st.session_state:
        st.session_state.idea_text = ""
    
    # Sidebar for input (collapsed by default, can be toggled)
    with st.sidebar:
        st.markdown("### 💡 Enter Your Idea")
        
        # Handle Clear button action FIRST (before text area)
        clear_btn = False
        evaluate_btn = False
        
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            evaluate_btn = st.button("Evaluate", type="primary", use_container_width=True, key="evaluate_btn")
        with col2:
            clear_btn = st.button("Clear", use_container_width=True, key="clear_btn")
        
        # Handle Clear button action - must happen before text area
        if clear_btn:
            st.session_state.show_evaluation = False
            st.session_state.current_idea = ""
            st.session_state.idea_text = ""
            # Clear the text area widget state (widgets with keys store value in session_state[key])
            st.session_state.idea_input = ""
            # Force rerun to clear the text area
            st.rerun()
        
        # Initialize idea_input in session state if not exists
        if 'idea_input' not in st.session_state:
            st.session_state.idea_input = st.session_state.idea_text
        
        # Text area - widget with key stores value in st.session_state.idea_input
        idea_text = st.text_area(
            "Describe your startup idea in detail",
            height=200,
            placeholder="Example: A mobile and web-based application that helps college students track their daily expenses, set monthly budgets, and receive AI-based spending insights...",
            key="idea_input"
        )
        
        # Sync with our session state
        st.session_state.idea_text = idea_text
        
        # If text changes, hide evaluation
        if idea_text != st.session_state.get('previous_idea', ''):
            if st.session_state.show_evaluation:
                st.session_state.show_evaluation = False
            st.session_state.previous_idea = idea_text
    
    # Main content area
    if not idea_text.strip():
        # Empty state
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem;">
            <h3>Get Started</h3>
            <p class="card-content">Enter your startup idea in the sidebar to receive a comprehensive AI-powered evaluation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show example sections
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="card">
                <div class="card-header">📊 Comprehensive Analysis</div>
                <div class="card-content">11 detailed evaluation dimensions covering all aspects of your startup idea.</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card">
                <div class="card-header">🎯 Feasibility Scoring</div>
                <div class="card-content">Weighted scoring algorithm (0-100) based on practical feasibility criteria.</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="card">
                <div class="card-header">📈 Visual Analytics</div>
                <div class="card-content">Interactive charts and component breakdowns for better insights.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Handle evaluation
        evaluation = None
        
        if evaluate_btn and idea_text.strip():
            # User clicked Evaluate - perform evaluation
            cache_key = get_cache_key(idea_text)
            
            # Check cache first
            if cache_key in st.session_state.evaluation_cache:
                evaluation = st.session_state.evaluation_cache[cache_key]
                st.session_state.show_evaluation = True
                st.session_state.current_idea = idea_text
            else:
                # Perform new evaluation
                with st.spinner("Analyzing your startup idea..."):
                    try:
                        evaluation = llm_service.evaluate_idea(idea_text)
                        score = scoring_service.calculate_score(evaluation, idea_text)
                        evaluation['feasibility_score'] = score
                        
                        # Get component scores
                        component_scores = scoring_service.get_component_scores(evaluation)
                        evaluation['component_scores'] = component_scores
                        
                        # Cache the result
                        st.session_state.evaluation_cache[cache_key] = evaluation
                        st.session_state.show_evaluation = True
                        st.session_state.current_idea = idea_text
                    except Exception as e:
                        st.error(f"Error evaluating idea: {str(e)}")
                        st.stop()
        elif st.session_state.show_evaluation and st.session_state.current_idea == idea_text and idea_text.strip():
            # Show cached evaluation if idea matches and evaluation was shown
            cache_key = get_cache_key(idea_text)
            if cache_key in st.session_state.evaluation_cache:
                evaluation = st.session_state.evaluation_cache[cache_key]
        
        if evaluation and st.session_state.show_evaluation:
            # Score Display Section
            score = evaluation.get('feasibility_score', 0)
            score_color = get_score_color(score)
            
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <div class="score-badge" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);">
                    {score}
                </div>
                <div class="score-label">Feasibility Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component Scores Chart
            if 'component_scores' in evaluation:
                st.markdown("### 📊 Component Analysis")
                fig = create_radar_chart(evaluation['component_scores'])
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Evaluation Sections in Grid Layout
            st.markdown("### 📋 Detailed Evaluation")
            
            # Row 1: Executive Summary & Problem Statement
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">📝 Executive Summary</div>
                    <div class="card-content">{evaluation.get('executive_summary', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">🎯 Problem Statement</div>
                    <div class="card-content">{evaluation.get('problem_statement', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Row 2: Target Users & Market Potential
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">👥 Target Users</div>
                    <div class="card-content">{evaluation.get('target_users', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">📈 Market Potential</div>
                    <div class="card-content">{evaluation.get('market_potential', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Row 3: Technical Feasibility & Innovation
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">⚙️ Technical Feasibility</div>
                    <div class="card-content">{evaluation.get('technical_feasibility', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">💡 Innovation & Uniqueness</div>
                    <div class="card-content">{evaluation.get('innovation_uniqueness', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Row 4: Risks & Final Recommendation
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">⚠️ Risks & Challenges</div>
                    <div class="card-content">{evaluation.get('risks_challenges', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">✅ Final Recommendation</div>
                    <div class="card-content">{evaluation.get('final_recommendation', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Lists Section
            col1, col2, col3 = st.columns(3)
            with col1:
                strengths = evaluation.get('strengths', [])
                if strengths:
                    st.markdown("### 💪 Strengths")
                    st.markdown('<ul class="evaluation-list">', unsafe_allow_html=True)
                    for strength in strengths:
                        st.markdown(f'<li>{strength}</li>', unsafe_allow_html=True)
                    st.markdown('</ul>', unsafe_allow_html=True)
            
            with col2:
                weaknesses = evaluation.get('weaknesses', [])
                if weaknesses:
                    st.markdown("### ⚠️ Weaknesses")
                    st.markdown('<ul class="evaluation-list">', unsafe_allow_html=True)
                    for weakness in weaknesses:
                        st.markdown(f'<li>{weakness}</li>', unsafe_allow_html=True)
                    st.markdown('</ul>', unsafe_allow_html=True)
            
            with col3:
                suggestions = evaluation.get('improvement_suggestions', [])
                if suggestions:
                    st.markdown("### 💡 Suggestions")
                    st.markdown('<ul class="evaluation-list">', unsafe_allow_html=True)
                    for suggestion in suggestions:
                        st.markdown(f'<li>{suggestion}</li>', unsafe_allow_html=True)
                    st.markdown('</ul>', unsafe_allow_html=True)
            
            # PDF Download Section
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📄 Download Report")
            
            # Generate PDF and provide download
            try:
                pdf_path = pdf_generator.generate_report(evaluation)
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                # Get filename from path
                pdf_filename = Path(pdf_path).name
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
            

if __name__ == "__main__":
    main()
