from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict
import re

class AIService:
    def __init__(self):
        # Load TinyLlama model and tokenizer
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        print("Loading TinyLlama model and tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map="auto"
        )
        print("Model loaded successfully!")

    def generate_questions(self, text: str, num_questions: int = 5) -> List[Dict]:
        """Generate questions using TinyLlama"""
        prompt = f"""
        Generate {num_questions} study questions from this text. For each question:
        1. Make it thought-provoking
        2. Include the relevant context
        3. Specify the type (definition/analysis/application)
        4. Set an appropriate difficulty level

        Text: {text}

        Format each question as:
        Question: [the question]
        Context: [relevant context]
        Type: [question type]
        Difficulty: [Easy/Medium/Hard]
        """

        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=1024,
            temperature=0.7,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parse the response into structured questions
        questions = self._parse_questions(response)
        return questions

    def validate_answer(self, question: str, context: str, student_answer: str) -> Dict:
        """Validate student's answer using TinyLlama"""
        prompt = f"""
        Evaluate this student's answer:

        Question: {question}
        Context: {context}
        Student's Answer: {student_answer}

        Provide:
        1. Accuracy (0-100%)
        2. Feedback
        3. Key points missed (if any)
        4. Suggestions for improvement
        """

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=512,
            temperature=0.3,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parse the validation response
        return self._parse_validation(response)

    def _parse_questions(self, response: str) -> List[Dict]:
        """Parse the model's response into structured questions"""
        questions = []
        
        # Split response into individual questions
        raw_questions = re.split(r'\nQuestion:', response)
        
        for raw_q in raw_questions[1:]:  # Skip first empty split
            try:
                # Extract components using regex
                question = re.search(r'^(.*?)\nContext:', raw_q, re.DOTALL)
                context = re.search(r'Context:(.*?)\nType:', raw_q, re.DOTALL)
                q_type = re.search(r'Type:(.*?)\nDifficulty:', raw_q, re.DOTALL)
                difficulty = re.search(r'Difficulty:(.*?)(?:\n|$)', raw_q, re.DOTALL)
                
                if all([question, context, q_type, difficulty]):
                    questions.append({
                        "question": question.group(1).strip(),
                        "context": context.group(1).strip(),
                        "type": q_type.group(1).strip().lower(),
                        "difficulty": difficulty.group(1).strip()
                    })
            except Exception as e:
                print(f"Error parsing question: {e}")
                continue
                
        return questions

    def _parse_validation(self, response: str) -> Dict:
        """Parse the validation response into structured feedback"""
        try:
            accuracy = re.search(r'Accuracy:?\s*(\d+)%', response)
            feedback = re.search(r'Feedback:?(.*?)(?:Key points|$)', response, re.DOTALL)
            key_points = re.search(r'Key points.*?:(.*?)(?:Suggestions|$)', response, re.DOTALL)
            suggestions = re.search(r'Suggestions.*?:(.*?)$', response, re.DOTALL)
            
            return {
                "accuracy": int(accuracy.group(1)) if accuracy else 0,
                "feedback": feedback.group(1).strip() if feedback else "",
                "key_points_missed": key_points.group(1).strip() if key_points else "",
                "suggestions": suggestions.group(1).strip() if suggestions else ""
            }
        except Exception as e:
            print(f"Error parsing validation: {e}")
            return {
                "accuracy": 0,
                "feedback": "Error processing answer",
                "key_points_missed": "",
                "suggestions": ""
            }
