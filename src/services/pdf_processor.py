from PyPDF2 import PdfReader
from typing import List, Dict
from mistralai import Mistral
import re
import os

class PDFProcessor:
    def __init__(self):
        # Initialize Mistral client
        api_key = "uoqh3XsN9jLVTrC9dtIs8NVsA3bAGOfZ"  # Consider moving this to environment variables
        self.client = Mistral(api_key=api_key)
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

    def generate_basic_questions(self, text: str, num_questions: int = 5) -> List[dict]:
        """Generate questions using Mistral AI"""
        system_prompt = """You are an experienced university professor creating exam questions. 
        Your task is to create high-quality exam questions based on the provided content.
        Each question should test different levels of understanding and include detailed feedback."""
        
        user_prompt = f"""Based on this content, create {num_questions} university-level exam questions:

Content:
{text[:2000]}  # Limit text length to avoid token limits

For each question, provide:
1. The question text (clear and academically rigorous)
2. Question type (knowledge/application/analysis/evaluation)
3. What the question tests (specific learning outcomes)
4. A model answer outline (key points that should be included)
5. Common mistakes students might make

Format each question as a JSON-like structure:
{{
    "question": "(question text)",
    "type": "(question type)",
    "context": "(what the question tests)",
    "difficulty": "(easy/medium/hard)"
}}"""

        try:
            # Call Mistral API
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            
            # Parse response into structured format
            response_text = response.choices[0].message.content
            questions = self._parse_mistral_response(response_text)
            return questions[:num_questions]  # Ensure we return requested number of questions
            
        except Exception as e:
            print(f"Error generating questions with Mistral: {e}")
            return []

    def _parse_mistral_response(self, response_text: str) -> List[dict]:
        """Parse Mistral's response into structured question format"""
        questions = []
        try:
            # Split response into question blocks
            blocks = response_text.split("\n\n")
            
            for block in blocks:
                if not block.strip():
                    continue
                    
                # Extract question components using regex
                question_match = re.search(r'"question":\s*"([^"]+)"', block)
                type_match = re.search(r'"type":\s*"([^"]+)"', block)
                context_match = re.search(r'"context":\s*"([^"]+)"', block)
                difficulty_match = re.search(r'"difficulty":\s*"([^"]+)"', block)
                
                if question_match:
                    question = {
                        "question": question_match.group(1).strip(),
                        "type": type_match.group(1).strip() if type_match else "knowledge",
                        "context": context_match.group(1).strip() if context_match else "",
                        "difficulty": difficulty_match.group(1).strip() if difficulty_match else "medium"
                    }
                    questions.append(question)
                    
        except Exception as e:
            print(f"Error parsing Mistral response: {e}")
            
        return questions

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate student's answer using Mistral AI"""
        prompt = f"""Evaluate this student answer:

Question: {question}
Context: {context}
Student Answer: {student_answer}

Provide evaluation in this format:
{{
    "score": (0-100),
    "feedback": "(brief feedback)",
    "strengths": ["point1", "point2"],
    "improvements": ["point1", "point2"],
    "tip": "(one specific improvement tip)"
}}"""

        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": "You are an experienced professor evaluating student answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response into structured format
            response_text = response.choices[0].message.content
            return self._parse_validation_response(response_text)
            
        except Exception as e:
            print(f"Error validating answer with Mistral: {e}")
            return {
                "score": 0,
                "feedback": "Error processing response",
                "strengths": [],
                "improvements": [],
                "tip": "Please try again"
            }

    def _parse_validation_response(self, response_text: str) -> Dict:
        """Parse Mistral's validation response"""
        try:
            # Extract components using regex
            score_match = re.search(r'"score":\s*(\d+)', response_text)
            feedback_match = re.search(r'"feedback":\s*"([^"]+)"', response_text)
            strengths_match = re.search(r'"strengths":\s*\[(.*?)\]', response_text, re.DOTALL)
            improvements_match = re.search(r'"improvements":\s*\[(.*?)\]', response_text, re.DOTALL)
            tip_match = re.search(r'"tip":\s*"([^"]+)"', response_text)
            
            return {
                "score": int(score_match.group(1)) if score_match else 0,
                "feedback": feedback_match.group(1) if feedback_match else "No feedback available",
                "strengths": [s.strip().strip('"') for s in strengths_match.group(1).split(",")] if strengths_match else [],
                "improvements": [i.strip().strip('"') for i in improvements_match.group(1).split(",")] if improvements_match else [],
                "tip": tip_match.group(1) if tip_match else "No specific tip available"
            }
            
        except Exception as e:
            print(f"Error parsing validation response: {e}")
            return {
                "score": 0,
                "feedback": "Error processing response",
                "strengths": [],
                "improvements": [],
                "tip": "Please try again"
            }
