# 🧠 Smart Resume Analyser

An AI-powered resume analyser that compares your resume against a job description,
scores your skill match, and gives LLM-powered suggestions to improve your resume.

Built as a portfolio project for my QE → AI Engineer transition.

🔗 **Live Demo**: [your-streamlit-url-here]

---

## ✨ Features

- 📄 PDF resume upload and text extraction
- 🧹 Text cleaning and alias normalization (JS → javascript, k8s → kubernetes)
- 🧠 NLP-based skill extraction using spaCy PhraseMatcher
- 📊 Weighted skill scoring (frequency × position × category)
- 💡 LLM-powered improvement suggestions via HuggingFace
- 🎯 Prioritised missing skills (Critical / Important / Good to have)
- 📈 Evaluation metrics: Precision, Recall, F1 = 0.9808

---

## 🏗️ System Architecture
```
Resume PDF ──→ resume_parser.py ──→ aliases.py ──→ nlp_extractor.py
                                                          ↑
Job Description ──────────────────────────────────────────┘
                                                          ↓
                                                   skill_scorer.py
                                                   (freq × pos × cat)
                                                          ↓
                                                    llm_client.py
                                                          ↓
                                                       ui.py
                                                  (Streamlit frontend)

evaluator.py → developer tool (precision, recall, F1) — not shown in UI
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| NLP | spaCy, PhraseMatcher |
| UI | Streamlit |
| LLM | HuggingFace Inference API |
| PDF Parsing | pdfplumber |
| Data | skills.csv (95+ skills with categories) |
| Containerization | Docker |
| Deployment | Streamlit Cloud |

---

## 📂 Project Structure
```
smart-resume-analyser/
│
├── ui.py                 # Streamlit frontend
├── resume_parser.py      # PDF extraction + text cleaning
├── nlp_extractor.py      # spaCy PhraseMatcher skill extraction
├── aliases.py            # Alias normalization (js → javascript)
├── skill_scorer.py       # Weighted scoring system
├── llm_client.py         # HuggingFace LLM suggestions
├── evaluator.py          # Precision, Recall, F1 evaluation
├── Dockerfile            # Container setup
├── requirements.txt      # Dependencies
└── Data/
    └── skills.csv        # 95+ skills with categories
```

---

## 🚀 How to Run

### Option 1 — Local
```bash
git clone https://github.com/kruba152001/smart-resume-analyzer
cd smart-resume-analyzer
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run ui.py
```

### Option 2 — Docker
```bash
docker build -t smart-resume-analyser .
docker run -p 8501:8501 --env-file .env smart-resume-analyser
```

Then open: `http://localhost:8501`

---

## 🔑 Environment Variables

Create a `.env` file:
```
HF_TOKEN=your_huggingface_token_here
```

---

## 📊 Evaluation Results

Run `python evaluator.py` to measure extractor quality:
```
Average Precision : 1.0
Average Recall    : 0.9643
Average F1 Score  : 0.9808
```

---

## 🛣️ What I Learned

- NLP pipeline design with spaCy PhraseMatcher
- Multi-signal scoring systems (frequency × position × category)
- Evaluation metrics: precision, recall, F1
- Docker containerization
- Streamlit Cloud deployment
- Clean architecture: separating data from config

---

## 🎯 Why This Project?

Built to demonstrate real AI Engineering skills:
- End-to-end NLP pipeline
- Data-driven design (skills.csv as single source of truth)
- Measurable quality (F1 = 0.9808)
- Production-ready (Dockerized + deployed)

---

👨‍💻 Built by Kruba — QE → AI Engineer transition project
```
