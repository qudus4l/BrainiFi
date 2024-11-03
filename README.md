# BrainiFi 📚

BrainiFi is an AI-powered study assistant that transforms your study materials into interactive learning experiences. Built with React, TypeScript, and Python, BrainiFi leverages advanced AI to generate intelligent questions from your PDF documents, helping you study smarter and more efficiently.

## ✨ Features

### Core Features

- **📄 PDF Document Analysis**: Seamlessly upload and process PDF study materials.
- **🤖 AI-Powered Question Generation**: Automatically generate a variety of questions to test your understanding.
- **📊 Real-time Answer Validation**: Get immediate feedback on your answers to reinforce learning.
- **📈 Progress Tracking**: Monitor your study progress and performance over time.

### Study Modes

- **🎯 Quick Review**: Test your basic understanding with straightforward questions.
- **📝 Deep Study**: Engage with comprehensive questions that require detailed understanding.
- **🔄 Revision**: Reinforce your knowledge with a mix of recall and understanding questions.
- **📊 Test Prep**: Prepare for exams with exam-style questions that simulate test conditions.

### Smart Features

- **Adaptive Question Generation**: Questions adjust based on your performance and learning style.
- **Personalized Feedback**: Receive tailored feedback to enhance your study sessions.
- **Multiple Difficulty Levels**: Choose questions that match your current knowledge level.
- **Progress Analytics**: Gain insights into your learning journey with detailed analytics.
- **Keyboard Shortcuts**: Navigate and interact with the application efficiently using keyboard shortcuts.

## 🛠 Tech Stack

### Frontend

- **React 18**
- **TypeScript**
- **Vite**
- **Tailwind CSS**
- **Framer Motion**
- **React Icons**

### Backend

- **FastAPI**
- **Python 3.8+**
- **Google Generative AI**
- **PyPDF2**
- **Uvicorn**

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Node.js**: Version 16 or higher [Download Node.js](https://nodejs.org/)
- **Python**: Version 3.8 or higher [Download Python](https://www.python.org/downloads/)
- **Google API Key for Gemini**: Obtain an API key from Google Cloud Platform.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/brainifi.git
   cd brainifi
   ```

2. **Setup Backend**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the `backend` directory and add your Google API Key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Start Backend Server**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Setup Frontend**
   Open a new terminal window:

   ```bash
   cd frontend
   npm install
   ```

6. **Start Frontend Development Server**

   ```bash
   npm run dev
   ```

7. **Access the Application**
   Navigate to `http://localhost:3000` in your web browser to start using BrainiFi.

## 📄 Usage

1. **Upload PDF**
   - Click on the "Upload PDF" button to upload your study materials.

2. **Select Study Mode**
   - Choose from Quick Review, Deep Study, Revision, or Test Prep to generate relevant questions.

3. **Answer Questions**
   - Provide your answers and receive real-time feedback to enhance your learning.

4. **Track Progress**
   - Monitor your study progress through the analytics dashboard.

## 🧰 Available Scripts

In the project directory, you can run:

### Frontend

- **`npm run dev`**: Starts the development server.
- **`npm run build`**: Builds the app for production.
- **`npm run lint`**: Runs ESLint to analyze code for potential errors.
- **`npm run preview`**: Previews the production build.

### Backend

- **`uvicorn app.main:app --reload`**: Starts the FastAPI server with hot-reloading.

## 🛡️ Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch**

   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit your Changes**

   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open a Pull Request**

## 📜 License

Distributed under the [MIT License](LICENSE). See `LICENSE` for more information.

## 📫 Contact

- **Project Link**: [https://github.com/your-username/brainifi](https://github.com/your-username/brainifi)
- **Made with ❤️ for Nigerian Students 🇳🇬**

## Acknowledgements

- [React](https://reactjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://cloud.google.com/products/ai)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)
- And many more!
