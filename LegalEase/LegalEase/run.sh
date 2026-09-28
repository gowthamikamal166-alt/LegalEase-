#!/usr/bin/env bash
# Starts backend (FastAPI) and frontend (Streamlit)
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACK_PID=$!
trap "kill $BACK_PID" EXIT
streamlit run frontend/app.py
