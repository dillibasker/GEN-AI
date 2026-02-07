from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load text file
loader = TextLoader("data/rules.txt")
docs = loader.load()

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector DB (auto-persist)
db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="./db"
)

print("Vector DB created and persisted successfully")
