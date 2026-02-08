from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-3-flash-preview",
        temperature=0.2,
        google_api_key="AIzaSyDhJVEoYyTx0bOGjcpmrWA4eon1G_w8CoE"
    )
