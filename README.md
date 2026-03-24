# DAIS-8700 – Document-Driven Agentic Intelligence System

This repository contains the corpus, data pipeline, and agentic prototype developed for Milestones 2 and 3.


## Corpus

The document corpus consists of six SEC EDGAR 10-K filings for large technology companies:

- Apple (AAPL)
- Microsoft (MSFT)
- Alphabet (GOOGL)

The filings cover fiscal years 2024 and 2025 and are stored in the `data/raw` directory.


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

The data pipeline scripts are located in `src/pipeline` and include:

- `01_ingest_html.py` – loads raw HTML filings
- `02_chunk_filings.py` – extracts and splits text into chunks
- `03_save_chunks_json.py` – saves processed chunks to JSON
- `04_build_faiss.py` – builds the FAISS vector index
- `05_query_vector_db.py` – performs similarity search queries

Note: The FAISS vector index is not included in the repository because it can be rebuilt locally.


## Agentic Prototype (Milestone 3)

The system has been extended into a ReAct-style agent that enables question answering over financial filings using a tool-based architecture.


### Architecture Overview

User Question  
→ Chat / Batch Interface  
→ ReAct Agent (LLM via Ollama)  
→ Tool Selection  
→ FAISS Vector Database (via search_10k)  
→ Retrieved Document Chunks  
→ LLM Synthesis  
→ Final Answer  


## Agent Design (ReAct Framework)

The system uses a ReAct-style agent that combines reasoning and tool usage.

The agent follows a structured process:

- Thought → determine next action  
- Action → call a tool  
- Observation → receive results  
- Final Answer → generate response  

The agent is configured with safeguards such as iteration limits and controlled output to ensure stable responses.


## Tools

The agent has access to two tools:


### search_10k
- Retrieves relevant excerpts from the FAISS vector database  
- Uses semantic similarity search  
- Returns document chunks with metadata (company, year, chunk ID)  


### summarize_text
- Summarizes financial text into concise insights  
- Supports synthesis across retrieved excerpts  

These tools allow the agent to retrieve and reason over financial disclosures.


## Agents (Implementation)

Agent-related components are located in `src/agents`:

- `react_agent.py` – ReAct agent with tool integration  
- `tools.py` – tool definitions (search and summarization)  
- `retrieval_agent.py` – FAISS retrieval wrapper  
- `chat_interface.py` – interactive query interface  
- `batch_query.py` – batch query execution script  


## Chat Interface (Usage)

To run the interactive agent:

python -m src.agents.chat_interface

Example queries:

- What are Microsoft's main business segments?
- What cybersecurity risks does Microsoft mention?
- What supply chain risks does Apple disclose?

The chat interface allows users to interact with the agent in real time and receive grounded answers based on SEC 10-K filings.


## Batch Query Interface

To run predefined evaluation queries:

python -m src.agents.batch_query

Results are saved to:

data/processed/ml3_batch_answers.txt

This file contains:

- query text  
- generated answers  
- structured outputs  

The batch interface enables automated testing and evaluation of the agent across multiple financial questions.


## System Characteristics

- Retrieval-Augmented Generation (RAG)
- ReAct-style agent architecture
- Tool-based reasoning framework
- Local vector database using FAISS
- Local LLM inference using Ollama (llama3)
- Metadata-aware document retrieval
- Supports both single-entity and comparison queries


## Limitations

- Retrieval quality may vary depending on query phrasing  
- Fixed-size chunking may split important context  
- The system does not perform section-aware filtering (e.g., Risk Factors vs Financial Statements)  
- Answers depend on the relevance of retrieved chunks  
- Comparison queries may require broader retrieval to ensure balanced responses  


## Installation

To install required dependencies:

pip install -r requirements.txt


## Repository

GitHub Repository:  
https://github.com/alessandropuleos-ui/dais-8700