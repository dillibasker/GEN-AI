def normalize_output(output):
    # Case 0: None
    if output is None:
        return ""

    # Case 1: string
    if isinstance(output, str):
        return output.strip()

    # Case 2: list (Gemini / LangChain)
    if isinstance(output, list):
        texts = []
        for item in output:
            if isinstance(item, str):
                texts.append(item)
            elif isinstance(item, dict):
                # Gemini uses "text", not "content"
                if "text" in item:
                    texts.append(item["text"])
                elif "content" in item:
                    texts.append(item["content"])
        return "\n".join(texts).strip()

    # Case 3: dict
    if isinstance(output, dict):
        if "text" in output:
            return output["text"].strip()
        if "content" in output:
            return output["content"].strip()

    # Fallback
    return str(output).strip()
