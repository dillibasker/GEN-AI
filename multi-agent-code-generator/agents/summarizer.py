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


def summarizing_agent(requirement: str, plan: str, design: str, code: str, test_result: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a technical documentation agent in a multi-agent AI system.

Your job is to generate a professional executive summary.

Requirement:
{requirement}

Plan Created:
{plan}

Design Produced:
{design}

Generated Code:
{code}

Test Result:
{test_result}

Write a structured summary explaining:

- What the requirement was
- How it was planned
- How it was designed
- How it was implemented
- Testing outcome
- Final conclusion

Keep it concise, professional, and clear.
Do NOT include raw code in the summary.
Output only the summary text.
"""

    final_output = ""

    try:
        # STREAMING MODE
        for chunk in llm.stream(prompt):
            text = extract_text(chunk.content)
            if text:
                print(text, end="", flush=True)
                final_output += text

        return final_output

    except Exception as e:
        error_msg = str(e).lower()

        if "overloaded" in error_msg or "503" in error_msg:
            print("\n\n Gemini overloaded. Switching to non-streaming mode...\n")
        else:
            print(f"\n\n Streaming failed: {e}\nSwitching to fallback...\n")

    # FALLBACK MODE
    try:
        response = llm.invoke(prompt)
        final_text = extract_text(response.content)
        print(final_text)
        return final_text

    except Exception as e:
        print(f"\nFailed to generate summary: {e}")
        return ""