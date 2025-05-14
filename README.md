# AI-Resume-Ranking
AI Resume Screening &amp; Candidate Ranking System An AI-powered resume screening tool that ranks candidates based on job descriptions. Uses TF-IDF Vectorization &amp; Cosine Similarity to compare resumes with job requirements. Built with Streamlit, Python, scikit-learn, and PyPDF2. 🚀

This project helps you **analyze and rank resumes** based on a given **job description** using AI. It compares extracted resume skills with job requirements, computes an ATS (Applicant Tracking System) score, and offers improvement suggestions.

---

## 🚀 Features

- Upload **PDF or DOCX** resumes
- Paste a **Job Description**
- Get a smart **ATS Score**
- See **Skill Matches & Gaps**
- Get **AI-based skill suggestions**
- Keeps resume structure intact


## 🛠 Tech Stack

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- Gemini API (Google)
- `python-docx`, `PyPDF2`, `dotenv`, `langchain`


## 📦 Installation

1. **Clone this repository:**

git clone https://github.com/rupeshgit-dev/AI-Resume-Ranking.git
cd AI-Resume-Ranking/resume_ranking

**2.(Optional) Create and activate a virtual environment:**
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

**3.Install required packages:**
pip install -r requirements.txt

**▶️ Run the App**
streamlit run resume_ranking.py

**📁 Folder Structure**
AI-Resume-Ranking/
│
├── resume_ranking/
│   ├── resume_ranking.py
│   ├── helper.py
│   ├── requirements.txt
│   └── .env  ← (add your Gemini key here)
├── README.md


📬 Contact
Built with ❤️ by Rupesh
Linkdin : https://www.linkedin.com/in/rupesh-miriyala/
Raise an issue or open a pull request to contribute.
