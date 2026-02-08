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

def designing_agent(plan: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a Designing Agent.

Based on the plan, design:
- Architecture
- Modules
- Functions
- Data flow

RULES:
- No code
- Clear explanation
- Structured output

Plan:
{plan}
"""
    final_output = ""
    for chunk in llm.stream(prompt):
        text = extract_text(chunk.content)
        if text:
            print(text, end="", flush=True)
            final_output += text

    return final_output
