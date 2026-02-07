from config.llm import get_llm

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
    response = llm.invoke(prompt)
    return response.content.strip()
