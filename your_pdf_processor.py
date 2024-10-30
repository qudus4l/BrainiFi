def process_pdf_in_chunks(pdf_content, chunk_size=512):
    chunks = split_into_chunks(pdf_content, chunk_size)
    all_questions = []
    
    for chunk in chunks:
        questions = generate_ai_questions(chunk)
        if questions:
            all_questions.extend(questions)
    
    return all_questions 