from pathlib import Path
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Step 1: Load your chunked JSON file
file_path = Path("data/processed/chunked_filings.json")

with open(file_path, "r", encoding="utf-8") as f:
    chunk_data = json.load(f)

print(f"Loaded {len(chunk_data)} chunk records.")

# Step 2: Turn each chunk into a LangChain Document
documents = []

for record in chunk_data:
    doc = Document(
        page_content=record["chunk_text"],
        metadata={
            "filename": record["filename"],
            "company": record["company"],
            "year": record["year"],
            "chunk_id": record["chunk_id"]
        }
    )
    documents.append(doc)

print(f"Converted {len(documents)} records into Document objects.")

# Step 3: Load the embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 4: Build the FAISS vector store
vectorstore = FAISS.from_documents(documents, embeddings)

# Step 5: Save it locally
output_folder = "data/processed/faiss_index"
vectorstore.save_local(output_folder)

print(f"FAISS index saved to: {output_folder}")