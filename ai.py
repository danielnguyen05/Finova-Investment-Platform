from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template = (
    "You are an AI assistant. Answer the user's question as accurately and concisely as possible.\n"
    "Question: {user_query}\n"
    "Answer:"
)

def chat_with_ai():
    """Runs an interactive chat loop in the terminal."""
    print("AI Chatbot (Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ") 
        
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        response = chain.invoke({"user_query": user_input})
        
        print(f"AI: {response}\n")

if __name__ == "__main__":
    chat_with_ai()
