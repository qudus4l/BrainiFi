import google.generativeai as genai
from typing import List, Dict
import re
import time

class AIService:
    def __init__(self):
        # Initialize Google AI
        api_key = "AIzaSyAGniIqi7LTNz3EeqGWN9MhuzxTVlzjXCM"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_questions(self, content: str, num_questions: int = 5, mode: str = "quick") -> List[Dict]:
        """Generate questions using Google AI with mode-specific prompts"""
        print(f"\nStarting question generation for mode: {mode}")
        print(f"Requested {num_questions} questions")
        
        mode_prompts = {
            "quick": """Create {num_questions} quick review questions that test basic understanding. 
                       Focus on definitions and key concepts.""",
            "deep": """Create {num_questions} in-depth questions that require detailed understanding. 
                      Include analysis and application questions.""",
            "revision": """Create {num_questions} revision questions that help reinforce learning. 
                          Mix recall with understanding questions.""",
            "test": """Create {num_questions} exam-style questions that simulate test conditions. 
                      Include higher-order thinking questions."""
        }

        try:
            print("Preparing prompts...")
            system_prompt = """You are an experienced university professor creating exam questions. 
            Your task is to create high-quality questions based on the provided content.
            Format each question as a JSON object with the following structure:
            {
                "question": "the question text",
                "type": "knowledge/application/analysis",
                "context": "what this question tests",
                "difficulty": "easy/medium/hard",
                "hint": "a helpful hint",
                "key_points": ["point1", "point2"]
            }
            Separate each question object with a newline."""
            
            user_prompt = f"""Based on this content, create {num_questions} questions following this specific format:
            {mode_prompts.get(mode, mode_prompts["quick"])}

            Content:
            {content[:2000]}

            Remember to format each question as a proper JSON object."""
            
            print("Sending request to Gemini...")
            response = self.model.generate_content([
                system_prompt,
                user_prompt
            ])
            
            print("Received response from Gemini")
            print("Response text:", response.text[:200] + "...")  # Print first 200 chars
            
            parsed_questions = self._parse_questions(response.text)
            print(f"Parsed {len(parsed_questions)} questions")
            
            final_questions = parsed_questions[:num_questions]
            print(f"Returning {len(final_questions)} questions")
            
            return final_questions
                
        except Exception as e:
            print(f"Error in generate_questions: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return []

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate student's answer using Google AI"""
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
            response = self.model.generate_content(prompt)
            return self._parse_validation(response.text)
            
        except Exception as e:
            print(f"Error validating answer with Google AI: {e}")
            return {
                "score": 0,
                "feedback": "Error processing response. Please try again later.",
                "strengths": [],
                "improvements": [],
                "tip": "Service temporarily unavailable"
            }

    def _parse_questions(self, response_text: str) -> List[dict]:
        """Parse AI response into structured question format"""
        print("\nStarting question parsing")
        print("Response text length:", len(response_text))
        questions = []
        try:
            blocks = response_text.split("\n\n")
            print(f"Found {len(blocks)} blocks")
            
            for i, block in enumerate(blocks):
                print(f"\nProcessing block {i+1}")
                if not block.strip():
                    print("Empty block, skipping")
                    continue
                    
                print("Block content preview:", block[:100] + "...")
                
                question_match = re.search(r'"question":\s*"([^"]+)"', block)
                if question_match:
                    print("Found question match")
                    type_match = re.search(r'"type":\s*"([^"]+)"', block)
                    context_match = re.search(r'"context":\s*"([^"]+)"', block)
                    difficulty_match = re.search(r'"difficulty":\s*"([^"]+)"', block)
                    hint_match = re.search(r'"hint":\s*"([^"]+)"', block)
                    key_points_match = re.search(r'"key_points":\s*\[(.*?)\]', block, re.DOTALL)
                    
                    question = {
                        "question": question_match.group(1).strip(),
                        "type": type_match.group(1).strip() if type_match else "knowledge",
                        "context": context_match.group(1).strip() if context_match else "",
                        "difficulty": difficulty_match.group(1).strip() if difficulty_match else "medium",
                        "hint": hint_match.group(1).strip() if hint_match else "Think about the main concepts discussed.",
                        "key_points": [p.strip().strip('"') for p in key_points_match.group(1).split(",")] if key_points_match else []
                    }
                    print("Created question:", question["question"][:50] + "...")
                    questions.append(question)
                else:
                    print("No question match found in block")
                    
        except Exception as e:
            print(f"Error parsing questions: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
        print(f"Finished parsing. Found {len(questions)} questions")
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
