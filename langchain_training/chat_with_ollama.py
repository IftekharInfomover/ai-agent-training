from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Initialize the Ollama model
llm = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0.7
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful chatbot powered by DeepSeek-R1. Provide clear and concise answers."),
    *[],  # Placeholder for conversation history
    HumanMessage(content="{{user_input}}")
])

# Initialize conversation history
history = []

def main():
    print("Welcome to the DeepSeek-R1 Chatbot! Type 'exit' to quit.")

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user message to history
        history.append(HumanMessage(content=user_input))

        # Prepare the prompt with history
        messages = [
                       SystemMessage(content="You are a helpful chatbot powered by DeepSeek-R1. Provide clear and concise answers.")
                   ] + history

        # Update prompt with current messages
        formatted_prompt = ChatPromptTemplate.from_messages(messages)

        # Create the chain
        chain = formatted_prompt | llm

        # Invoke the model
        try:
            response = chain.invoke({"user_input": user_input})
            response_text = response.content

            # Add model response to history
            history.append(AIMessage(content=response_text))

            # Print response
            print(f"Bot: {response_text}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()