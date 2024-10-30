try:
    questions = generate_ai_questions(pdf_content)
    if questions is None:
        raise ValueError("Question generation failed")
    
    # Save to database
    save_to_database(questions)
except Exception as e:
    logger.error(f"Error processing file: {str(e)}")
    # Handle the error appropriately, perhaps return an error response 