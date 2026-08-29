from langchain_ollama import ChatOllama


def create_llm() -> ChatOllama:
    return ChatOllama(
        model="gemma4:latest",
        temperature=0,
    )


def ask_llm(llm: ChatOllama, question: str) -> str:
    response = llm.invoke(question)
    return response.content


def main():
    llm = create_llm()

    question = input("Ask Gemma: ")
    answer = ask_llm(llm, question)

    print("\nGemma:")
    print(answer)


if __name__ == "__main__":
    main()