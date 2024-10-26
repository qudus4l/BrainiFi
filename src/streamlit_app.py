import streamlit as st
import requests
import io

st.title("BrainiFi - Academic Document Processor")

uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

if uploaded_file is not None:
    st.write("Processing your document...")
    
    # Send file to FastAPI backend
    files = {"file": ("document.pdf", uploaded_file, "application/pdf")}
    response = requests.post("http://localhost:8000/upload-pdf/", files=files)
    
    if response.status_code == 200:
        st.success("Document uploaded successfully!")
        st.json(response.json())
    else:
        st.error("Error uploading document")

st.markdown("""
### How to use BrainiFi:
1. Upload your PDF document
2. Wait for processing
3. Get insights and questions from your document
""")
