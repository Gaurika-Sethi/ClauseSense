from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# Prefer Streamlit secrets in deployment
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GEMINI_MODEL = st.secrets.get("GEMINI_MODEL", "gemini-2.0-flash")
else:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

print("[CONFIG] Gemini API Key Loaded:", GEMINI_API_KEY is not None)
print("[CONFIG] Using Model:", GEMINI_MODEL)
