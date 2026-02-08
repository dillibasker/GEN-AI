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

def planning_agent(requirement: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a senior software architect.

Generate a clear step-by-step PLAN for the following requirement.

RULES:
- Use numbered steps
- Be concise
- Do NOT include code
- Output only the plan

Requirement:
{requirement}

FORMAT:
### PLAN
1. ...
2. ...
"""
    final_output = ""
    for chunk in llm.stream(prompt):
        text = extract_text(chunk.content)
        if text:
            print(text, end="", flush=True)
            final_output += text

    return final_output
