import google.generativeai as genai
import inspect

print("GENAI VERSION:", genai.__version__)

print("\n=== embed_content SIGNATURE ===")
try:
    print(inspect.signature(genai.embed_content))
except Exception as e:
    print("Error reading signature:", e)

print("\n=== embed_content SOURCE ===")
try:
    print(inspect.getsource(genai.embed_content))
except Exception as e:
    print("Error reading source:", e)