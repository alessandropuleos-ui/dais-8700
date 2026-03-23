from pathlib import Path
from src.agents.react_agent import create_agent


def main():
    agent = create_agent()

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

            response = agent.run(query)

            header = f"{'#' * 100}\nQUERY {i}: {query}\n{'#' * 100}\n"
            f.write(header)
            f.write("Answer:\n")
            f.write(response)
            f.write("\n\n")

            f.flush()

    print(f"Batch answers saved to: {output_path}")


if __name__ == "__main__":
    main()