from langchain_ollama import ChatOllama


class AnswerAgent:
    def __init__(self, model_name="llama3"):
        self.llm = ChatOllama(
            model=model_name,
            num_predict=250,
            temperature=0
        )

    def build_prompt(self, query: str, docs):
        context_parts = []

        for i, doc in enumerate(docs, start=1):
            context_parts.append(
                f"[Document {i}]\n"
                f"Company: {doc.metadata.get('company', 'N/A')}\n"
                f"Year: {doc.metadata.get('year', 'N/A')}\n"
                f"Chunk ID: {doc.metadata.get('chunk_id', 'N/A')}\n"
                f"Text:\n{doc.page_content}\n"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a financial research assistant helping an equity analyst.

Use only the retrieved excerpts below to answer the user's question.
Do not make up facts.
If the answer is not clearly supported by the excerpts, say so.
Write one concise professional paragraph or a short bullet list only when clearly helpful.
Do not repeat yourself.
Do not include a Sources section.
Do not restate the question.

User Question:
{query}

Retrieved Excerpts:
{context}

Answer:
"""
        return prompt

    def answer(self, query: str, docs):
        prompt = self.build_prompt(query, docs)
        response = self.llm.invoke(prompt)
        answer_text = response.content.strip()

        # Basic cleanup for repeated or accidental "Sources:" text from model output
        if "Sources:" in answer_text:
            answer_text = answer_text.split("Sources:")[0].strip()

        return answer_text