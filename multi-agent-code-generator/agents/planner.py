from config.llm import get_llm

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

    response = llm.invoke(prompt)
    return response.content.strip()
