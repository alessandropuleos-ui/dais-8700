# DAIS-8700 – Document-Driven Agentic Intelligence System

This repository contains the corpus, data pipeline, and agentic prototype developed for Milestones 2 and 3.

## Corpus

The document corpus consists of six SEC EDGAR 10-K filings for large technology companies:

- Apple (AAPL)
- Microsoft (MSFT)
- Alphabet (GOOGL)

The filings cover fiscal years 2024 and 2025 and are stored in the data/raw directory.

## Processed Data

The processed dataset is stored in:

data/processed/chunked_filings.json

This file contains 1,518 text chunks extracted from the filings, each with metadata including:

- filename
- company
- year
- chunk_id
- chunk_text

## Data Pipeline (Milestone 2)

The data pipeline scripts are located in src/pipeline and include:

- 01_ingest_html.py – loads raw HTML filings
- 02_chunk_filings.py – extracts and splits text into chunks
- 03_save_chunks_json.py – saves processed chunks to JSON
- 04_build_faiss.py – builds the FAISS vector index
- 05_query_vector_db.py – performs similarity search queries

Note: The FAISS vector index is not included in the repository because it can be rebuilt locally.

## Agentic Prototype (Milestone 3)

The system has been extended into a working multi-agent pipeline that enables question answering over financial filings.

Architecture Overview:

User Question
→ Retrieval Agent (FAISS similarity search)
→ Relevant document chunks
→ Answer Agent (LLM via Ollama)
→ Final grounded response

## Agents

The agent-based components are located in src/agents:

- retrieval_agent.py – retrieves relevant chunks from the FAISS vector store
- answer_agent.py – generates answers using a local LLM (Ollama)
- chat_interface.py – interactive question-answering interface
- batch_query.py – batch processing of predefined queries

## Chat Interface

To run the interactive chat system:

python -m src.agents.chat_interface

You can then ask questions such as:

- What are Microsoft's main business segments?
- What risks does Apple disclose in its filings?

## Batch Query Interface

To run predefined evaluation queries:

python -m src.agents.batch_query

Results will be saved to:

data/processed/ml3_batch_answers.txt

This file contains:

- query text
- generated answers
- supporting document sources

## System Characteristics

- Retrieval-Augmented Generation (RAG) architecture
- Local vector database using FAISS
- Local LLM inference using Ollama
- Metadata-aware document retrieval
- Source-grounded answers

## Limitations

- Retrieval quality may vary depending on the query
- Some chunks may not fully capture context due to fixed-size chunking
- The system does not yet perform section-aware or semantic filtering
- Answers depend heavily on the relevance of retrieved chunks

## Installation

To install required dependencies:

pip install -r requirements.txt