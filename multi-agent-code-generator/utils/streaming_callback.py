from langchain_core.callbacks import BaseCallbackHandler
import sys

class StreamingHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []

    def on_llm_new_token(self, token, **kwargs):
        if token is None:
            return

        text = ""

        if isinstance(token, list):
            text = "".join(t for t in token if isinstance(t, str))
        elif isinstance(token, dict):
            text = token.get("text", "")
        elif isinstance(token, str):
            text = token

        if text:
            self.tokens.append(text)
            sys.stdout.write(text)
            sys.stdout.flush()

    def get_text(self):
        return "".join(self.tokens)
