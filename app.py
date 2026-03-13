"""
MUJ Student Advisor AI - Complete Implementation
PS 01: Student Academic Performance Prediction
Theme-Adaptive Design (Works in Light & Dark Mode)
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
import re

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="MUJ Student Advisor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== THEME-AWARE CSS WITH DARK MODE FIXES ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Theme variables - Light mode (default) */
    :root {
        --bg-primary: #F8FAFC;
        --bg-secondary: #FFFFFF;
        --card-bg: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
        --border-color: #E2E8F0;
        --input-bg: #FFFFFF;
        --hover-bg: #F1F5F9;
        --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --shadow-color: rgba(0, 0, 0, 0.05);
    }
    
    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0A0F1A;
            --bg-secondary: #151F2F;
            --card-bg: #1E2A3A;
            --text-primary: #FFFFFF !important;
            --text-secondary: #E2E8F0 !important;
            --text-muted: #94A3B8 !important;
            --border-color: #2D3A4F;
            --input-bg: #0A0F1A;
            --hover-bg: #2D3A4F;
            --shadow-color: rgba(0, 0, 0, 0.5);
        }
        
        /* Force ALL card backgrounds to change */
        .feature-card, 
        .metric-card, 
        .contact-card, 
        .recommendation-item,
        .sidebar-section,
        .stTabs [data-baseweb="tab-list"],
        .streamlit-expanderHeader,
        .streamlit-expanderContent,
        div[data-baseweb="select"] > div,
        .stNumberInput input, 
        .stTextInput input,
        .stTextArea textarea,
        .stAlert,
        .stDownloadButton button,
        [data-testid="stSidebar"] {
            background-color: var(--card-bg) !important;
            border-color: var(--border-color) !important;
        }
        
        /* Card text colors in dark mode */
        .feature-card,
        .metric-card,
        .contact-card,
        .recommendation-item,
        .sidebar-section {
            color: var(--text-secondary) !important;
        }
        
        .feature-label,
        .metric-label,
        .contact-title,
        .sidebar-section-title,
        .confidence-label {
            color: var(--text-primary) !important;
        }
        
        .feature-value,
        .metric-value,
        .contact-detail strong {
            color: var(--text-primary) !important;
        }
    }
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        color: var(--text-secondary);
        background-color: var(--bg-primary);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: var(--text-primary);
    }
    
    /* Wider Sidebar */
    [data-testid="stSidebar"] {
        min-width: 480px !important;
        max-width: 500px !important;
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
        padding: 1.5rem;
    }
    
    /* Input fields */
    div[data-baseweb="select"] > div,
    .stNumberInput input, 
    .stTextInput input,
    .stTextArea textarea {
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }
    
    .stSlider label, .stSelectbox label, .stNumberInput label,
    .stRadio label, .stCheckbox label {
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: var(--text-primary) !important;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 1.4rem;
        color: var(--text-primary) !important;
        margin: 1rem 0;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Grade Boxes */
    .grade-box-0 { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
    .grade-box-1 { background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); }
    .grade-box-2 { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); }
    .grade-box-3 { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); }
    
    .grade-box-0, .grade-box-1, .grade-box-2, .grade-box-3 {
        padding: 2rem;
        border-radius: 20px;
        color: white !important;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .grade-box-0 div, .grade-box-1 div, .grade-box-2 div, .grade-box-3 div { 
        color: white !important; 
    }
    
    .grade-title { 
        font-size: 2.2rem; 
        font-weight: 700; 
        margin-bottom: 0.5rem; 
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .grade-description { 
        font-size: 1.1rem; 
        opacity: 0.95; 
        margin-bottom: 1rem; 
    }
    
    .grade-badge { 
        display: inline-block; 
        background: rgba(255,255,255,0.2); 
        padding: 0.5rem 1.2rem; 
        border-radius: 50px; 
        font-size: 0.9rem; 
        margin: 0.5rem 0; 
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Cards */
    .feature-card { 
        background: var(--card-bg); 
        padding: 1.2rem; 
        border-radius: 16px; 
        margin: 0.5rem 0; 
        border-left: 4px solid #667eea; 
        box-shadow: 0 4px 20px var(--shadow-color); 
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
    }
    
    .feature-card:hover { 
        transform: translateX(5px); 
        box-shadow: 0 8px 30px var(--shadow-color); 
    }
    
    .feature-icon { 
        font-size: 1.5rem; 
        margin-right: 0.5rem; 
    }
    
    .feature-label { 
        font-weight: 600; 
        color: var(--text-primary); 
        margin-bottom: 0.25rem; 
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .feature-value { 
        font-size: 1.2rem; 
        color: var(--text-primary); 
        font-weight: 500;
    }
    
    /* Metric Cards */
    .metric-card { 
        background: var(--card-bg); 
        padding: 1.2rem; 
        border-radius: 16px; 
        text-align: center; 
        box-shadow: 0 4px 20px var(--shadow-color); 
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 8px 30px var(--shadow-color); 
        border-color: #667eea;
    }
    
    .metric-icon { 
        font-size: 2rem; 
        margin-bottom: 0.5rem; 
    }
    
    .metric-label { 
        font-size: 0.85rem; 
        color: var(--text-muted); 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
    }
    
    .metric-value { 
        font-size: 2rem; 
        font-weight: 700; 
        color: var(--text-primary); 
        margin: 0.5rem 0; 
    }
    
    /* Contact Cards */
    .contact-card { 
        background: var(--card-bg); 
        padding: 1.5rem; 
        border-radius: 20px; 
        border: 1px solid var(--border-color); 
        box-shadow: 0 4px 20px var(--shadow-color); 
        flex-grow: 1; 
        display: flex; 
        flex-direction: column; 
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px var(--shadow-color);
    }
    
    .contact-title { 
        font-size: 1.2rem; 
        font-weight: 600; 
        color: var(--text-primary) !important; 
        margin-bottom: 1rem; 
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .contact-detail { 
        padding: 0.5rem 0; 
        border-bottom: 1px solid var(--border-color); 
        color: var(--text-secondary); 
    }
    
    .contact-detail:last-child { 
        border-bottom: none; 
    }
    
    .contact-detail strong {
        color: var(--text-primary);
    }
    
    /* Recommendation Items */
    .recommendation-item { 
        background: var(--card-bg); 
        padding: 1rem; 
        border-radius: 12px; 
        margin: 0.5rem 0; 
        border-left: 4px solid #667eea; 
        box-shadow: 0 4px 20px var(--shadow-color); 
        transition: all 0.2s ease; 
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
    }
    
    .recommendation-item:hover { 
        transform: translateX(5px); 
        box-shadow: 0 8px 30px var(--shadow-color); 
    }
    
    /* Confidence Bar */
    .confidence-item { 
        margin: 0.75rem 0; 
    }
    
    .confidence-label { 
        display: flex; 
        justify-content: space-between; 
        margin-bottom: 0.25rem; 
        font-weight: 500; 
        color: var(--text-primary); 
    }
    
    .confidence-bar-bg { 
        background: var(--border-color); 
        border-radius: 10px; 
        height: 24px; 
        width: 100%; 
        overflow: hidden; 
    }
    
    .confidence-bar-fill { 
        height: 24px; 
        border-radius: 10px; 
        transition: width 0.5s ease-in-out; 
    }
    
    /* Buttons */
    .stButton > button { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white !important; 
        font-weight: 600; 
        padding: 0.75rem 2rem; 
        border-radius: 12px; 
        border: none; 
        width: 100%; 
        font-size: 1.1rem; 
        text-transform: uppercase; 
        letter-spacing: 0.5px; 
        transition: all 0.3s ease; 
        box-shadow: 0 10px 20px -10px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 15px 30px -10px rgba(102, 126, 234, 0.6); 
    }
    
    /* Sidebar specific */
    .sidebar-header { 
        font-size: 1.5rem; 
        font-weight: 700; 
        color: var(--text-primary) !important; 
        text-align: center; 
        margin: 1rem 0; 
        padding: 1rem; 
        border-bottom: 2px solid #667eea; 
    }
    
    .sidebar-section { 
        background: var(--card-bg); 
        padding: 1rem; 
        border-radius: 16px; 
        margin: 1rem 0; 
        box-shadow: 0 4px 20px var(--shadow-color); 
        border: 1px solid var(--border-color);
    }
    
    .sidebar-section-title { 
        font-size: 1rem; 
        font-weight: 600; 
        color: var(--text-primary) !important; 
        margin-bottom: 1rem; 
        text-transform: uppercase; 
        letter-spacing: 0.5px; 
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 2rem; 
        background: var(--bg-secondary); 
        padding: 0.5rem; 
        border-radius: 16px; 
        box-shadow: 0 4px 20px var(--shadow-color); 
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] { 
        height: 3rem; 
        font-weight: 600; 
        color: var(--text-secondary) !important; 
        border-radius: 10px; 
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; 
        color: white !important; 
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color: var(--text-primary) !important;
        background-color: var(--card-bg) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Dividers */
    .custom-divider { 
        height: 2px; 
        background: linear-gradient(90deg, transparent, #667eea, transparent); 
        margin: 2rem 0; 
    }
    
    /* Footer */
    .footer { 
        text-align: center; 
        padding: 2rem; 
        color: var(--text-muted); 
        font-size: 0.9rem; 
        border-top: 1px solid var(--border-color); 
        margin-top: 2rem; 
    }
    
    /* Diff indicators */
    .diff-positive { 
        background: rgba(16, 185, 129, 0.1); 
        color: #10B981 !important; 
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
    }
    
    .diff-negative { 
        background: rgba(239, 68, 68, 0.1); 
        color: #EF4444 !important; 
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
    }
    
    .diff-neutral { 
        background: rgba(100, 116, 139, 0.1); 
        color: var(--text-muted) !important; 
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
    }
    
    /* ===== FIX FOR DEMO PROFILE CARDS ===== */
    .content-card {
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    /* Light mode text colors for demo cards */
    .content-card h4 {
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .content-card p {
        margin: 0.2rem 0;
        font-weight: 500;
        color: #1E293B !important;  /* Dark text for light mode */
    }
    
    /* Dark mode overrides for demo cards */
    @media (prefers-color-scheme: dark) {
        .content-card {
            background: var(--card-bg) !important;
            border: 1px solid var(--border-color);
        }
        
        .content-card h4 {
            color: inherit;  /* Uses the color set inline from demo */
        }
        
        .content-card p {
            color: var(--text-secondary) !important;  /* Light text for dark mode */
        }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header { font-size: 2.2rem; }
        .sub-header { font-size: 1.5rem; }
        [data-testid="stSidebar"] { min-width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)# ==================== LOAD MODEL AND METADATA ====================
@st.cache_resource
def load_model():
    """Load the trained model and metadata"""
    try:
        with open('student_performance_predictor.pkl', 'rb') as f:
            model = pickle.load(f)
        try:
            with open('model_metadata.pkl', 'rb') as f:
                metadata = pickle.load(f)
        except:
            metadata = None
        st.sidebar.success("✅ Model loaded successfully")
        return model, metadata
    except FileNotFoundError:
        st.sidebar.error("❌ Model file not found! Please run train_model.py first.")
        st.stop()
    except Exception as e:
        st.sidebar.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

model, metadata = load_model()

# ==================== LOAD GUIDELINES ====================
def load_guidelines():
    """Load MUJ student success guidelines"""
    try:
        with open('muj_guidelines.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
MUJ STUDENT SUCCESS GUIDELINES:

GRADE CATEGORY 0 (Highest Performers):
- Invite to the 'Student Excellence' Research Program for guided undergraduate research.
- Suggest applying for Peer Mentor or Teaching Assistant (TA) roles for junior CSE batches.
- Recommend advanced certification courses in specialized domains like AI/ML or Cloud Computing.
- Encourage submitting their semester projects to national hackathons.

GRADE CATEGORY 1 (Above Average):
- Suggest joining technical clubs like IEEE CIS MUJ.
- Recommend exploring elective subjects in specialized CSE domains.
- Encourage participation in coding competitions and hackathons.
- Suggest taking up leadership roles in student chapters.

GRADE CATEGORY 2 (Below Average):
- Recommend attending weekly Faculty Office Hours.
- Suggest the 'Time Management & Study Skills' workshop.
- Encourage forming study groups with peers.
- Recommend using online learning resources like NPTEL.

GRADE CATEGORY 3 (At-Risk):
- Immediate mandatory referral to the Student Success Center for an academic recovery plan.
- Require a confidential meeting with the Campus Counselor to address potential stress or burnout.
- Recommend a strict 50% reduction in extracurricular and club commitments to prioritize core academics.
- Assign a dedicated senior peer mentor for weekly accountability and assignment tracking.
- Suggest a review of their current course load to see if dropping a non-core elective is necessary to protect their GPA.
"""

