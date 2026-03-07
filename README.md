# DAIS-8700 – Document-Driven Agentic Intelligence System

This repository contains the corpus and data pipeline developed for Milestone 2.

## Corpus
The document corpus consists of six SEC EDGAR 10-K filings for large technology companies:

- Apple (AAPL)
- Microsoft (MSFT)
- Alphabet (GOOGL)

The filings cover fiscal years 2024 and 2025 and are stored in the `data/raw` directory.

## Processed Data
The processed dataset is stored in:

`data/processed/chunked_filings.json`

This file contains 1,518 text chunks extracted from the filings, each with metadata including:

- filename
- company
- year
- chunk_id
- chunk_text

## Pipeline Scripts
The data pipeline scripts are located in `src/pipeline` and include:

- `01_ingest_html.py` – loads raw HTML filings
- `02_chunk_filings.py` – extracts and splits text into chunks
- `03_save_chunks_json.py` – saves processed chunks to JSON
- `04_build_faiss.py` – builds the FAISS vector index
- `05_query_vector_db.py` – performs similarity search queries

## Note
The FAISS vector index is not included in the repository because it can be rebuilt locally using the pipeline script.