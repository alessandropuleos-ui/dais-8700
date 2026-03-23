from src.agents.react_agent import create_agent


def main():
    agent = create_agent()
    print(type(agent))

    print("DAIS-8700 Financial Filing Chat")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() == "exit":
            print("Goodbye.")
            break

        response = agent.run(query)

        print("\n--- Answer ---\n")
        print(response)
        print("\n")


if __name__ == "__main__":
    main()