# Imports first
import streamlit as st
import requests
import io
from datetime import datetime
from enum import Enum
from typing import Optional, List
import time
from services.ai_service import AIService
from services.pdf_processor import PDFProcessor

# Initialize session state variables FIRST
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

# THEN Define study modes
class StudyMode(Enum):
    QUICK_REVIEW = "quick_review"
    DEEP_STUDY = "deep_study"
    REVISION = "revision"
    TEST_PREP = "test_prep"

# THEN initialize services
ai_service = AIService()
pdf_processor = PDFProcessor()

# THEN all the function definitions
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
        validation = validate_answer(question_id, question["question"], question["context"], answer)
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
        validation = validate_answer(question_id, question["question"], question["context"], answer)
        if validation:
            # Score and main feedback
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Score", f"{validation['score']}%")
            with col2:
                st.info(validation['main_feedback'])
            
            # Key points covered
            if validation['key_points_covered']:
                st.markdown("#### ✅ Key Points Covered")
                for point in validation['key_points_covered']:
                    st.success(f"• {point}")
            
            # Missing elements
            if validation['missing_elements']:
                st.markdown("#### 🔍 Missing Elements")
                for point in validation['missing_elements']:
                    st.warning(f"• {point}")
            
            # Improvement suggestions
            if validation['improvement_suggestions']:
                st.markdown("#### 💡 How to Improve")
                for suggestion in validation['improvement_suggestions']:
                    st.info(f"• {suggestion}")
            
            # Sample answer
            if validation['sample_answer']:
                with st.expander("📝 Sample Answer"):
                    st.write(validation['sample_answer'])
            
            if validation['score'] >= 70:
                handle_feedback(question_id, True)

def show_progressive_feedback(question_id: int, question: dict, answer: str):
    """Revision mode - Show step-by-step feedback"""
    if not answer.strip():
        st.warning("Please write an answer first!")
        return
        
    with st.spinner("Analyzing..."):
        validation = validate_answer(question_id, question["question"], question["context"], answer)
        if validation:
            # Initial score
            st.metric("Current Score", f"{validation['score']}%")
            
            # Progressive feedback tabs
            tab1, tab2, tab3 = st.tabs(["Initial Feedback", "Detailed Analysis", "Improvement Plan"])
            
            with tab1:
                st.info(validation['main_feedback'])
            
            with tab2:
                if validation['key_points_covered']:
                    st.success("✅ You've covered these key points:")
                    for point in validation['key_points_covered']:
                        st.write(f"• {point}")
                
                if validation['missing_elements']:
                    st.warning("🎯 Focus on these areas:")
                    for point in validation['missing_elements']:
                        st.write(f"• {point}")
            
            with tab3:
                if validation['improvement_suggestions']:
                    st.markdown("#### Your Improvement Plan:")
                    for i, suggestion in enumerate(validation['improvement_suggestions'], 1):
                        st.info(f"Step {i}: {suggestion}")
                
                with st.expander("💡 Study Tip"):
                    st.write("Try rewriting your answer incorporating the feedback, then check again!")
            
            if validation['score'] >= 70:
                handle_feedback(question_id, True)

