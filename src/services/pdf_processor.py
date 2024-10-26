from PyPDF2 import PdfReader
from typing import List

class PDFProcessor:
    def __init__(self):
        pass

    def extract_text(self, pdf_file) -> str:
        """Extract text from a PDF file"""
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing"""
        # Remove extra whitespace
        text = " ".join(text.split())
        return text

    def generate_basic_questions(self, text: str) -> List[dict]:
        """Generate basic questions from text using templates"""
        # This is a very basic implementation
        # Will be enhanced with proper NLP/AI later
        sentences = text.split('.')
        questions = []
        
        for sentence in sentences[:5]:  # Limit to first 5 sentences for MVP
            if len(sentence.strip()) > 20:  # Only process meaningful sentences
                questions.append({
                    "question": f"What can you tell me about: {sentence.strip()}?",
                    "context": sentence.strip()
                })
        
        return questions
