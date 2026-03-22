from src.agents.retrieval_agent import RetrievalAgent
from src.agents.answer_agent import AnswerAgent


def main():
    retrieval_agent = RetrievalAgent()
    answer_agent = AnswerAgent(model_name="llama3")

    print("DAIS-8700 Financial Filing Chat")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() == "exit":
            print("Goodbye.")
            break

        docs = retrieval_agent.retrieve(query, k=3)
        answer = answer_agent.answer(query, docs)

        print("\n--- Answer ---\n")
        print(answer)
        
        print("\n--- Sources ---")
        for i, doc in enumerate(docs, start=1):
            print(
                f"{i}. Company: {doc.metadata.get('company', 'N/A')} | "
                f"Year: {doc.metadata.get('year', 'N/A')} | "
                f"Chunk ID: {doc.metadata.get('chunk_id', 'N/A')}"
            )
        print("\n")


if __name__ == "__main__":
    main()