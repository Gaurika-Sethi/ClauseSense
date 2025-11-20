# gemini/prompts/rewrite_prompts.py

def build_rewrite_prompt(original_text: str, rule_text: str, style: str = "strict") -> str:
    """
    Prompt to rewrite a violating section into a compliant one.
    style: "minimal" | "moderate" | "strict"
    """
    return (
        f"You are a professional compliance editor. Rewrite the following SECTION so it"
        f" fully complies with the RULE. Keep the tone similar to the original. "
        f"Provide only the rewritten SECTION (no commentary).\n\n"
        f"ORIGINAL SECTION:\n{original_text}\n\n"
        f"APPLICABLE RULE:\n{rule_text}\n\n"
        f"Rewrite style: {style} (minimal/moderate/strict)."
    )