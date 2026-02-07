from config.llm import get_llm

def testing_agent(code: str, requirement: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a QA engineer.

Test the generated code against the requirement.

RULES:
- Do NOT rewrite the code
- Provide clear results
- Mention PASS or FAIL
- Suggest fixes if failed

Requirement:
{requirement}

Code:
{code}

FORMAT:
### TEST_RESULT
Status: PASS/FAIL
Reason:
Suggestions:
"""

    response = llm.invoke(prompt)
    return response.content