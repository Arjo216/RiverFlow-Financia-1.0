import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# LangChain RAG Ecosystem
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

# Silence LangChain telemetry warnings
os.environ["LANGCHAIN_TRACING_V2"] = "false"

load_dotenv()

# --- ARCHITECTURE SETUP ---
DB_PASS = os.getenv("DB_PASSWORD", "secretpassword")
# Formatted specifically for PGVector and psycopg2
CONNECTION_STRING = f"postgresql+psycopg2://admin:{DB_PASS}@sentient_db:5432/sentient_alpha"
COLLECTION_NAME = "institutional_research"

print("💠 RIVERFLOW APEX: SEC RAG INGESTOR ONLINE")

# 1. INITIALIZE EMBEDDING ENGINE
# We use all-MiniLM-L6-v2: Fast, local, and highly optimized for financial semantics
print("⚙️ Booting HuggingFace Vector Engine...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. THE SEC ACQUISITION PROTOCOL
def fetch_mstr_10k():
    print("📡 Targeting the FRESH 2026 MicroStrategy 10-K...")
    
    headers = {
        'User-Agent': 'RiverFlowQuant/1.0 (admin@riverflow.com) ResearchBot/2.0',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
    }
    
    # 🎯 CONFIRMED 2026 FILING PATH (Filed Feb 19, 2026)
    primary_url = "https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm"
    # 🎯 FAILOVER: TEXT-ONLY VERSION (More stable against scraper blocks)
    backup_url = "https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/0001050446-26-000020.txt"

    for url in [primary_url, backup_url]:
        try:
            print(f"📥 Attempting download from: {url[-30:]}")
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                print("✅ Direct Secure Link Established.")
                soup = BeautifulSoup(response.content, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                return soup.get_text(separator='\n', strip=True)
            else:
                print(f"⚠️ URL failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Connection glitch: {e}")
            continue

    raise Exception("❌ SEC Global Block: All automated paths rejected.")
    
# 3. EXECUTION PIPELINE
def run_ingestion():
    raw_text = fetch_mstr_10k()
    print(f"✅ Acquired Document: {len(raw_text):,} characters of pure data.")
    
    # Chunking: We cannot feed 100 pages to Groq at once. We break it into chunks.
    # The 200-character overlap ensures we don't accidentally cut a sentence in half.
    print("🔪 Slicing document into strategic vector chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = splitter.split_text(raw_text)
    
    # Add metadata for "Citation Tracking" (Phase A compliance requirement)
    docs = [
        Document(
            page_content=chunk, 
            metadata={"source": "MSTR_10-K", "type": "SEC_FILING", "chunk_id": i}
        ) for i, chunk in enumerate(chunks)
    ]
    
    print(f"🧠 Generated {len(docs)} high-density context vectors.")
    
    # 4. INJECT INTO TIMESCALEDB
    print("💾 Injecting vectors into TimescaleDB Vault...")
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=True # Overwrites old data for a clean slate
    )
    
    print("🎯 RAG INGESTION COMPLETE. The Database is primed.")

if __name__ == "__main__":
    run_ingestion()