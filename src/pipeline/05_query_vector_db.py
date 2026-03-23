from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Step 1: Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 2: Load FAISS vector store
vectorstore = FAISS.load_local(
    "data/processed/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("Vector database loaded.\n")

# Step 3: Define test queries
queries = [
    "What cybersecurity risks does Microsoft mention?",
    "What AI strategy does Microsoft describe?",
    "What regulatory risks does Google disclose?",
    "What supply chain risks does Apple face?",
    "Compare competition risks between Apple and Google"
]

top_k = 3

# Step 4: Define output file
output_path = Path("data/processed/query_results.txt")

with open(output_path, "w", encoding="utf-8") as f:
    for query_num, query in enumerate(queries, start=1):
        header = f"\n{'#' * 100}\nQUERY {query_num}: {query}\n{'#' * 100}\n"
        print(header)
        f.write(header)

        results = vectorstore.similarity_search(query, k=top_k)

        for i, doc in enumerate(results, start=1):
            result_text = (
                f"\n{'=' * 80}\n"
                f"Result {i}\n"
                f"Company: {doc.metadata.get('company', 'N/A')}\n"
                f"Year: {doc.metadata.get('year', 'N/A')}\n"
                f"Chunk ID: {doc.metadata.get('chunk_id', 'N/A')}\n\n"
                f"Text Preview:\n{doc.page_content[:800]}\n\n"
            )
            print(result_text)
            f.write(result_text)

print(f"Results saved to: {output_path}")