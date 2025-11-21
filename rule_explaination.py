# rule_explanations.py
import google.generativeai as genai
import numpy as np
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use consistent model
GEMINI_MODEL = "gemini-2.0-flash"
EMBED_MODEL = "text-embedding-004"

model = genai.GenerativeModel(GEMINI_MODEL)


def embed_text(text: str):
    """
    Embeds text using Gemini embeddings.
    Returns a numpy vector.
    """
    try:
        resp = genai.embed_content(
            model=EMBED_MODEL,
            content=text,
        )
        vec = resp["embedding"]
        return np.array(vec, dtype=float)
    except Exception as e:
        print(f"[Embedding Error] {e}")
        return np.zeros(768)  # safe fallback


def cosine_similarity(a, b):
    """Safe cosine similarity (0–1)."""
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float((sim + 1) / 2)  # scale -1..1 → 0..1


def ask_gemini(prompt: str) -> str:
    """
    Safe wrapper around Gemini generate_content().
    Returns plain text.
    """
    try:
        resp = model.generate_content(prompt)
        return resp.text if hasattr(resp, "text") else str(resp)
    except Exception as e:
        return f"[Gemini Error: {e}]"


def generate_rule_explanations(sections, relevant_rules):
    """
    For every (section, rule) pair:
    - Generate explanation using Gemini.
    - Compute confidence using embedding similarity.

    Returns:
    {
       "R1": [
          {"section": "...", "explanation": "...", "confidence": 0.83},
          ...
       ]
    }
    """

    explanations = {}

    for rule in relevant_rules:
        rule_id = rule["rule_id"]
        rule_text = rule["text"]

        # Pre-embed rule text (performance optimization)
        rule_vec = embed_text(rule_text)

        explanations[rule_id] = []

        for section in sections:
            # --- Confidence Score via cosine similarity ---
            section_vec = embed_text(section)
            conf = cosine_similarity(rule_vec, section_vec)

            # --- Explanation via Gemini ---
            prompt = f"""
You are an AI compliance assistant.

A document section triggered a policy rule.

Explain clearly:
1. Why this section violates the rule.
2. What exact text in the section triggered the violation.
3. A short reasoning summary.

Return a natural language explanation.

--- RULE ---
{rule_text}

--- DOCUMENT SECTION ---
{section}
"""

            explanation_text = ask_gemini(prompt)

            explanations[rule_id].append({
                "section": section,
                "explanation": explanation_text,
                "confidence": round(conf, 3)
            })

    return explanations
