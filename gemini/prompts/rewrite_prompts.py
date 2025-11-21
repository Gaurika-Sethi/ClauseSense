# rewrite_prompts.py

"""
Prompt builder for RewriteAgent.
This function prepares the formatted prompt that will be sent to the Gemini model.
"""

def build_rewrite_prompt(original_text: str, rewriting_style: str = "professional and concise"):
    """
    Builds a prompt asking Gemini to rewrite/transform the given text.

    Args:
        original_text (str): the extracted clause or contract text
        rewriting_style (str): tone or format the user expects (optional)

    Returns:
        str: final formatted prompt
    """
    if not original_text or original_text.strip() == "":
        return "Rewrite the text professionally."

    prompt = f"""
You are an AI agent that rewrites legal and technical content.

Rewrite the following text in a {rewriting_style} tone.
Preserve the meaning accurately, do not add extra information,
do not remove legally important details.

TEXT TO REWRITE:
\"\"\"{original_text}\"\"\" 

OUTPUT FORMAT REQUIREMENTS:
- No explanation
- Just the rewritten text
"""

    return prompt.strip()
