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

# Initialize session state variables
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'study_mode' not in st.session_state:
    st.session_state.study_mode = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(int(time.time()))
if 'display_counter' not in st.session_state:
    st.session_state.display_counter = 0
if 'test_start_time' not in st.session_state:
    st.session_state.test_start_time = None
if 'quick_review_questions' not in st.session_state:
    st.session_state.quick_review_questions = []
if 'deep_study_questions' not in st.session_state:
    st.session_state.deep_study_questions = []
if 'revision_questions' not in st.session_state:
    st.session_state.revision_questions = []
if 'test_prep_questions' not in st.session_state:
    st.session_state.test_prep_questions = []
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = None

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

# Process file if uploaded
if uploaded_file and 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = uploaded_file.name
    try:
        with st.spinner("Processing document..."):
            start_time = time.time()
            
            # Extract and preprocess text
            text = pdf_processor.extract_text(uploaded_file)
            processed_text = pdf_processor.preprocess_text(text)
            
            # Store processed text for later use
            st.session_state.processed_text = processed_text
            
            # Generate questions sequentially instead of parallel for now
            st.info("Generating questions (this may take a few minutes)...")
            progress_text = st.empty()
            
            # Quick review questions
            progress_text.text("Generating quick review questions...")
            st.session_state.quick_review_questions = pdf_processor.generate_basic_questions(
                processed_text, num_questions=3
            )
            
            # Deep study questions
            progress_text.text("Generating deep study questions...")
            st.session_state.deep_study_questions = pdf_processor.generate_basic_questions(
                processed_text, num_questions=5
            )
            
            # Revision questions
            progress_text.text("Generating revision questions...")
            st.session_state.revision_questions = pdf_processor.generate_basic_questions(
                processed_text, num_questions=5
            )
            
            # Test prep questions
            progress_text.text("Generating test prep questions...")
            st.session_state.test_prep_questions = pdf_processor.generate_basic_questions(
                processed_text, num_questions=10
            )
            
            processing_time = time.time() - start_time
            st.success(f"✅ Questions generated in {processing_time:.1f} seconds!")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        print(f"Error processing document: {str(e)}")

def display_questions(questions: List[dict], mode: StudyMode):
    """Display questions based on study mode"""
    print(f"Displaying {len(questions)} questions in mode {mode}")
    
    if not questions:
        st.warning("Please upload a document first.")
        return

    if mode == StudyMode.QUICK_REVIEW:
        # Show fewer questions with immediate feedback
        for i, q in enumerate(questions[:3], 1):
            with st.expander(f"Q{i}: {q['type'].title()} ({q['difficulty']})"):
                st.markdown(f"**{q['question']}**")
                answer = st.text_area(
                    "Your Answer", 
                    key=f"qr_ans_{i}_{st.session_state.session_id}"
                )
                if st.button("Check", key=f"qr_check_{i}_{st.session_state.session_id}"):
                    show_feedback(i, q, answer)

    elif mode == StudyMode.DEEP_STUDY:
        for i, q in enumerate(questions, 1):
            with st.expander(f"Q{i}: {q['type'].title()} ({q['difficulty']})"):
                st.markdown(f"**{q['question']}**")
                st.info("Context: " + q['context'])
                answer = st.text_area(
                    "Your Answer", 
                    key=f"ds_ans_{i}_{st.session_state.session_id}"
                )
                if st.button("Detailed Feedback", key=f"ds_check_{i}_{st.session_state.session_id}"):
                    show_detailed_feedback(i, q, answer)

    elif mode == StudyMode.REVISION:
        for i, q in enumerate(questions, 1):
            with st.expander(f"Q{i}: {q['type'].title()} ({q['difficulty']})"):
                st.markdown(f"**{q['question']}**")
                if st.button("Show Hint", 
                    key=f"{st.session_state.session_id}_{mode.value}_hint_{i}"):
                    st.info("Hint: Look for key terms in: " + q['context'][:100] + "...")
                answer = st.text_area("Your Answer", 
                    key=f"{st.session_state.session_id}_{mode.value}_ans_{i}")
                if st.button("Check & Improve", 
                    key=f"{st.session_state.session_id}_{mode.value}_check_{i}"):
                    show_progressive_feedback(i, q, answer)

    elif mode == StudyMode.TEST_PREP:
        if 'test_start_time' not in st.session_state:
            st.session_state.test_start_time = time.time()
        
        time_remaining = 30 * 60 - (time.time() - st.session_state.test_start_time)
        if time_remaining > 0:
            st.progress(time_remaining / (30 * 60))
            st.write(f"Time remaining: {int(time_remaining/60)}:{int(time_remaining%60):02d}")
            
            for i, q in enumerate(questions, 1):
                with st.expander(f"Q{i}: {q['type'].title()}"):
                    st.markdown(f"**{q['question']}**")
                    st.session_state.answers[i] = st.text_area(
                        "Your Answer", 
                        value=st.session_state.answers.get(i, ""),
                        key=f"{st.session_state.session_id}_{mode.value}_ans_{i}"
                    )
            
            if st.button("Submit Test", 
                key=f"{st.session_state.session_id}_{mode.value}_submit"):
                show_test_results()
        else:
            st.warning("Time's up! Here are your results:")
            show_test_results()

