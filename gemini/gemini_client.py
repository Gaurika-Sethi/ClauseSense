# gemini/gemini_client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load .env

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def is_configured() -> bool:
    return API_KEY is not None and API_KEY != ""

# Configure Gemini
if is_configured():
    genai.configure(api_key=API_KEY)


# ------------------------- Text Completion -------------------------
def generate_completion(prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
    """
    Generates text using Gemini model.
    Falls back to a deterministic stub if key is missing.
    """
    if not is_configured():
        return "[STUB] Gemini disabled — no API key available."

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        return response.text
    except Exception as e:
        return f"[ERROR] Gemini: {str(e)}"


# ------------------------- Embeddings -------------------------
# ------------------------- Local Embeddings -------------------------
from sentence_transformers import SentenceTransformer

_local_model = None

def embed_text(text_list):
    """
    Local embedding function using SentenceTransformer.
    Model: all-MiniLM-L6-v2 (384-dimensional vector).
    """

    global _local_model

    # Load model only once (caching)
    if _local_model is None:
        try:
            print("[EMBED] Loading local embedding model...")
            _local_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print("[EMBED ERROR] Could not load local model:", e)
            return [[0.0] * 384 for _ in text_list]

    try:
        return _local_model.encode(text_list).tolist()
    except Exception as e:
        print("[EMBED ERROR]", e)
        return [[0.0] * 384 for _ in text_list]

