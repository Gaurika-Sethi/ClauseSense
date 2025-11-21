import json

def parse_json_safe(raw_output: str):
    """
    Takes Gemini string output and safely extracts JSON.
    If model adds extra text, tries to isolate JSON portion.
    """
    if not raw_output:
        return {}

    raw_output = raw_output.strip()

    # Pure JSON case
    try:
        return json.loads(raw_output)
    except Exception:
        pass

    # Try extracting JSON substring
    start = raw_output.find("{")
    end = raw_output.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw_output[start:end + 1])
        except Exception:
            pass

    # Last fallback
    return {}
