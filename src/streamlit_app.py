import streamlit as st
import requests
import io
from datetime import datetime
from enum import Enum
from typing import Optional

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

# Define study modes
class StudyMode(Enum):
    QUICK_REVIEW = "quick_review"
    DEEP_STUDY = "deep_study"
    REVISION = "revision"
    TEST_PREP = "test_prep"

# Initialize session state
if 'study_start_time' not in st.session_state:
    st.session_state.study_start_time = datetime.now()
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'study_mode' not in st.session_state:
    st.session_state.study_mode = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

# Mode selection handlers
def set_study_mode(mode: StudyMode):
    st.session_state.study_mode = mode
    st.session_state.questions_answered = 0
    st.session_state.answers = {}
    st.session_state.feedback = {}

# Feedback handlers
def handle_feedback(question_id: int, is_helpful: bool):
    st.session_state.feedback[question_id] = is_helpful
    if is_helpful:
        st.session_state.questions_answered += 1

# Answer handlers
def save_answer(question_id: int, answer: str):
    if answer.strip():  # Only save non-empty answers
        st.session_state.answers[question_id] = answer

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

# Main content - streamlined layout
st.title("📚 BrainiFi")

# Study modes with functionality
modes = st.columns(4)
with modes[0]: 
    if st.button("🎯 Quick Review", use_container_width=True):
        set_study_mode(StudyMode.QUICK_REVIEW)
with modes[1]: 
    if st.button("📝 Deep Study", use_container_width=True):
        set_study_mode(StudyMode.DEEP_STUDY)
with modes[2]: 
    if st.button("🔄 Revision", use_container_width=True):
        set_study_mode(StudyMode.REVISION)
with modes[3]: 
    if st.button("📊 Test Prep", use_container_width=True):
        set_study_mode(StudyMode.TEST_PREP)

# Show current mode
if st.session_state.study_mode:
    st.info(f"Current Mode: {st.session_state.study_mode.name.replace('_', ' ').title()}")

# Simplified file upload
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    try:
        with st.spinner("Processing..."):
            files = {"file": ("document.pdf", uploaded_file, "application/pdf")}
            
            # Add error logging
            st.write("Sending file to server...")
            response = requests.post(
                "http://localhost:8000/upload-pdf/",
                files=files,
                params={"course_code": st.session_state.get('selected_course', '')}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Document processed successfully!")
                
                # Simplified tabs
                tab1, tab2 = st.tabs(["📄 Content", "❓ Questions"])
                
                with tab1:
                    st.text_area("Extracted Text", data["text"], height=300)
                    st.download_button("💾 Save", data["text"], "text.txt")
                
                with tab2:
                    # Adjust question display based on study mode
                    questions = data["questions"]
                    if st.session_state.study_mode == StudyMode.QUICK_REVIEW:
                        questions = questions[:3]  # Show fewer questions
                    elif st.session_state.study_mode == StudyMode.TEST_PREP:
                        # Shuffle questions and add time limit
                        import random
                        random.shuffle(questions)
                    
                    for i, q in enumerate(questions, 1):
                        with st.expander(
                            f"Q{i}: {q['type'].title()} ({q.get('difficulty', 'Medium')})"
                        ):
                            st.markdown(f"**{q['question']}**")
                            
                            # Get previous answer if it exists
                            previous_answer = st.session_state.answers.get(i, "")
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                answer = st.text_area(
                                    "Your Answer", 
                                    value=previous_answer,
                                    key=f"ans_{i}",
                                    height=100
                                )
                            
                            with col2:
                                if st.button("Submit & Validate", key=f"validate_{i}"):
                                    if answer.strip():
                                        with st.spinner("Analyzing your answer..."):
                                            validation = validate_answer(
                                                i, q["question"], q["context"], answer
                                            )
                                            if validation:
                                                # Store answer and show feedback
                                                save_answer(i, answer)
                                                
                                                # Show accuracy
                                                st.metric("Accuracy", f"{validation['accuracy']}%")
                                                
                                                # Show feedback
                                                if validation['feedback']:
                                                    st.markdown("#### Feedback")
                                                    st.info(validation['feedback'])
                                                
                                                # Show missed points if any
                                                if validation['key_points_missed']:
                                                    st.markdown("#### Key Points Missed")
                                                    st.warning(validation['key_points_missed'])
                                                
                                                # Show suggestions
                                                if validation['suggestions']:
                                                    st.markdown("#### Suggestions")
                                                    st.success(validation['suggestions'])
                                                
                                                # Update progress
                                                if validation['accuracy'] >= 70:
                                                    handle_feedback(i, True)
                                    else:
                                        st.warning("Please write an answer first!")
                            
                            # Show context based on mode
                            if st.session_state.study_mode != StudyMode.TEST_PREP:
                                st.markdown("#### Reference Context")
                                st.info(q['context'])
                            
                            # Show progress if answer was validated
                            if i in st.session_state.feedback:
                                st.progress(1.0)
                    
                    # Show completion message
                    if st.session_state.questions_answered == len(questions):
                        st.balloons()
                        st.success("🎉 Congratulations! You've completed all questions!")
                        if st.button("Start New Session"):
                            set_study_mode(None)

    except requests.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")

else:
    st.info("Upload your study material to begin!")

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

# Add this function to handle answer validation
def validate_answer(question_id: int, question: str, context: str, answer: str):
    try:
        response = requests.post(
            f"http://localhost:8000/validate-answer/{question_id}",
            json={
                "answer_text": answer,
                "question_text": question,
                "context": context
            }
        )
        if response.status_code == 200:
            return response.json()["validation"]
        return None
    except Exception as e:
        st.error(f"Error validating answer: {str(e)}")
        return None
