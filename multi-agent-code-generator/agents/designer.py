from config.llm import get_llm

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

    response = llm.invoke(prompt)
    return response.content.strip()
