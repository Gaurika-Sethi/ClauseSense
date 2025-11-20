import sys, os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import config  # NOW this will FINALLY work
from gemini.gemini_client import is_configured, generate_completion, embed_text

print("=== Gemini Integration Test ===")

print("Gemini configured:", is_configured())

print("\n--- Test Completion ---")
print(generate_completion("Say 'Gemini is working!'", max_tokens=20))

print("\n--- Test Embeddings ---")
vecs = embed_text(["hello world", "confidential data"])
print("Embedding vector length:", len(vecs[0]))