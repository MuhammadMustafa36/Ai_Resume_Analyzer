# 📄 AI Resume Analyzer

An AI-powered resume analysis application built using Python,
Streamlit, and Ollama.

The application allows users to upload their resume and compare
their skills with a job description.

---

## 🚀 Features

- Upload PDF resumes
- Upload DOCX resumes
- Upload TXT resumes
- Extract resume text
- Extract technical skills
- Extract skills from job descriptions
- Compare resume skills with job requirements
- Identify matched skills
- Identify missing skills
- Identify additional resume skills
- Calculate skill match percentage
- Generate AI-powered improvement suggestions
- Local LLM support using Ollama
- No OpenAI API key required

---

## 🛠️ Technologies

- Python
- Streamlit
- PyPDF
- python-docx
- Requests
- Ollama
- Regular Expressions

---

## 📁 Project Structure

```text
AI_Resume_Analyzer/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── parser.py
│   ├── skills.py
│   └── ai.py
│
├── requirements.txt
├── README.md
└── .gitignore