guidelines = load_guidelines()

# ==================== FEATURE DEFINITIONS ====================
FEATURE_INFO = {
    'StudyHours': {'description': 'Weekly hours spent studying', 'range': (5, 43), 'default': 20, 'icon': '📚'},
    'Attendance': {'description': 'Class attendance percentage', 'range': (60, 100), 'default': 80, 'icon': '📊'},
    'Resources': {'description': 'Access to learning resources', 'options': {0: 'Limited', 1: 'Basic', 2: 'Extensive'}, 'default': 1, 'icon': '📖'},
    'Extracurricular': {'description': 'Participation in extracurricular activities', 'options': {0: 'No', 1: 'Yes'}, 'default': 0, 'icon': '⚽'},
    'Motivation': {'description': 'Student motivation level', 'options': {0: 'Low', 1: 'Medium', 2: 'High'}, 'default': 1, 'icon': '🎯'},
    'Internet': {'description': 'Internet access availability', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '🌐'},
    'Gender': {'description': 'Student gender', 'options': {0: 'Male', 1: 'Female'}, 'default': 0, 'icon': '👤'},
    'Age': {'description': 'Student age', 'range': (18, 30), 'default': 21, 'icon': '🎂'},
    'LearningStyle': {'description': 'Preferred learning style', 'options': {0: 'Visual', 1: 'Auditory', 2: 'Reading/Writing', 3: 'Kinesthetic'}, 'default': 0, 'icon': '🧠'},
    'OnlineCourses': {'description': 'Number of online courses taken', 'range': (0, 20), 'default': 5, 'icon': '💻'},
    'Discussions': {'description': 'Participation in academic discussions', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '💬'},
    'AssignmentCompletion': {'description': 'Percentage of assignments completed', 'range': (50, 100), 'default': 85, 'icon': '📝'},
    'ExamScore': {'description': 'Score on primary examination', 'range': (40, 100), 'default': 75, 'icon': '📋'},
    'EduTech': {'description': 'Use of educational technology tools', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '🖥️'},
    'StressLevel': {'description': 'Reported stress level', 'options': {0: 'Low', 1: 'Medium', 2: 'High'}, 'default': 1, 'icon': '😰'}
}

