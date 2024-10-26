from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    course_code = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    questions = relationship("Question", back_populates="document")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    question_text = Column(Text)
    context = Column(Text)
    question_type = Column(String)
    difficulty = Column(String)
    document = relationship("Document", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    question = relationship("Question", back_populates="answers")
