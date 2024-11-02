from mistralai import Mistral
from typing import List, Dict
import re

class AIService:
    def __init__(self):
        # Initialize Mistral client
        api_key = "uoqh3XsN9jLVTrC9dtIs8NVsA3bAGOfZ"  # Consider moving this to environment variables
        self.client = Mistral(api_key=api_key)

    def generate_questions(self, content: str, num_questions: int = 5) -> List[Dict]:
        """Generate questions using Mistral AI"""
        system_prompt = """You are an experienced university professor creating exam questions. 
        Your task is to create high-quality exam questions based on the provided content.
        Each question should test different levels of understanding and include detailed feedback."""
        
        user_prompt = f"""Based on this content, create {num_questions} university-level exam questions:

Content:
{content[:2000]}  # Limit text length to avoid token limits

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
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            
            response_text = response.choices[0].message.content
            return self._parse_questions(response_text)[:num_questions]
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

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
            
            return self._parse_validation(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error validating answer: {e}")
            return {
                "score": 0,
                "feedback": "Error processing response",
                "strengths": [],
                "improvements": [],
                "tip": "Please try again"
            }

    def _parse_questions(self, response_text: str) -> List[dict]:
        """Parse AI response into structured question format"""
        questions = []
        try:
            blocks = response_text.split("\n\n")
            
            for block in blocks:
                if not block.strip():
                    continue
                    
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
            print(f"Error parsing questions: {e}")
            
        return questions

    def _parse_validation(self, response_text: str) -> Dict:
        """Parse AI validation response"""
        try:
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
            print(f"Error parsing validation: {e}")
            return {
                "score": 0,
                "feedback": "Error processing response",
                "strengths": [],
                "improvements": [],
                "tip": "Please try again"
            }
