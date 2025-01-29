from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# pip install -U langchain langchain-community langchain-ollama run this in the terminal to install the required packages if it doesnt work

model = OllamaLLM(model="llama3.2")

memory = ChatMessageHistory()

template = (
    "You are an AI assistant. Answer the user's question as accurately and concisely as possible.\n\n"
    "{history}\n"
    "User: {user_query}\n"
    "AI:"
)

prompt = ChatPromptTemplate.from_template(template)

conversation = RunnableWithMessageHistory(
    prompt | model, 
    lambda session_id: memory,  
    input_messages_key="user_query", 
    history_messages_key="history"  
)

def chat_with_ai():
    """Runs an interactive chat loop in the terminal with memory support."""
    print("💬 AI Chatbot (Type 'exit' to quit)\n")

    session_id = "default"  

    while True:
        user_input = input("You: ") 
        
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        response = conversation.invoke(
            {"user_query": user_input}, 
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"AI: {response}\n")

if __name__ == "__main__":
    chat_with_ai()
