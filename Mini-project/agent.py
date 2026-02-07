from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector database
db = Chroma(
    persist_directory="./db",
    embedding_function=embeddings
)

def rag_answer(question: str) -> str:
    # Retrieve relevant documents
    docs = db.similarity_search(question, k=3)

    if not docs:
        return "This information is not available in the college rules."

    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a college rules assistant.
Answer ONLY using the information given below.
Do not guess or add extra information.

College Rules:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content


# Test
question = "How should students apply for leave?"
answer = rag_answer(question)
print(answer)