def show_test_results():
    """Test Prep mode - Show comprehensive test results"""
    if 'current_questions' not in st.session_state:
        st.error("No questions found. Please upload a document first.")
        return
        
    total_score = 0
    num_questions = len(st.session_state.answers)
    
    st.markdown("### 📊 Test Results")
    
    for i, (question_id, answer) in enumerate(st.session_state.answers.items(), 1):
        with st.expander(f"Question {i}"):
            question = st.session_state.current_questions[question_id-1]
            validation = validate_answer(
                question_id,
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
                    st.write(validation['main_feedback'])
                
                if validation['key_points_covered']:
                    st.success("✅ Correct Elements")
                    for point in validation['key_points_covered']:
                        st.write(f"• {point}")
                
                if validation['missing_elements']:
                    st.warning("❌ Areas for Improvement")
                    for point in validation['missing_elements']:
                        st.write(f"• {point}")
    
    # Overall results
    avg_score = total_score / num_questions if num_questions > 0 else 0
    st.metric("Final Score", f"{avg_score:.1f}%")
    
    # Performance breakdown
    st.markdown("### 📈 Performance Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions Completed", f"{num_questions}")
    with col2:
        time_taken = time.time() - st.session_state.test_start_time
        st.metric("Time Taken", f"{int(time_taken/60)}:{int(time_taken%60):02d}")
    
    # Reset button
    if st.button("Start New Test"):
        set_study_mode(None)

def validate_answer(question_id: int, question: str, context: str, answer: str):
    """Validate answer using AI service directly"""
    try:
        return ai_service.validate_answer(question, context, answer)
    except Exception as e:
        st.error(f"Error validating answer: {str(e)}")
        return None

def handle_feedback(question_id: int, is_helpful: bool):
    """Handle feedback for questions"""
    st.session_state.feedback[question_id] = is_helpful
    if is_helpful:
        st.session_state.questions_answered += 1

def save_answer(question_id: int, answer: str):
    """Save answer to session state"""
    if answer.strip():  # Only save non-empty answers
        st.session_state.answers[question_id] = answer

def set_study_mode(mode: StudyMode):
    """Set study mode and handle question display"""
    print(f"Setting study mode to: {mode}")  # Debug log
    st.session_state.study_mode = mode
    st.session_state.questions_answered = 0
    st.session_state.answers = {}
    st.session_state.feedback = {}
    
    # Display existing questions if available
    if mode and 'current_questions' in st.session_state:
        print(f"Displaying existing questions in new mode: {mode}")  # Debug log
        display_questions(st.session_state.current_questions, mode)

# THEN the rest of the UI code
# Page configuration
st.set_page_config(
    page_title="BrainiFi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS - removed unnecessary styles
st.markdown("""
    <style>
    /* Core styles only */
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

# Simplified sidebar
with st.sidebar:
    st.image("logo.webp", width=150)
    
    # Core study progress
    st.markdown("### 📊 Progress")
    st.progress(min(st.session_state.questions_answered / 5, 1.0))
    st.caption(f"Questions: {st.session_state.questions_answered}/5")
    
    # Essential features in collapsible sections
    with st.expander("📚 Documents"):
        st.selectbox("Course", ["CSC 301", "MTH 305", "PHY 202", "+ Add"])
        st.selectbox("Term", ["1st Sem 2024", "2nd Sem 2024"])
    
    with st.expander("🎯 Goals"):
        st.checkbox("Complete 5 questions")
        st.checkbox("Review chapter")
        st.button("+ Add")

# Main content
st.title("📚 BrainiFi")

# File upload FIRST
uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="pdf_uploader")

# Process file if uploaded
if uploaded_file and 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = uploaded_file.name
    try:
        with st.spinner("Processing document..."):
            # Extract and preprocess text
            text = pdf_processor.extract_text(uploaded_file)
            processed_text = pdf_processor.preprocess_text(text)
            
            # Store processed text for later use
            st.session_state.processed_text = processed_text
            
            # Generate questions for each mode
            with st.progress(0) as progress_bar:
                st.session_state.quick_review_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=3)
                progress_bar.progress(0.25)
                
                st.session_state.deep_study_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=5)
                progress_bar.progress(0.5)
                
                st.session_state.revision_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=5)
                progress_bar.progress(0.75)
                
                st.session_state.test_prep_questions = pdf_processor.generate_basic_questions(
                    processed_text, num_questions=10)
                progress_bar.progress(1.0)
            
            st.success("Questions generated! Select a study mode to begin.")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        print(f"Error processing document: {str(e)}")

# THEN show mode buttons only if we have questions
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

    # Show current mode and "Generate More" button
    if st.session_state.study_mode:
        st.info(f"Current Mode: {st.session_state.study_mode.name.replace('_', ' ').title()}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("💡 Click 'Generate More Questions' to get additional questions for this mode.")
        
        with col2:
            if st.button("🔄 Generate More Questions"):
                with st.spinner("Generating additional questions..."):
                    if st.session_state.study_mode == StudyMode.QUICK_REVIEW:
                        new_questions = pdf_processor.generate_basic_questions(
                            st.session_state.processed_text, 
                            num_questions=3
                        )
                        st.session_state.quick_review_questions.extend(new_questions)
                        display_questions(st.session_state.quick_review_questions, StudyMode.QUICK_REVIEW)
                        st.success(f"Added {len(new_questions)} new questions!")
                    
                    elif st.session_state.study_mode == StudyMode.DEEP_STUDY:
                        new_questions = pdf_processor.generate_basic_questions(
                            st.session_state.processed_text, 
                            num_questions=5
                        )
                        st.session_state.deep_study_questions.extend(new_questions)
                        display_questions(st.session_state.deep_study_questions, StudyMode.DEEP_STUDY)
                        st.success(f"Added {len(new_questions)} new questions!")
                    
                    elif st.session_state.study_mode == StudyMode.REVISION:
                        new_questions = pdf_processor.generate_basic_questions(
                            st.session_state.processed_text, 
                            num_questions=5
                        )
                        st.session_state.revision_questions.extend(new_questions)
                        display_questions(st.session_state.revision_questions, StudyMode.REVISION)
                        st.success(f"Added {len(new_questions)} new questions!")
                    
                    elif st.session_state.study_mode == StudyMode.TEST_PREP:
                        new_questions = pdf_processor.generate_basic_questions(
                            st.session_state.processed_text, 
                            num_questions=10
                        )
                        st.session_state.test_prep_questions.extend(new_questions)
                        display_questions(st.session_state.test_prep_questions, StudyMode.TEST_PREP)
                        st.success(f"Added {len(new_questions)} new questions!")
else:
    st.info("Upload a PDF to get started!")

# Minimal footer with centered text
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Made with ❤️ for Nigerian Students | "
    "<a href='/'>Help</a> | "
    "<a href='/'>Feedback</a>"
    "</div>",
    unsafe_allow_html=True
)