GRADE_INFO = {
    0: {'name': 'Highest Performer', 'description': 'Excellent academic standing - Top of the class', 'color': '#10B981', 'emoji': '🌟', 'range': '90-100%', 'short': 'Best'},
    1: {'name': 'Above Average', 'description': 'Good academic standing - Above peer average', 'color': '#3B82F6', 'emoji': '📈', 'range': '75-89%', 'short': 'Above Avg'},
    2: {'name': 'Below Average', 'description': 'Needs improvement - Below peer average', 'color': '#F59E0B', 'emoji': '⚠️', 'range': '60-74%', 'short': 'Below Avg'},
    3: {'name': 'At-Risk', 'description': 'Requires immediate intervention', 'color': '#EF4444', 'emoji': '🚨', 'range': 'Below 60%', 'short': 'At-Risk'}
}

# ==================== CALLBACK FOR DEMO PROFILES ====================
def apply_demo_profile(demo_data):
    st.session_state['ExamScore'] = demo_data['ExamScore']
    st.session_state['Attendance'] = demo_data['Attendance']
    st.session_state['StudyHours'] = demo_data['StudyHours']
    st.session_state['StressLevel'] = demo_data['Stress']
    
    # Set defaults for other fields
    st.session_state['AssignmentCompletion'] = FEATURE_INFO['AssignmentCompletion']['default']
    st.session_state['OnlineCourses'] = FEATURE_INFO['OnlineCourses']['default']
    st.session_state['Motivation'] = 2 if demo_data['name'] == "🌟 High Performer" else 1
    st.session_state['LearningStyle'] = FEATURE_INFO['LearningStyle']['default']
    st.session_state['Gender'] = FEATURE_INFO['Gender']['default']
    st.session_state['Age'] = FEATURE_INFO['Age']['default']
    st.session_state['Internet'] = FEATURE_INFO['Internet']['default']
    st.session_state['Resources'] = FEATURE_INFO['Resources']['default']
    st.session_state['EduTech'] = FEATURE_INFO['EduTech']['default']
    st.session_state['Extracurricular'] = FEATURE_INFO['Extracurricular']['default']
    st.session_state['Discussions'] = FEATURE_INFO['Discussions']['default']
    
    st.session_state['auto_predict'] = True

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎓 MUJ Student Portal</div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Student Information")
    st.markdown("Enter the student's complete profile below:")
    st.markdown("---")
    
    input_data = {}
    
    with st.expander("📚 Academic Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['StudyHours'] = st.slider("📚 Study Hours", FEATURE_INFO['StudyHours']['range'][0], FEATURE_INFO['StudyHours']['range'][1], FEATURE_INFO['StudyHours']['default'], key='StudyHours')
            input_data['AssignmentCompletion'] = st.slider("📝 Assignment %", FEATURE_INFO['AssignmentCompletion']['range'][0], FEATURE_INFO['AssignmentCompletion']['range'][1], FEATURE_INFO['AssignmentCompletion']['default'], key='AssignmentCompletion')
        with col2:
            input_data['Attendance'] = st.slider("📊 Attendance %", FEATURE_INFO['Attendance']['range'][0], FEATURE_INFO['Attendance']['range'][1], FEATURE_INFO['Attendance']['default'], key='Attendance')
            input_data['ExamScore'] = st.slider("📋 Exam Score", FEATURE_INFO['ExamScore']['range'][0], FEATURE_INFO['ExamScore']['range'][1], FEATURE_INFO['ExamScore']['default'], key='ExamScore')
    
    with st.expander("🧠 Psychological Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Motivation'] = st.selectbox("🎯 Motivation", list(FEATURE_INFO['Motivation']['options'].keys()), format_func=lambda x: FEATURE_INFO['Motivation']['options'][x], key='Motivation')
            input_data['LearningStyle'] = st.selectbox("🧠 Learning Style", list(FEATURE_INFO['LearningStyle']['options'].keys()), format_func=lambda x: FEATURE_INFO['LearningStyle']['options'][x], key='LearningStyle')
        with col2:
            input_data['StressLevel'] = st.selectbox("😰 Stress Level", list(FEATURE_INFO['StressLevel']['options'].keys()), format_func=lambda x: FEATURE_INFO['StressLevel']['options'][x], key='StressLevel')
    
    with st.expander("👥 Demographic Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Gender'] = st.radio("👤 Gender", list(FEATURE_INFO['Gender']['options'].keys()), format_func=lambda x: FEATURE_INFO['Gender']['options'][x], horizontal=True, key='Gender')
        with col2:
            input_data['Age'] = st.number_input("🎂 Age", FEATURE_INFO['Age']['range'][0], FEATURE_INFO['Age']['range'][1], FEATURE_INFO['Age']['default'], key='Age')
    
    with st.expander("🌐 Environmental & Social", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Internet'] = st.selectbox("🌐 Internet", list(FEATURE_INFO['Internet']['options'].keys()), format_func=lambda x: FEATURE_INFO['Internet']['options'][x], key='Internet')
            input_data['Resources'] = st.selectbox("📖 Resources", list(FEATURE_INFO['Resources']['options'].keys()), format_func=lambda x: FEATURE_INFO['Resources']['options'][x], key='Resources')
            input_data['OnlineCourses'] = st.slider("💻 Online Courses", FEATURE_INFO['OnlineCourses']['range'][0], FEATURE_INFO['OnlineCourses']['range'][1], FEATURE_INFO['OnlineCourses']['default'], key='OnlineCourses')
        with col2:
            input_data['EduTech'] = st.selectbox("🖥️ EduTech Use", list(FEATURE_INFO['EduTech']['options'].keys()), format_func=lambda x: FEATURE_INFO['EduTech']['options'][x], key='EduTech')
            input_data['Extracurricular'] = st.selectbox("⚽ Extracurricular", list(FEATURE_INFO['Extracurricular']['options'].keys()), format_func=lambda x: FEATURE_INFO['Extracurricular']['options'][x], key='Extracurricular')
            input_data['Discussions'] = st.selectbox("💬 Discussions", list(FEATURE_INFO['Discussions']['options'].keys()), format_func=lambda x: FEATURE_INFO['Discussions']['options'][x], key='Discussions')
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    predict_clicked = st.button("🔮 GENERATE SUCCESS PLAN", use_container_width=True)
    
    if predict_clicked or st.session_state.get('auto_predict', False):
        if 'auto_predict' in st.session_state:
            st.session_state['auto_predict'] = False
            
        feature_order = ['StudyHours', 'Attendance', 'Resources', 'Extracurricular',
                        'Motivation', 'Internet', 'Gender', 'Age', 'LearningStyle',
                        'OnlineCourses', 'Discussions', 'AssignmentCompletion',
                        'ExamScore', 'EduTech', 'StressLevel']
        
        # Validate all features are present
        for feature in feature_order:
            if feature not in input_data:
                input_data[feature] = FEATURE_INFO[feature]['default'] if feature in FEATURE_INFO else 0
        
        input_list = [input_data[feature] for feature in feature_order]
        input_df = pd.DataFrame([input_list], columns=feature_order)
        
        # Validate no null values
        if input_df.isnull().any().any():
            st.sidebar.error("⚠️ Some input values are invalid")
        else:
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            
            st.session_state['prediction'] = prediction
            st.session_state['probabilities'] = probabilities
            st.session_state['input_data'] = input_data
            st.success("✅ Prediction generated! Scroll down to view results.")

# ==================== THEME-AWARE PLOTLY TEMPLATE ====================
def get_plotly_template():
    """Returns appropriate Plotly template based on theme"""
    if st.get_option("theme.base") == "dark":
        return "plotly_dark"
    return "plotly_white"

# ==================== MAIN CONTENT ====================
st.markdown('<h1 class="main-header">🎓 MUJ Student Advisor AI</h1>', unsafe_allow_html=True)
st.markdown("""<p style="text-align: center; font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 2rem;">Intelligent Student Performance Prediction & Personalized Intervention System</p>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 PREDICTION & ANALYSIS", "📈 DEEP DIVE", "📚 GUIDELINES", "ℹ️ ABOUT"])

with tab1:
    st.markdown('<h2 class="sub-header">🚀 Quick Start: Demo Profiles</h2>', unsafe_allow_html=True)
    st.write("Load a sample student profile to instantly generate a prediction and personalized success plan.")
    
    demo_cols = st.columns(4)
    demos = [
        {"name": "🌟 High Performer", "ExamScore": 95, "Attendance": 98, "StudyHours": 35, "Stress": 0, "color": "#10B981"},
        {"name": "📈 Above Average", "ExamScore": 82, "Attendance": 85, "StudyHours": 25, "Stress": 1, "color": "#3B82F6"},
        {"name": "⚠️ Below Average", "ExamScore": 68, "Attendance": 70, "StudyHours": 15, "Stress": 1, "color": "#F59E0B"},
        {"name": "🚨 At-Risk", "ExamScore": 45, "Attendance": 60, "StudyHours": 8, "Stress": 2, "color": "#EF4444"}
    ]
    
    for col, demo in zip(demo_cols, demos):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="
                text-align: center; 
                border-left: 4px solid {demo['color']};
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <h4 style="
                    margin-bottom: 0.75rem; 
                    color: {demo['color']};
                    font-size: 0.95rem;
                    white-space: nowrap;
                ">{demo['name']}</h4>
                <p style="margin: 0.15rem 0; font-size: 0.85rem;">📋 Exam: {demo['ExamScore']}</p>
                <p style="margin: 0.15rem 0; font-size: 0.85rem;">📊 Att: {demo['Attendance']}%</p>
                <p style="margin: 0.15rem 0; font-size: 0.85rem;">📚 Study: {demo['StudyHours']}h</p>
            </div>
            """, unsafe_allow_html=True)
        
            st.button(
                f"{demo['name'].split()[1]}", 
                key=f"demo_tab1_{demo['name']}", 
                use_container_width=True,
                on_click=apply_demo_profile,
                args=(demo,)
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    if 'input_data' in st.session_state:
        input_data = st.session_state['input_data']
    
    st.markdown('<h2 class="sub-header">👤 Student Profile Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p class="section-header">📚 Academic</p>', unsafe_allow_html=True)
        for icon, label, value in [
            ("📚", "Study Hours", f"{input_data['StudyHours']} hrs/week"),
            ("📊", "Attendance", f"{input_data['Attendance']}%"),
            ("📝", "Assignments", f"{input_data['AssignmentCompletion']}%"),
            ("📋", "Exam Score", f"{input_data['ExamScore']}"),
        ]:
            st.markdown(f"""
            <div class="feature-card" style="
                display:flex; align-items:center; gap:14px;
                height:64px; padding:0 16px;">
                <span style="font-size:1.4rem">{icon}</span>
                <div style="flex:1; min-width:0;">
                    <div class="feature-label" style="font-size:.7rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{label}</div>
                    <div class="feature-value" style="font-size:1rem;">{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-header">🧠 Psychological</p>', unsafe_allow_html=True)
        for icon, label, value in [
            ("🎯", "Motivation", FEATURE_INFO['Motivation']['options'][input_data['Motivation']]),
            ("😰", "Stress Level", FEATURE_INFO['StressLevel']['options'][input_data['StressLevel']]),
            ("🧠", "Learning Style", FEATURE_INFO['LearningStyle']['options'][input_data['LearningStyle']]),
            ("🎂", "Age", f"{input_data['Age']} years"),
        ]:
            st.markdown(f"""
            <div class="feature-card" style="
                display:flex; align-items:center; gap:14px;
                height:64px; padding:0 16px;">
                <span style="font-size:1.4rem">{icon}</span>
                <div style="flex:1; min-width:0;">
                    <div class="feature-label" style="font-size:.7rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{label}</div>
                    <div class="feature-value" style="font-size:1rem;">{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown('<p class="section-header">🌐 Environmental</p>', unsafe_allow_html=True)
        for icon, label, value in [
            ("🌐", "Internet", FEATURE_INFO['Internet']['options'][input_data['Internet']]),
            ("📖", "Resources", FEATURE_INFO['Resources']['options'][input_data['Resources']]),
            ("💻", "Online Courses", f"{input_data['OnlineCourses']}"),
            ("⚽", "Extracurricular", FEATURE_INFO['Extracurricular']['options'][input_data['Extracurricular']]),
        ]:
            st.markdown(f"""
            <div class="feature-card" style="
                display:flex; align-items:center; gap:14px;
                height:64px; padding:0 16px;">
                <span style="font-size:1.4rem">{icon}</span>
                <div style="flex:1; min-width:0;">
                    <div class="feature-label" style="font-size:.7rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{label}</div>
                    <div class="feature-value" style="font-size:1rem;">{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if 'prediction' in st.session_state:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">🎯 Prediction Results</h2>', unsafe_allow_html=True)
        
        pred = st.session_state['prediction']
        probabilities = st.session_state['probabilities']
        grade_info = GRADE_INFO[pred]
        
        box_class = f"grade-box-{pred}"
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="{box_class}">
                <span class="grade-badge">Predicted Grade Category: {pred}</span>
                <div class="grade-title">{grade_info['emoji']} {grade_info['name']}</div>
                <div class="grade-description">{grade_info['description']}</div>
                <div style="font-size: 1.2rem; margin-top: 1rem;">Expected Score Range: <strong>{grade_info['range']}</strong></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Build confidence bars
            bars_html = ""
            for i in range(4):
                glow = f"box-shadow:0 0 6px {GRADE_INFO[i]['color']};" if i == pred else ""
                weight = "700" if i == pred else "400"
                text_color = "#fff" if i == pred else "var(--text-muted)"
                opacity = "1" if i == pred else "0.4"
                width = f"{probabilities[i]*100:.1f}"
                pct = f"{probabilities[i]:.1%}"
                name = GRADE_INFO[i]['name']
                color = GRADE_INFO[i]['color']
        
                bars_html += (
                    f'<div style="margin-bottom:12px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">'
                    f'<div style="display:flex;align-items:center;gap:8px;">'
                    f'<div style="width:8px;height:8px;border-radius:50%;background:{color};{glow}"></div>'
                    f'<span style="font-size:.82rem;font-weight:{weight};color:{text_color};">{name}</span>'
                    f'</div>'
                    f'<span style="font-size:.82rem;font-weight:700;color:{color};">{pct}</span>'
                    f'</div>'
                    f'<div style="background:rgba(255,255,255,.07);border-radius:4px;height:6px;width:100%;overflow:hidden;">'
                    f'<div style="width:{width}%;height:6px;border-radius:4px;background:{color};opacity:{opacity};"></div>'
                    f'</div>'
                    f'</div>'
                )

            # Render opening card
            st.markdown(
                '<div style="background:var(--card-bg);border:1px solid var(--border-color);'
                'border-radius:16px;padding:15px;">'
                '<div style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;'
                'color:var(--text-muted);margin-bottom:10px;font-weight:600;margin-top: 10px">Confidence Breakdown</div>',
                unsafe_allow_html=True
            )
    
            # Render bars
            st.markdown(bars_html, unsafe_allow_html=True)
    
            # Close card
            st.markdown('</div>', unsafe_allow_html=True) 
        

        #######
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown('<h2 class="sub-header">📋 Personalized Success Plan</h2>', unsafe_allow_html=True)
            #st.markdown('<div class="contact-card" style="min-height: 280px;">', unsafe_allow_html=True)
            
            if pred == 0:
                st.markdown("""
                <div class="recommendation-item">✅ Invite to the 'Student Excellence' Research Program for guided undergraduate research.</div>
                <div class="recommendation-item">✅ Suggest applying for Peer Mentor or Teaching Assistant (TA) roles for junior CSE batches.</div>
                <div class="recommendation-item">✅ Recommend advanced certification courses in specialized domains like AI/ML or Cloud Computing.</div>
                <div class="recommendation-item">✅ Encourage submitting their semester projects to national hackathons.</div>
                """, unsafe_allow_html=True)
            elif pred == 1:
                st.markdown("""
                <div class="recommendation-item">✅ Suggest joining technical clubs like IEEE CIS MUJ.</div>
                <div class="recommendation-item">✅ Recommend exploring elective subjects in specialized CSE domains.</div>
                <div class="recommendation-item">✅ Encourage participation in coding competitions and hackathons.</div>
                <div class="recommendation-item">✅ Suggest taking up leadership roles in student chapters.</div>
                """, unsafe_allow_html=True)
            elif pred == 2:
                st.markdown("""
                <div class="recommendation-item">✅ Recommend attending weekly Faculty Office Hours.</div>
                <div class="recommendation-item">✅ Suggest the 'Time Management & Study Skills' workshop.</div>
                <div class="recommendation-item">✅ Encourage forming study groups with peers.</div>
                <div class="recommendation-item">✅ Recommend using online learning resources like NPTEL.</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="recommendation-item">✅ Immediate mandatory referral to the Student Success Center for an academic recovery plan.</div>
                <div class="recommendation-item">✅ Require a confidential meeting with the Campus Counselor to address potential stress or burnout.</div>
                <div class="recommendation-item">✅ Recommend a strict 50% reduction in extracurricular and club commitments to prioritize core academics.</div>
                <div class="recommendation-item">✅ Assign a dedicated senior peer mentor for weekly accountability and assignment tracking.</div>
                <div class="recommendation-item">✅ Suggest a review of their current course load to see if dropping a non-core elective is necessary to protect their GPA.</div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h2 class="sub-header">📞 Contact Points</h2>', unsafe_allow_html=True)
            if pred == 0:
                st.markdown("""<div class="contact-card" style="min-height: 180px;"><div class="contact-title">👨‍🏫 Research Coordinator</div><div class="contact-detail"><strong>Dr. Rajesh Kumar</strong></div><div class="contact-detail">📧 rajesh.kumar@muj.edu</div><div class="contact-detail">📍 AB-1, Room 204</div></div>""", unsafe_allow_html=True)
            elif pred == 1:
                st.markdown("""<div class="contact-card" style="min-height: 180px;"><div class="contact-title">🤖 IEEE CIS MUJ</div><div class="contact-detail"><strong>Prof. Priya Sharma</strong></div><div class="contact-detail">📧 priya.sharma@muj.edu</div><div class="contact-detail">📍 AB-2, Room 105</div></div>""", unsafe_allow_html=True)
            elif pred == 2:
                st.markdown("""<div class="contact-card" style="min-height: 180px;"><div class="contact-title">👨‍🏫 Academic Advisor</div><div class="contact-detail"><strong>Dr. Amit Patel</strong></div><div class="contact-detail">🕒 Tue/Thu 2-4 PM</div><div class="contact-detail">📍 AB-1, Room 305</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="contact-card" style="min-height: 180px;"><div class="contact-title">🆘 Student Success Center</div><div class="contact-detail">📧 success@muj.edu</div><div class="contact-detail">📞 +91-123-4567890</div><div class="contact-detail">📍 Student Services Block</div></div>""", unsafe_allow_html=True)
    else:
        st.info("👆 Load a demo profile above or click 'GENERATE SUCCESS PLAN' in the sidebar to see prediction results.")

with tab2:
    st.markdown('<h2 class="sub-header">📈 Performance Analysis Dashboard</h2>', unsafe_allow_html=True)
    if 'prediction' in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if metadata and 'feature_importance' in metadata:
                st.markdown("#### 🔍 Top Predictive Features")
                import_df = pd.DataFrame(metadata['feature_importance']).head(8)
                fig = px.bar(
                    import_df,
                    x='importance',
                    y='feature',
                    orientation='h',
                    title='Most Important Factors',
                    color='importance',
                    color_continuous_scale='Viridis',
                    template=get_plotly_template()
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(type='log'),  # ← this is the key fix
                    yaxis=dict(categoryorder='total ascending')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Radar Chart
            st.markdown("#### 📊 Multi-Factor Balance")
            radar_metrics = ['Study', 'Attendance', 'Assignments', 'Motivation', 'Discussions']
            radar_values = [
                (st.session_state['input_data']['StudyHours'] / 43) * 100,
                st.session_state['input_data']['Attendance'],
                st.session_state['input_data']['AssignmentCompletion'],
                (st.session_state['input_data']['Motivation'] / 2) * 100,
                (st.session_state['input_data']['Discussions'] * 100) if isinstance(st.session_state['input_data']['Discussions'], int) else 50
            ]
            
            pred_color = GRADE_INFO[st.session_state['prediction']]['color']
            r, g, b = tuple(int(pred_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

            fig_radar = go.Figure(data=go.Scatterpolar(
                r=radar_values + [radar_values[0]],  # close the shape
                theta=radar_metrics + [radar_metrics[0]],
                fill='toself',
                line=dict(color=pred_color, width=2),
                fillcolor=f"rgba({r},{g},{b},0.25)",
                marker=dict(size=6, color=pred_color)
            ))

            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',  # transparent background
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(size=10, color='rgba(255,255,255,0.4)'),
                        gridcolor='rgba(255,255,255,0.1)',
                        linecolor='rgba(255,255,255,0.1)',
                        tickvals=[20, 40, 60, 80, 100],
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=13, color='rgba(255,255,255,0.85)'),
                        gridcolor='rgba(255,255,255,0.1)',
                        linecolor='rgba(255,255,255,0.15)',
                    )
                ),
                showlegend=False,
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=60, r=60, t=30, b=30),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Profile Comparison")
            st.markdown("*Comparing with MUJ student averages*")
            metrics = [
                ("Exam Score", st.session_state['input_data']['ExamScore'], 75, "📋"),
                ("Attendance", st.session_state['input_data']['Attendance'], 85, "📊"),
                ("Study Hours", st.session_state['input_data']['StudyHours'], 20, "📚"),
                ("Assignment Completion", st.session_state['input_data']['AssignmentCompletion'], 85, "📝")
            ]
            
            for name, value, avg, icon in metrics:
                diff = value - avg
                diff_color = "#10B981" if diff > 0 else "#EF4444" if diff < 0 else "#64748B"
                bg_color = "rgba(16,185,129,.1)" if diff > 0 else "rgba(239,68,68,.1)" if diff < 0 else "rgba(100,116,139,.1)"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:12px 16px; border:1px solid var(--border-color);
                    border-radius:12px; margin-bottom:8px; background:var(--card-bg);">
                    <span style="font-size:1.1rem">{icon}</span>
                    <span style="font-size:.85rem; color:var(--text-muted); flex:1; margin-left:10px">{name}</span>
                    <span style="font-weight:700; color:var(--text-primary); margin-right:10px">{value}</span>
                    <span style="font-size:.78rem; color:{diff_color}; background:{bg_color};
                        padding:3px 10px; border-radius:20px">
                            {"+" if diff > 0 else ""}{diff:.1f} vs avg
                    </span>
                </div>
                """, unsafe_allow_html=True)            
            # Environmental Impact
            st.markdown("#### 🔍 Environmental Impact")
            impact_data = pd.DataFrame({
                "Factor": ["Internet", "Resources", "EduTech", "Extra-Curricular"],
                "Score": [
                    st.session_state['input_data']['Internet'] * 100,
                    (st.session_state['input_data']['Resources'] / 2) * 100,
                    st.session_state['input_data']['EduTech'] * 100,
                    50 if st.session_state['input_data']['Extracurricular'] == 1 else 0
                ]
            })
            
            fig_impact = px.bar(impact_data, x='Factor', y='Score', 
                               color='Score', color_continuous_scale='Viridis',
                               title='Environmental Factor Impact',
                               template=get_plotly_template())
            fig_impact.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_impact, use_container_width=True)
            
            # Stress Impact
            stress_level = st.session_state['input_data']['StressLevel']
            stress_impact = {
                0: "✨ **Low Stress**: Students with low stress typically perform 10-15% better",
                1: "⚖️ **Moderate Stress**: Can be motivating if managed well",
                2: "⚠️ **High Stress**: Reduces performance by 20-30% - intervene immediately"
            }
            st.markdown("#### 🧠 Stress Impact Analysis")
            st.info(stress_impact[stress_level])
    else:
        st.info("👆 Generate a prediction first to see detailed analysis")

with tab3:
    st.markdown('<h2 class="sub-header">📚 MUJ Student Success Guidelines</h2>', unsafe_allow_html=True)
    
    # Display guidelines
    categories = [
        (0, "#10B981", "🌟 GRADE CATEGORY 0 (Highest Performers)"),
        (1, "#3B82F6", "📈 GRADE CATEGORY 1 (Above Average)"),
        (2, "#F59E0B", "⚠️ GRADE CATEGORY 2 (Below Average)"),
        (3, "#EF4444", "🚨 GRADE CATEGORY 3 (At-Risk)")
    ]
    
    guidelines_text = guidelines.split('\n\n')
    for i, (grade_num, color, title) in enumerate(categories):
        st.markdown(f"""
        <div class="contact-card" style="margin-bottom: 1.5rem; border-left: 4px solid {color};">
            <h3 style="color: {color};">{title}</h3>
        """, unsafe_allow_html=True)
        
        # Find the relevant section
        for section in guidelines_text:
            if f"GRADE CATEGORY {grade_num}" in section:
                for line in section.split('\n')[1:]:
                    if line.strip():
                        if line.strip().startswith('-'):
                            st.markdown(f'<div class="recommendation-item" style="margin: 5px 0;">✅ {line.strip()[1:].strip()}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"**{line.strip()}**")
                break
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Download Guidelines PDF", 
        data=guidelines, 
        file_name="MUJ_Guidelines.txt", 
        mime="text/plain", 
        use_container_width=True
    )

with tab4:
    st.markdown('<h2 class="sub-header">ℹ️ About This System</h2>', unsafe_allow_html=True)
    
    st.markdown("""
<div class="contact-card">
    <h3 style="color: #667eea;">🎯 System Purpose</h3>
    <p style="line-height: 1.8; font-size: 1rem; margin-bottom: 1.5rem;">
        The <strong>MUJ Student Advisor AI</strong> transforms academic advising 
        from reactive to predictive by analyzing 15 factors across academic, 
        psychological, and environmental domains — enabling advisors to intervene 
        early, allocate resources effectively, and ensure every student gets the 
        support they need before it's too late.
    </p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Identify at-risk students early</span>
        </div>
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Generate personalized interventions</span>
        </div>
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Optimize resource allocation</span>
        </div>
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Ensure fair assessment across demographics</span>
        </div>
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Support faculty with data-driven insights</span>
        </div>
        <div class="recommendation-item" style="display:flex; gap:10px; align-items:flex-start; padding:12px 16px; font-size:.875rem;">
            <span style="flex-shrink:0;">✅</span><span>Reduce student dropout rates proactively</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Model Architecture
    st.markdown("""
    <div class="contact-card" style="margin-top: 1.5rem;">
        <h3 style="color: #667eea;">🛠️ Technical Architecture</h3>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
            <div class="metric-card"><span class="metric-icon">🌲</span><div class="metric-label">Algorithm</div><div class="metric-value" style="font-size: 1.2rem;">Random Forest</div></div>
            <div class="metric-card"><span class="metric-icon">📊</span><div class="metric-label">Features</div><div class="metric-value" style="font-size: 1.2rem;">15 Factors</div></div>
            <div class="metric-card"><span class="metric-icon">📈</span><div class="metric-label">Accuracy</div><div class="metric-value" style="font-size: 1.2rem;">99%</div></div>
            <div class="metric-card"><span class="metric-icon">⚡</span><div class="metric-label">Response</div><div class="metric-value" style="font-size: 1.2rem;"><0.5s</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎓 MUJ Student Advisor AI</div>
    <div style="margin-bottom: 0.5rem;">Developed for IEEE CIS AI Model Quest 2.0 | PS 01: Student Academic Performance Prediction</div>
    <div>📍 Manipal University Jaipur | Department of Computer Science & Engineering</div>
    <div style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-secondary);">© 2026 All Rights Reserved</div>
</div>
""", unsafe_allow_html=True)
