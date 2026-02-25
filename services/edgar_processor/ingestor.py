import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

# Load Vault Keys
load_dotenv()
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")

# 🔗 Institutional Database Link (Notice it uses postgresql+psycopg2 for LangChain)
DB_URL = f"postgresql+psycopg2://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"
COLLECTION_NAME = "institutional_research"

def arm_the_vault(file_path):
    print(f"\n💠 RIVERFLOW APEX 4.0: DATA INGESTOR INITIALIZING...")
    
    # --- PHASE 1: TARGET ACQUISITION ---
    print(f"📄 [PHASE 1] Loading Institutional Document: {file_path}")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # --- PHASE 2: THE SLICER ---
    print("✂️ [PHASE 2] Slicing text into Neural Chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"   -> Successfully sliced into {len(chunks)} overlapping vectors.")
    
    # --- PHASE 3: NEURAL TRANSLATION ---
    print("🧠 [PHASE 3] Waking up HuggingFace Embedding Engine...")
    # This runs a localized AI model to turn English into Math
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # --- PHASE 4: THE VAULT DROP ---
    print("💾 [PHASE 4] Injecting Vectors into PostgreSQL Vault...")
    store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=DB_URL,
        pre_delete_collection=False  # Set to True if you ever want to wipe the vault first
    )
    
    print("\n✅ INGESTION COMPLETE. The RAG Vault is now armed.")

if __name__ == "__main__":
    # Point the Ingestor at the Bitcoin Whitepaper
    target_pdf = "/app/data/btc_whitepaper.pdf"
    
    if os.path.exists(target_pdf):
        arm_the_vault(target_pdf)
    else:
        print(f"⚠️ [ERROR] Could not find {target_pdf}. Did you map the volume correctly?")