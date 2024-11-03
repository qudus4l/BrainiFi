from PyPDF2 import PdfReader
from typing import List, Dict
import re
import os
from .ai_service import AIService

class PDFProcessor:
    def __init__(self):
        self.ai_service = AIService()
        print("PDFProcessor initialized with AIService")
        self.max_workers = max(1, (os.cpu_count() or 2) - 1)

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

    def generate_basic_questions(self, text: str, num_questions: int = 5, question_type: str = "quick") -> List[Dict]:
        """Generate questions using AI service with specific type"""
        
        # Customize prompt based on question type
        type_prompts = {
            "quick": """Create quick review questions that test basic understanding. 
                       Focus on definitions and key concepts.""",
            "deep": """Create in-depth questions that require detailed understanding. 
                      Include analysis and application questions.""",
            "revision": """Create revision questions that help reinforce learning. 
                          Include a mix of recall and understanding questions.""",
            "test": """Create exam-style questions that simulate test conditions. 
                      Include higher-order thinking questions."""
        }
        
        prompt = type_prompts.get(question_type, type_prompts["quick"])
        
        return self.ai_service.generate_questions(text, num_questions, prompt)

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate answer using AI service"""
        return self.ai_service.validate_answer(question, context, student_answer)
