from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.pdf_service import PDFProcessor
from ..services.ai_service import AIService
from typing import List, Dict
import io

router = APIRouter()
pdf_processor = PDFProcessor()
ai_service = AIService()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process PDF file"""
    try:
        # First extract and preprocess text
        content = pdf_processor.extract_text(file.file)
        processed_content = pdf_processor.preprocess_text(content)
        
        # Generate different questions for each mode
        print("Generating quick review questions...")
        quick_review = pdf_processor.generate_basic_questions(
            processed_content, 
            3, 
            question_type="quick"
        )
        
        print("Generating deep study questions...")
        deep_study = pdf_processor.generate_basic_questions(
            processed_content, 
            5,
            question_type="deep"
        )
        
        print("Generating revision questions...")
        revision = pdf_processor.generate_basic_questions(
            processed_content, 
            5,
            question_type="revision"
        )
        
        print("Generating test prep questions...")
        test_prep = pdf_processor.generate_basic_questions(
            processed_content, 
            5,
            question_type="test"
        )
        
        questions = {
            "QUICK_REVIEW": quick_review,
            "DEEP_STUDY": deep_study,
            "REVISION": revision,
            "TEST_PREP": test_prep
        }
        
        print("Questions generated successfully!")
        return {"questions": questions, "status": "success"}
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def validate_answer(request: dict):
    """Validate student answer"""
    try:
        result = ai_service.validate_answer(
            request["question"],
            request["context"],
            request["answer"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
