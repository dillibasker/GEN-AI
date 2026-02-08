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
    final_output = ""

    try:
        #  STREAMING MODE
        for chunk in llm.stream(prompt):
            text = extract_text(chunk.content)
            if text:
                print(text, end="", flush=True)
                final_output += text

        return final_output  # exit if streaming works

    except Exception as e:
        error_msg = str(e).lower()

        if "overloaded" in error_msg or "503" in error_msg:
            print("\n\n Gemini overloaded. Switching to non-streaming mode...\n")
        else:
            print(f"\n\n  Streaming failed: {e}\nSwitching to fallback...\n")

    # FALLBACK MODE
    try:
        response = llm.invoke(prompt)
        final_text = extract_text(response.content)
        print(final_text)
        return final_text

    except Exception as e:
        print(f"\n Failed to generate test result: {e}")
        return ""