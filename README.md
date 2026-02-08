🧠 Smart Resume Analyzer
A Python-based Smart Resume Analyzer that compares a resume against job-required skills, calculates a match percentage, highlights missing skills, and gives a simple decision message on candidate fit.

This project is built step by step to demonstrate:

Text extraction from PDFs

Text preprocessing (cleaning)

Skill matching using Python sets

Basic scoring logic

Simple decision-making logic

(Upcoming) NLP improvements and UI

✨ Features
📄 Extracts text from resume PDF

🧹 Cleans and normalizes text for analysis

🧠 Matches resume skills against job skills

📊 Calculates Match Percentage

❌ Shows Missing Skills

✅ Gives a Decision Message:

Good fit

Partial match

Low match

🛠 Tech Stack
Python 3

pdfplumber (for PDF text extraction)

re (for text cleaning)

(Planned) spaCy for NLP

(Planned) Streamlit for UI

📂 Project Structure
smart-resume-analyzer/
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── requirements.txt
├── sample_resumes/
│ └── sample_resume.pdf
└── README.md
🚀 How It Works
Reads a resume PDF

Extracts raw text

Cleans the text (lowercase, remove symbols, fix spaces)

Matches skills against a predefined job skill set

Calculates match percentage

Finds missing skills

Prints a decision message based on the score

▶️ How to Run

1. Clone the repository
   git clone <your-repo-url>
   cd smart-resume-analyzer
2. Create and activate virtual environment
   python -m venv venv
   venv\Scripts\activate # Windows

# or

source venv/bin/activate # Mac/Linux 3. Install dependencies
pip install -r requirements.txt 4. Add your resume
Put your resume PDF inside:

sample_resumes/
And update the path in app.py if needed:

resume_path = "sample_resumes/sample_resume.pdf" 5. Run the app
python app.py
📊 Example Output
Matched Skills: {'python', 'java', 'sql', 'aws', 'docker', 'html', 'css', 'javascript'}
Matched Skills Percentage: 90.00%
Missing Skills: {'kubernetes'}
Decision: The candidate is a good fit for the job.
🛣 Roadmap (Planned Improvements)
Improve skill extraction using spaCy (NLP)

Support job description input instead of hardcoded skills

Add Streamlit UI for file upload and results display

Better formatting and reports

Export results to PDF/CSV

🎯 Why This Project?
This project is built to:

Learn AI/NLP fundamentals

Understand real-world text preprocessing

Build an end-to-end analysis pipeline

Create a portfolio-ready, explainable project

🙌 Author
Built by Kruba
Learning AI, Python, and building real-world projects step by step.
