import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# --- CONNECTION PROTOCOL ---
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")
CONNECTION_STRING = f"postgresql+psycopg2://admin:{DB_PASS}@timescaledb:5432/sentient_alpha"
COLLECTION_NAME = "institutional_research"

print("🧠 RIVERFLOW ANALYST AGENT: ONLINE")

# 1. LOAD THE BRAIN (Embeddings + Vector DB)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
store = PGVector(
    connection_string=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings
)

# 2. INITIALIZE THE EXECUTIVE (Groq 70B)
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def ask_analyst(query):
    print(f"\n🔍 Querying Institutional Vault: {query}")
    
    # RETRIEVAL: Find the most relevant 5 chunks from the 10-K
    docs = store.similarity_search(query, k=5)
    context = "\n---\n".join([doc.page_content for doc in docs])
    
    # AUGMENTATION: Build the high-IQ prompt
    prompt = f"""
    SYSTEM: You are a Senior FinTech Analyst specializing in Bitcoin Treasury strategies.
    CONTEXT FROM MICROSTRATEGY 2026 10-K:
    {context}
    
    TASK: Answer the user's question using ONLY the provided context. 
    If the answer isn't in the context, say you don't know.
    Include specific 'Citation IDs' or page themes if visible.
    
    USER QUESTION: {query}
    """
    
    # GENERATION
    response = llm.invoke(prompt)
    print("\n📊 ANALYST REPORT:")
    print("-" * 50)
    print(response.content)
    print("-" * 50)

if __name__ == "__main__":
    # Test Question: What is their total BTC holding as of Feb 2026?
    ask_analyst("Summarize MicroStrategy's Bitcoin acquisition strategy and current debt obligations related to BTC.")