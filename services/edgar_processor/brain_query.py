import argparse
import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🧠 ORACLE - %(message)s')
DB_CONNECTION = "postgresql+psycopg2://admin:secretpassword@timescaledb:5432/sentient_alpha"

def query_brain(question, k=3):
    logging.info(f"Encoding Question: '{question}'...")
    
    # Load Model (CPU)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} 
    )

    # Connect to DB
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="financial_filings",
        connection=DB_CONNECTION,
        use_jsonb=True,
    )

    # Search
    logging.info("Scanning Neural Database...")
    results = vector_store.similarity_search_with_score(question, k=k)

    print(f"\n🔍 --- TOP {k} INSIGHTS FOR: '{question}' ---\n")
    for i, (doc, score) in enumerate(results):
        relevance = 1 - score 
        print(f"📄 Result #{i+1} (Relevance: {relevance:.2%})")
        print(f"📝 Content: \"{doc.page_content[:300]}...\"")
        print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str)
    args = parser.parse_args()
    query_brain(args.question)