def show_feedback(question_id: int, question: dict, answer: str):
    """Show focused feedback for an answer"""
    if not answer.strip():
        st.warning("Please write an answer first!")
        return
        
    with st.spinner("Checking your answer..."):
        validation = pdf_processor.validate_answer(question["question"], question["context"], answer)
        if validation:
            # Show score with color
            score = validation['score']
            if score >= 80:
                st.success(f"Score: {score}%")
            elif score >= 60:
                st.warning(f"Score: {score}%")
            else:
                st.error(f"Score: {score}%")
            
            # Show feedback
            st.info(validation['feedback'])
            
            # Show strengths and improvements in columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Strengths:**")
                for point in validation['strengths']:
                    st.write(f"• {point}")
            
            with col2:
                st.markdown("**🎯 Areas to Improve:**")
                for point in validation['improvements']:
                    st.write(f"• {point}")
            
            # Show quick tip
            st.info(f"💡 Quick Tip: {validation['tip']}")
            
            # Update progress
            if score >= 70:
                st.session_state.questions_answered += 1
                st.balloons()

def show_detailed_feedback(question_id: int, question: dict, answer: str):
    """Deep Study mode - Show comprehensive feedback"""
    if not answer.strip():
        st.warning("Please write an answer first!")
        return
        
    with st.spinner("Analyzing your answer..."):
        validation = pdf_processor.validate_answer(question["question"], question["context"], answer)
        if validation:
            # Score and main feedback
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Score", f"{validation['score']}%")
            with col2:
                st.info(validation['feedback'])
            
            # Key points covered
            if validation['strengths']:
                st.markdown("#### ✅ Key Points Covered")
                for point in validation['strengths']:
                    st.success(f"• {point}")
            
            # Missing elements
            if validation['improvements']:
                st.markdown("#### 🔍 Missing Elements")
                for point in validation['improvements']:
                    st.warning(f"• {point}")
            
            # Show quick tip
            st.info(f"💡 Quick Tip: {validation['tip']}")
            
            # Update progress
            if validation['score'] >= 70:
                st.session_state.questions_answered += 1
                st.balloons()

def show_progressive_feedback(question_id: int, question: dict, answer: str):
    """Revision mode - Show step-by-step feedback"""
    if not answer.strip():
        st.warning("Please write an answer first!")
        return
        
    with st.spinner("Analyzing..."):
        validation = pdf_processor.validate_answer(question["question"], question["context"], answer)
        if validation:
            # Initial score
            st.metric("Current Score", f"{validation['score']}%")
            
            # Progressive feedback tabs
            tab1, tab2, tab3 = st.tabs(["Initial Feedback", "Detailed Analysis", "Improvement Plan"])
            
            with tab1:
                st.info(validation['feedback'])
            
            with tab2:
                if validation['strengths']:
                    st.success("✅ You've covered these key points:")
                    for point in validation['strengths']:
                        st.write(f"• {point}")
                
                if validation['improvements']:
                    st.warning("🎯 Focus on these areas:")
                    for point in validation['improvements']:
                        st.write(f"• {point}")
            
            with tab3:
                if validation['improvements']:
                    st.markdown("#### Your Improvement Plan:")
                    for i, suggestion in enumerate(validation['improvements'], 1):
                        st.info(f"Step {i}: {suggestion}")
                
                with st.expander("💡 Study Tip"):
                    st.write("Try rewriting your answer incorporating the feedback, then check again!")
            
            if validation['score'] >= 70:
                st.session_state.questions_answered += 1
                st.balloons()

def show_test_results():
    """Test Prep mode - Show comprehensive test results"""
    if not st.session_state.answers:
        st.error("No answers submitted yet!")
        return
        
    st.markdown("### 📊 Test Results")
    total_score = 0
    num_questions = len(st.session_state.answers)
    
    for i, (question_id, answer) in enumerate(st.session_state.answers.items(), 1):
        with st.expander(f"Question {i}"):
            question = st.session_state.test_prep_questions[question_id-1]
            validation = pdf_processor.validate_answer(
                question["question"],
                question["context"],
                answer
            )
            
            if validation:
                score = validation['score']
                total_score += score
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Score", f"{score}%")
                with col2:
                    st.write(validation['feedback'])
                
                if validation['strengths']:
                    st.success("✅ Correct Elements")
                    for point in validation['strengths']:
                        st.write(f"• {point}")
                
                if validation['improvements']:
                    st.warning("❌ Areas for Improvement")
                    for point in validation['improvements']:
                        st.write(f"• {point}")
    
    # Overall results
    avg_score = total_score / num_questions if num_questions > 0 else 0
    st.metric("Final Score", f"{avg_score:.1f}%")


# Show mode buttons if we have questions
if any([
    st.session_state.quick_review_questions,
    st.session_state.deep_study_questions,
    st.session_state.revision_questions,
    st.session_state.test_prep_questions
]):
    # Study modes with functionality
    modes = st.columns(4)
    with modes[0]: 
        if st.button("🎯 Quick Review", use_container_width=True):
            st.session_state.study_mode = StudyMode.QUICK_REVIEW
            display_questions(st.session_state.quick_review_questions, StudyMode.QUICK_REVIEW)

    with modes[1]: 
        if st.button("📝 Deep Study", use_container_width=True):
            st.session_state.study_mode = StudyMode.DEEP_STUDY
            display_questions(st.session_state.deep_study_questions, StudyMode.DEEP_STUDY)

    with modes[2]:
        if st.button("🔄 Revision", use_container_width=True):
            st.session_state.study_mode = StudyMode.REVISION
            display_questions(st.session_state.revision_questions, StudyMode.REVISION)

    with modes[3]:
        if st.button("📊 Test Prep", use_container_width=True):
            st.session_state.study_mode = StudyMode.TEST_PREP
            display_questions(st.session_state.test_prep_questions, StudyMode.TEST_PREP)
else:
    st.info("Upload a PDF to get started!")

# Minimal footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Made with ❤️ for Nigerian Students | "
    "<a href='/'>Help</a> | "
    "<a href='/'>Feedback</a>"
    "</div>",
    unsafe_allow_html=True
)

