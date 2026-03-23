from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama
from src.agents.tools import search_10k, summarize_text


def create_agent():
    llm = ChatOllama(
        model="llama3",
        temperature=0
    )

    tools = [search_10k, summarize_text]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        max_iterations=4,
        early_stopping_method="generate",
        handle_parsing_errors=True,
        agent_kwargs={
            "prefix": """You are a financial research assistant.

Always follow this rule:
After using tools, you MUST produce a final answer.

Do NOT stop at Thought or Action.
Always end with:

Final Answer: <your answer>

For comparison questions, you MUST explicitly compare each company mentioned.
Include at least one point for each company and clearly contrast them.
If the question is about one company, answer only for that company.
Do not introduce other companies unless the question explicitly asks for comparison.
Do not return only Thought, Action, or Action Input.
Do not repeat the question.
Use the tools when needed, then finish with a concise professional answer."""
        }
    )

    return agent