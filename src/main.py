from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from .services.pdf_processor import PDFProcessor
from .database.db import get_db
from .database.models import Document, Question, Answer
from pydantic import BaseModel
import io
import os

class AnswerValidationRequest(BaseModel):
    answer_text: str
    question_text: str
    context: str

app = FastAPI(title="BrainiFi API", description="Academic Document Processing API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PDF processor
pdf_processor = PDFProcessor()

def check_model_availability():
    """Check if BitNet model is available"""
    model_path = "/Users/Q/Projects/BrainiFi/BitNet/models/bitnet_b1_58-large/ggml-model-i2_s.gguf"
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=503,
            detail=f"BitNet model not found at: {model_path}"
        )

@app.get("/")
async def root():
    return {"message": "Welcome to BrainiFi API"}

@app.post("/upload-pdf/")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    course_code: str = None,
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Check model availability first
        check_model_availability()
        
        print(f"Processing file: {file.filename}")  # Debug log
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        
        # Process PDF text first
        extracted_text = pdf_processor.extract_text(pdf_file)
        processed_text = pdf_processor.preprocess_text(extracted_text)
        
        # Save document to database first
        document = Document(
            filename=file.filename,
            content=processed_text,
            course_code=course_code
        )
        db.add(document)
        await db.flush()
        
        # Generate questions in background
        background_tasks.add_task(
            process_questions_background,
            document.id,
            processed_text,
            db
        )
        
        await db.commit()
        print("Initial database commit successful")  # Debug log
        
        return {
            "filename": file.filename,
            "status": "processing",
            "message": "Document uploaded. Questions are being generated in background.",
            "document_id": document.id
        }
    except Exception as e:
        print(f"Error processing file: {str(e)}")  # Debug log
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def process_questions_background(document_id: int, processed_text: str, db: AsyncSession):
    """Process questions in background"""
    try:
        # Generate questions with BitNet
        questions = pdf_processor.generate_basic_questions(processed_text)
        
        async with db.begin():
            # Save AI-generated questions
            for q in questions:
                question = Question(
                    document_id=document_id,
                    question_text=q["question"],
                    context=q["context"],
                    question_type=q["type"],
                    difficulty=q.get("difficulty", "Medium")
                )
                db.add(question)
            
            await db.commit()
            print(f"Questions saved for document {document_id}")
    except Exception as e:
        print(f"Error in background processing: {str(e)}")
        await db.rollback()

@app.post("/validate-answer/{question_id}")
async def validate_answer(
    question_id: int,
    validation_request: AnswerValidationRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Check model availability
        check_model_availability()
        
        # Add timeout handling for BitNet inference
        validation_result = pdf_processor.validate_answer(
            validation_request.question_text,
            validation_request.context,
            validation_request.answer_text
        )
        
        # Save answer to database
        answer = Answer(
            question_id=question_id,
            answer_text=validation_request.answer_text
        )
        db.add(answer)
        await db.commit()
        
        return {
            "validation": validation_result,
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/")
async def get_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document))
    documents = result.scalars().all()
    return documents

@app.get("/document/{document_id}")
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.get("/document/{document_id}/questions")
async def get_document_questions(document_id: int, db: AsyncSession = Depends(get_db)):
    """Get questions for a specific document"""
    result = await db.execute(
        select(Question).where(Question.document_id == document_id)
    )
    questions = result.scalars().all()
    if not questions:
        return {
            "status": "processing",
            "message": "Questions are still being generated"
        }
    return questions