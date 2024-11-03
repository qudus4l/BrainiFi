# Imports first
import streamlit as st
import requests
import io
from datetime import datetime
from enum import Enum
from typing import Optional, List
import time
from services.pdf_processor import PDFProcessor
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize session state variables FIRST
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(int(time.time()))
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'hints_shown' not in st.session_state:
    st.session_state.hints_shown = set()
if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False
if 'quick_review_questions' not in st.session_state:
    st.session_state.quick_review_questions = []
if 'deep_study_questions' not in st.session_state:
    st.session_state.deep_study_questions = []
if 'revision_questions' not in st.session_state:
    st.session_state.revision_questions = []
if 'test_prep_questions' not in st.session_state:
    st.session_state.test_prep_questions = []

# Helper functions first
async def generate_questions_async(processor, text, num_questions):
    """Generate questions asynchronously"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(
            pool, 
            processor.generate_basic_questions,
            text,
            num_questions
        )

def check_model_availability():
    """Check if BitNet model is available"""
    model_path = "/Users/Q/Projects/BrainiFi/BitNet/models/bitnet_b1_58-large/ggml-model-i2_s.gguf"
    if not os.path.exists(model_path):
        st.error(f"""
        BitNet model not found! Please ensure you have:
        1. Downloaded the model using setup_env.py
        2. Placed it in the correct directory: 
           {model_path}
        """)
        return False
    return True

# Define study modes
class StudyMode(Enum):
    QUICK_REVIEW = "quick_review"
    DEEP_STUDY = "deep_study"
    REVISION = "revision"
    TEST_PREP = "test_prep"

# Initialize services
pdf_processor = PDFProcessor()

# Page configuration
st.set_page_config(
    page_title="BrainiFi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1 { color: #1E3A8A; }
    h2, h3 { color: #2563EB; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #F3F4F6;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .question-box {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def set_mode(mode: StudyMode):
    st.session_state.current_mode = mode

# Sidebar
with st.sidebar:
    st.image("logo.webp", width=150)
    
    # Add model status indicator
    if check_model_availability():
        st.success("✅ BitNet Model Loaded")
    else:
        st.error("❌ BitNet Model Not Found")
    
    # Core study progress
    st.markdown("### 📊 Progress")
    st.progress(min(st.session_state.questions_answered / 5, 1.0))
    st.caption(f"Questions: {st.session_state.questions_answered}/5")

# Main content
st.title("📚 BrainiFi")

# File upload
uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="pdf_uploader")

# Process file if uploaded and questions not yet generated
if uploaded_file and not st.session_state.questions_generated:
    try:
        with st.spinner("Processing document..."):
            # Extract and preprocess text
            text = pdf_processor.extract_text(uploaded_file)
            processed_text = pdf_processor.preprocess_text(text)
            
            # Generate questions for each mode
            with st.status("Generating questions..."):
                st.write("Quick review questions...")
                st.session_state.quick_review_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=3
                )
                
                st.write("Deep study questions...")
                st.session_state.deep_study_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=5
                )
                
                st.write("Revision questions...")
                st.session_state.revision_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=5
                )
                
                st.write("Test prep questions...")
                st.session_state.test_prep_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=5
                )
            
            st.session_state.questions_generated = True
            st.success("✅ Questions generated successfully!")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")

def handle_check_answer(question, answer, key):
    """Callback for checking answers"""
    if not answer.strip():
        st.warning("Please write an answer first!")
        return
    
    feedback = pdf_processor.validate_answer(
        question["question"], 
        question["context"], 
        answer
    )
    st.session_state[f"feedback_{key}"] = feedback

def handle_hint_toggle(key):
    """Callback for toggling hints"""
    if key not in st.session_state:
        st.session_state[key] = False
    st.session_state[key] = not st.session_state[key]

def display_questions(questions: List[dict], mode: StudyMode):
    """Display questions based on study mode"""
    if not questions:
        st.warning("Please upload a document first.")
        return

    if mode == StudyMode.QUICK_REVIEW:
        for i, q in enumerate(questions[:3], 1):
            with st.expander(f"Q{i}: {q['type'].title()} ({q['difficulty']})"):
                st.markdown(f"**{q['question']}**")
                
                # Answer input
                answer_key = f"qr_ans_{i}"
                if answer_key not in st.session_state:
                    st.session_state[answer_key] = ""
                
                st.session_state[answer_key] = st.text_area(
                    "Your Answer",
                    key=answer_key
                )
                
                # Check button
                if st.button("Check", key=f"check_{i}"):
                    handle_check_answer(q, st.session_state[answer_key], answer_key)
                
                # Show feedback if available
                feedback_key = f"feedback_{answer_key}"
                if feedback_key in st.session_state:
                    feedback = st.session_state[feedback_key]
                    st.metric("Score", f"{feedback['score']}%")
                    st.info(feedback['feedback'])
                    st.success("✅ " + " | ".join(feedback['strengths']))
                    st.warning("🎯 " + " | ".join(feedback['improvements']))

    elif mode == StudyMode.REVISION:
        for i, q in enumerate(questions, 1):
            with st.expander(f"Q{i}: {q['type'].title()} ({q['difficulty']})"):
                st.markdown(f"**{q['question']}**")
                
                # Hint button
                hint_key = f"hint_{i}"
                if st.button("Show/Hide Hint", key=f"hint_btn_{i}"):
                    handle_hint_toggle(hint_key)
                
                if hint_key in st.session_state and st.session_state[hint_key]:
                    st.info(f"💡 Hint: {q['hint']}")
                
                # Answer input
                answer_key = f"rev_ans_{i}"
                if answer_key not in st.session_state:
                    st.session_state[answer_key] = ""
                
                st.session_state[answer_key] = st.text_area(
                    "Your Answer",
                    key=answer_key
                )
                
                # Check button
                if st.button("Check & Improve", key=f"check_{i}"):
                    handle_check_answer(q, st.session_state[answer_key], answer_key)
                
                # Show feedback if available
                feedback_key = f"feedback_{answer_key}"
                if feedback_key in st.session_state:
                    feedback = st.session_state[feedback_key]
                    st.info(feedback['feedback'])
                    st.success("✅ " + " | ".join(feedback['strengths']))
                    st.warning("🎯 " + " | ".join(feedback['improvements']))

# Show mode buttons if we have questions
if st.session_state.questions_generated:
    modes = st.columns(4)
    with modes[0]: 
        if st.button("🎯 Quick Review", use_container_width=True):
            set_mode(StudyMode.QUICK_REVIEW)

    with modes[1]: 
        if st.button("📝 Deep Study", use_container_width=True):
            set_mode(StudyMode.DEEP_STUDY)

    with modes[2]:
        if st.button("🔄 Revision", use_container_width=True):
            set_mode(StudyMode.REVISION)

    with modes[3]:
        if st.button("📊 Test Prep", use_container_width=True):
            set_mode(StudyMode.TEST_PREP)

    # Display questions for current mode
    if st.session_state.current_mode == StudyMode.QUICK_REVIEW:
        display_questions(st.session_state.quick_review_questions, StudyMode.QUICK_REVIEW)
    elif st.session_state.current_mode == StudyMode.DEEP_STUDY:
        display_questions(st.session_state.deep_study_questions, StudyMode.DEEP_STUDY)
    elif st.session_state.current_mode == StudyMode.REVISION:
        display_questions(st.session_state.revision_questions, StudyMode.REVISION)
    elif st.session_state.current_mode == StudyMode.TEST_PREP:
        display_questions(st.session_state.test_prep_questions, StudyMode.TEST_PREP)
else:
    st.info("Upload a PDF to get started!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Made with ❤️ for Nigerian Students"
    "</div>",
    unsafe_allow_html=True
)

