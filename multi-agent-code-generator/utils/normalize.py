def normalize_output(output):
    # Handle None safely
    if output is None:
        return ""

    # Case 1: already a string
    if isinstance(output, str):
        return output.strip()

    # Case 2: list (Gemini / LangChain responses)
    if isinstance(output, list):
        texts = []
        for item in output:
            if isinstance(item, str):
                texts.append(item)
            elif isinstance(item, dict):
                texts.append(item.get("content", ""))
        return "\n".join(texts).strip()

    # Case 3: dict response
    if isinstance(output, dict):
        return output.get("content", "").strip()

    # Fallback
    return str(output).strip()
