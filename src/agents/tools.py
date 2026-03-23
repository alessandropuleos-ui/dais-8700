from langchain.tools import tool
from src.agents.retrieval_agent import RetrievalAgent

retrieval_agent = RetrievalAgent()


@tool
def search_10k(query: str) -> str:
    """
    Search the 10-K filings and return the most relevant excerpts.
    Use this tool when the user asks about risks, strategy, segments, revenue,
    regulation, or comparisons across Apple, Microsoft, and Alphabet.
    """
    cleaned_query = (
        query.replace("AND", " ")
             .replace("OR", " ")
             .replace("and", " ")
             .replace("or", " ")
             .replace("(", " ")
             .replace(")", " ")
             .replace('"', " ")
    )

    lower_query = cleaned_query.lower()

    # Only boost all companies for explicit comparison questions
    if "compare" in lower_query or "between" in lower_query:
        final_query = cleaned_query + " Apple Google Alphabet Microsoft competition risk"
        k = 6
    else:
        final_query = cleaned_query
        k = 5

    docs = retrieval_agent.retrieve(final_query, k=k)

    results = []
    for doc in docs:
        results.append(
            f"Company: {doc.metadata['company']}, "
            f"Year: {doc.metadata['year']}, "
            f"Chunk ID: {doc.metadata['chunk_id']}\n"
            f"{doc.page_content[:700]}"
        )

    return "\n\n".join(results)


@tool
def summarize_text(text: str) -> str:
    """
    Summarize financial text into key insights.
    """
    return f"Summary of the text:\n{text[:300]}"