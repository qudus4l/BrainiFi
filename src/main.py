from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from .services.pdf_processor import PDFProcessor
from .database.db import get_db
from .database.models import Document, Question, Answer
from pydantic import BaseModel
import io

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

@app.get("/")
async def root():
    return {"message": "Welcome to BrainiFi API"}

@app.post("/upload-pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    course_code: str = None,
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        print(f"Processing file: {file.filename}")  # Debug log
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        
        # Process PDF with AI-powered question generation
        extracted_text = pdf_processor.extract_text(pdf_file)
        processed_text = pdf_processor.preprocess_text(extracted_text)
        questions = pdf_processor.generate_basic_questions(processed_text)
        
        print("Saving to database...")  # Debug log
        # Save to database
        document = Document(
            filename=file.filename,
            content=processed_text,
            course_code=course_code
        )
        db.add(document)
        await db.flush()
        
        # Save AI-generated questions
        for q in questions:
            question = Question(
                document_id=document.id,
                question_text=q["question"],
                context=q["context"],
                question_type=q["type"],
                difficulty=q.get("difficulty", "Medium")
            )
            db.add(question)
        
        await db.commit()
        print("Database commit successful")  # Debug log
        
        return {
            "filename": file.filename,
            "status": "processed",
            "text": processed_text[:500] + "...",
            "questions": questions
        }
    except Exception as e:
        print(f"Error processing file: {str(e)}")  # Debug log
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-answer/{question_id}")
async def validate_answer(
    question_id: int,
    validation_request: AnswerValidationRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Validate answer using AI service
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
