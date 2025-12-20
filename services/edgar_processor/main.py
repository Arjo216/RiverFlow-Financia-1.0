import os
import time
import huggingface_hub
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# 1. Database Connection
DB_CONNECTION = "postgresql+psycopg2://admin:secretpassword@timescaledb:5432/sentient_alpha"

def run_ingestion():
    print("🤖 Analyst Agent Starting...")

    # --- SECURE AUTHENTICATION (The Fix) ---
    # ERROR WAS HERE: Removed the quotes around the command
    token = os.getenv("HF_TOKEN") 
    
    if token:
        print(f"🔑 Logging in with token: {token[:5]}...") 
        try:
            huggingface_hub.login(token=token)
            print("✅ Login Successful!")
        except Exception as e:
            print(f"❌ Login Failed: {e}")
    else:
        print("⚠️ Warning: No HF_TOKEN found. Model download might fail.")
    # ------------------------------------------------

    # 2. Simulate Data
    sample_text = """
    APPLE INC. 10-K FILING SUMMARY (2024)
    Item 1A. Risk Factors:
    The Company's business can be impacted by global economic conditions. 
    Supply chain disruptions, including those affecting semiconductor manufacturing, could limit ability to sell products.
    The Company relies on third-party intellectual property and digital content.
    Competition in the technology sector is intense and characterized by rapid change.
    """
    
    print(f"📄 Reading Financial Document ({len(sample_text)} chars)...")
    
    # 3. Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([sample_text])
    
    # 4. Embeddings
    print("🧠 Loading AI Model (All-MiniLM-L6-v2)...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception as e:
        print(f"❌ Model Load Failed: {e}")
        return

    # 5. Save to Vector DB
    print("💾 Saving to Vector Database...")
    try:
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name="financial_filings",
            connection=DB_CONNECTION,
            use_jsonb=True,
        )
        vector_store.add_documents(docs)
        print("✅ Ingestion Complete! The AI has memorized the document.")
    except Exception as e:
        print(f"❌ Database Error: {e}")

    # Keep alive
    while True:
        time.sleep(600)  # <-- Fixed: Added 600 seconds here

if __name__ == "__main__":
    time.sleep(10)
    run_ingestion()