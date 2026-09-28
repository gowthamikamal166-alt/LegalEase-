"""Central configuration for LegalEase."""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Logo used in the web UI (dark theme) and in exported documents (white background)
WEB_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")
DOC_LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")

FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
