# config.py

from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env
load_dotenv()

# Read environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Indicate status
print("[CONFIG] Gemini API Key Loaded:", bool(GEMINI_API_KEY))
print("[CONFIG] Using Model:", GEMINI_MODEL)

# Configure Gemini SDK
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("[CONFIG] Gemini SDK configured successfully.")
    except Exception as e:
        print("[CONFIG ERROR] Failed to configure Gemini:", str(e))
else:
    print("[CONFIG WARNING] No API Key found! Running in STUB mode.")
