# BrainiFi 📚

An AI-powered study assistant that generates questions from your study materials.

## Features
- PDF document analysis
- Automatic question generation
- Multiple study modes:
  - Quick Review
  - Deep Study
  - Revision
  - Test Prep
- Real-time answer validation
- Progress tracking

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BrainiFi.git
cd BrainiFi
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

5. Run the app:
```bash
streamlit run src/streamlit_app.py
```

## Usage
1. Upload your study material (PDF)
2. Choose a study mode
3. Answer generated questions
4. Get instant feedback
5. Track your progress

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
[MIT](https://choosealicense.com/licenses/mit/)
