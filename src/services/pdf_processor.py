from PyPDF2 import PdfReader
from typing import List, Dict
from .ai_service import AIService
import re
import string

class PDFProcessor:
    def __init__(self):
        self.ai_service = AIService()
        print("PDF Processor initialized with AI Service")
        # Question templates for different types of content
        self.question_templates = {
            'definition': [
                "What is {concept}?",
                "Define {concept} in your own words:",
                "Explain the term {concept}:",
            ],
            'process': [
                "Describe the process of {concept}:",
                "What are the steps involved in {concept}?",
                "How does {concept} work?",
            ],
            'comparison': [
                "Compare and contrast {concept1} and {concept2}:",
                "What are the key differences between {concept1} and {concept2}?",
            ],
            'example': [
                "Can you provide an example of {concept}?",
                "How would you apply {concept} in a real-world situation?",
            ],
            'importance': [
                "Why is {concept} important?",
                "What is the significance of {concept}?",
            ]
        }

    def extract_text(self, pdf_file) -> str:
        """Extract text from a PDF file"""
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def preprocess_text(self, text: str) -> str:
        """Enhanced text preprocessing for academic content"""
        
        # Preserve mathematical expressions
        text = re.sub(r'(\$.*?\$)', lambda m: m.group(1).replace(' ', '_SPACE_'), text)
        
        # Preserve course codes and numbers with better pattern matching
        text = re.sub(r'([A-Z]{2,4})\s*[-/]?\s*(\d{3}[A-Z]?)', r'\1 \2', text)
        
        # Handle bullet points and numbered lists
        text = re.sub(r'^\s*[\u2022\u2023\u25E6\u2043\u2219]\s*', '• ', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*(\d+\.|\w+\.)\s+', r'\1 ', text, flags=re.MULTILINE)
        
        # Handle section headers
        text = re.sub(r'^([A-Z][A-Za-z\s]{,50}):\s*$', r'\n\1:\n', text, flags=re.MULTILINE)
        
        # Handle citations
        text = re.sub(r'\(([A-Za-z\s]+,\s*\d{4})\)', r'[REF:\1]', text)
        
        # Fix common academic abbreviations
        academic_fixes = {
            'i.e.': 'that is',
            'e.g.': 'for example',
            'et al': 'and others',
            'etc.': 'and so on',
            'fig.': 'figure',
            'eq.': 'equation'
        }
        for abbr, full in academic_fixes.items():
            text = re.sub(rf'\b{abbr}\b', full, text, flags=re.IGNORECASE)
        
        # Handle multi-line paragraphs
        text = re.sub(r'\n(?!\n)', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)
        
        # Fix spacing issues
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s*([.,;:])\s*', r'\1 ', text)
        
        # Restore mathematical expressions
        text = text.replace('_SPACE_', ' ')
        
        # Split into sentences and process each
        sentences = []
        for sentence in re.split(r'(?<=[.!?])\s+', text):
            sentence = sentence.strip()
            if len(sentence) > 30:  # Only process meaningful sentences
                if not re.match(r'^[A-Z]{2,4}\s*\d{3}', sentence):  # Not a course code
                    sentence = sentence[0].upper() + sentence[1:]
                sentences.append(sentence)
        
        return ' '.join(sentences)

    def identify_question_type(self, sentence: str) -> str:
        """Identify the type of question to generate based on content"""
        # Look for definition patterns
        if re.search(r'is\s+a|are\s+a|refers\s+to|defined\s+as', sentence.lower()):
            return 'definition'
        
        # Look for process patterns
        if re.search(r'steps|process|procedure|method|how\s+to', sentence.lower()):
            return 'process'
        
        # Look for comparison patterns
        if re.search(r'compared|versus|different|similar to|while', sentence.lower()):
            return 'comparison'
        
        # Look for example patterns
        if re.search(r'example|instance|such as|like|case', sentence.lower()):
            return 'example'
        
        # Look for importance patterns
        if re.search(r'important|significant|crucial|key|essential', sentence.lower()):
            return 'importance'
        
        return 'definition'  # default type

    def extract_key_concepts(self, sentence: str) -> Dict[str, str]:
        """Extract key concepts from the sentence"""
        concepts = {}
        
        # Extract main concept (usually before "is a" or similar patterns)
        if match := re.search(r'^(.*?)\s+(?:is|are|refers)', sentence.lower()):
            concepts['concept'] = match.group(1).strip()
        
        # Extract comparison concepts
        if 'compared' in sentence.lower() or 'versus' in sentence.lower():
            parts = re.split(r'\s+(?:compared|versus|and)\s+', sentence.lower())
            if len(parts) >= 2:
                concepts['concept1'] = parts[0].strip()
                concepts['concept2'] = parts[1].strip()
        
        # If no specific concept found, use the main subject
        if not concepts:
            concepts['concept'] = re.sub(r'^\W+|\W+$', '', sentence.split(',')[0])
        
        return concepts

    def generate_basic_questions(self, text: str) -> List[dict]:
        """Generate questions using AI service"""
        try:
            # Use AI service for question generation
            questions = self.ai_service.generate_questions(text)
            return questions
        except Exception as e:
            print(f"AI question generation failed: {e}")
            # Fallback to template-based questions if AI fails
            return self._generate_template_questions(text)

    def assess_difficulty(self, text: str) -> str:
        """Assess the difficulty of a question based on content complexity"""
        # Count complex terms and structures
        complex_patterns = [
            r'\b(?:analyze|evaluate|synthesize|critique)\b',
            r'\b(?:relationship|correlation|causation)\b',
            r'\b(?:therefore|however|consequently)\b',
            r'\([^)]*\)',  # Text in parentheses
            r'\b(?:theory|principle|law)\b'
        ]
        
        complexity_score = sum(len(re.findall(pattern, text, re.I)) 
                              for pattern in complex_patterns)
        
        # Assess sentence structure complexity
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        if complexity_score > 3 or avg_word_length > 7:
            return "Hard"
        elif complexity_score > 1 or avg_word_length > 6:
            return "Medium"
        else:
            return "Easy"

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate answer using AI service"""
        try:
            return self.ai_service.validate_answer(question, context, student_answer)
        except Exception as e:
            print(f"AI answer validation failed: {e}")
            return {
                "accuracy": 0,
                "feedback": "Unable to validate answer at this time",
                "key_points_missed": "",
                "suggestions": "Please try again later"
            }

    def _generate_template_questions(self, text: str) -> List[dict]:
        """Fallback method using templates (keep existing template logic)"""
        # ... (keep existing template-based question generation as fallback) ...
