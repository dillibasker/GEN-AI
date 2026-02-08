from config.llm import get_llm

def extract_text(content):
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text = ""
        for item in content:
            if isinstance(item, dict) and "text" in item:
                text += item["text"]
        return text

    return ""

def creating_agent(design: str, language: str) -> str:
    llm = get_llm()

    prompt = f"""
You are an expert {language} developer.

Generate production-ready code based on the design below.

STRICT RULES:
- Output ONLY code
- Wrap code inside triple backticks
- Mention language after backticks
- No explanations outside code

Design:
{design}

FORMAT:
```{language}
<code here>
"""
    final_output = ""
    for chunk in llm.stream(prompt):
        text = extract_text(chunk.content)
        if text:
            print(text, end="", flush=True)
            final_output += text

    return final_output
