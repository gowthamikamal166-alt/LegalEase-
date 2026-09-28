# LegalEase - AI Legal Document Generator

## Setup
```
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env       # then add your GEMINI_API_KEY
```
Put your logos in `Image/Logo.png` (white background docs) and `Image/inverseLogo.png` (dark web UI).

## Run
```
uvicorn legalEaseAPI.main:app --reload      # terminal 1 (backend, :8000)
streamlit run frontend/app.py               # terminal 2 (frontend, :8501)
```
