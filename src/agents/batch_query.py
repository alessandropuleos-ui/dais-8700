from pathlib import Path
from src.agents.retrieval_agent import RetrievalAgent
from src.agents.answer_agent import AnswerAgent


def main():
    retrieval_agent = RetrievalAgent()
    answer_agent = AnswerAgent(model_name="llama3")

    queries = [
        "What cybersecurity risks does Microsoft mention?",
        "What supply chain risks does Apple disclose?",
        "What regulatory risks does Alphabet report?",
        "Compare competition risks between Apple and Google."
    ]

    output_path = Path("data/processed/ml3_batch_answers.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        for i, query in enumerate(queries, start=1):
            print(f"Running query {i}: {query}")

            docs = retrieval_agent.retrieve(query, k=3)
            answer = answer_agent.answer(query, docs)

            header = f"{'#' * 100}\nQUERY {i}: {query}\n{'#' * 100}\n"
            f.write(header)
            f.write("Answer:\n")
            f.write(answer)
            f.write("\n\nSources:\n")

            for j, doc in enumerate(docs, start=1):
                source_line = (
                    f"{j}. Company: {doc.metadata.get('company', 'N/A')} | "
                    f"Year: {doc.metadata.get('year', 'N/A')} | "
                    f"Chunk ID: {doc.metadata.get('chunk_id', 'N/A')}\n"
                )
                f.write(source_line)

            f.write("\n")
            f.flush()

    print(f"Batch answers saved to: {output_path}")


if __name__ == "__main__":
    main()