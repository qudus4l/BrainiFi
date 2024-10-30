import google.generativeai as genai
from typing import List, Dict
import re
import os
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        # Load API key from environment variable
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
            
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model (free version)
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',  # Free model
            generation_config=generation_config
        )

    def generate_questions(self, text: str, num_questions: int = 5) -> List[Dict]:
        """Generate questions using Gemini"""
        prompt = f"""You are an educational assistant. Create {num_questions} study questions from the following text.

Text to analyze:
{text}

For each question, use exactly this format:
Question: (write your question here)
Context: (include relevant part from the text)
Type: (choose one: definition/analysis/application)
Difficulty: (choose one: Easy/Medium/Hard)

Remember:
1. Each question must follow the exact format above
2. Make questions clear and focused
3. Include specific context from the text
4. Choose an appropriate difficulty level
"""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_questions(response.text)
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate student's answer using Gemini"""
        prompt = f"""Evaluate this student's answer:

Question: {question}
Context: {context}
Student's Answer: {student_answer}

Provide a clear evaluation in this format:
1. Score (0-100): [score]
2. Brief Feedback: [2-3 sentences explaining why]
3. Strengths: [what they got right]
4. Areas to Improve: [what they missed]
5. Quick Tip: [one specific improvement suggestion]
"""

        try:
            response = self.model.generate_content(prompt)
            return self._parse_validation(response.text)
        except Exception as e:
            print(f"Error validating answer: {e}")
            return {
                "score": 0,
                "feedback": "Error processing answer",
                "strengths": [],
                "improvements": [],
                "tip": "Please try again"
            }

    def _parse_questions(self, response: str) -> List[Dict]:
        """Parse the model's response into structured questions"""
        questions = []
        
        if not response:
            print("Empty response from model")
            return questions
        
        print(f"Parsing response: {response[:200]}...")  # Debug log
        
        # Split response into individual questions
        raw_questions = re.split(r'(?:\n|^)Question:', response)
        
        for raw_q in raw_questions[1:]:  # Skip first empty split
            try:
                print(f"Processing question chunk: {raw_q[:200]}...")  # Debug log
                
                # More flexible regex patterns
                question = re.search(r'^(.*?)(?:\nContext:|\n\n|$)', raw_q, re.DOTALL)
                context = re.search(r'Context:\s*(.*?)(?:\nType:|\n\n|$)', raw_q, re.DOTALL)
                q_type = re.search(r'Type:\s*(.*?)(?:\nDifficulty:|\n\n|$)', raw_q, re.DOTALL)
                difficulty = re.search(r'Difficulty:\s*(.*?)(?:\n\n|$)', raw_q, re.DOTALL)
                
                if question:  # As long as we have a question, try to parse
                    questions.append({
                        "question": question.group(1).strip(),
                        "context": context.group(1).strip() if context else "No context provided",
                        "type": q_type.group(1).strip().lower() if q_type else "definition",
                        "difficulty": difficulty.group(1).strip() if difficulty else "Medium"
                    })
                    print(f"Successfully parsed question: {questions[-1]}")  # Debug log
                else:
                    print(f"Failed to parse question from: {raw_q[:200]}...")
                    
            except Exception as e:
                print(f"Error parsing question: {e}")
                print(f"Raw question text: {raw_q[:200]}...")
                continue
        
        return questions

    def _parse_validation(self, response: str) -> Dict:
        """Parse the validation response with improved structure"""
        try:
            score = re.search(r'Score:\s*(\d+)', response)
            main_feedback = re.search(r'Main Feedback:(.*?)(?:Key Points|$)', response, re.DOTALL)
            key_points = re.findall(r'Key Points Covered:(.+?)Missing Elements:', response, re.DOTALL)
            missing = re.findall(r'Missing Elements:(.+?)Improvement Suggestions:', response, re.DOTALL)
            suggestions = re.findall(r'Improvement Suggestions:(.+?)Sample Improved Answer:', response, re.DOTALL)
            sample = re.search(r'Sample Improved Answer:(.+?)$', response, re.DOTALL)

            # Process bullet points into lists
            def extract_bullets(text):
                if not text:
                    return []
                return [point.strip('• ').strip() for point in text[0].split('\n') if point.strip('• ').strip()]

            return {
                "score": int(score.group(1)) if score else 0,
                "main_feedback": main_feedback.group(1).strip() if main_feedback else "",
                "key_points_covered": extract_bullets(key_points),
                "missing_elements": extract_bullets(missing),
                "improvement_suggestions": extract_bullets(suggestions),
                "sample_answer": sample.group(1).strip() if sample else ""
            }
        except Exception as e:
            print(f"Error parsing validation: {e}")
            return {
                "score": 0,
                "main_feedback": "Error processing answer",
                "key_points_covered": [],
                "missing_elements": [],
                "improvement_suggestions": [],
                "sample_answer": ""
            }
