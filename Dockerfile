FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# blank 1 - spacy model download
RUN python -m spacy download en_core_web_sm

COPY . .

# blank 2 - run streamlit
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]