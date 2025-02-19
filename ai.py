import os
import json
import re
import string
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# AI model and memory
model = OllamaLLM(model="llama3.2")
memory = ChatMessageHistory()

# Load all financial data at startup
company_data = {}  # Dictionary: {"AAPL": {data}, "TSLA": {data}, ...}
company_mapping = {}  # Maps company names (lowercase) to tickers

def load_all_company_data() -> dict:
    '''
    Loads all JSON files and builds a mapping of names to tickers, stored as global variables.
    '''
    directory = "Company_Overviews"

    if not os.path.exists(directory):
        print("Error: Company_Overviews directory not found.")
        return

    for filename in os.listdir(directory):
        if filename.endswith("_overview.json"):
            ticker = filename.split("_")[0]
            filepath = os.path.join(directory, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    company_data[ticker] = data
                    if "Name" in data:
                        company_mapping[data["Name"].lower()] = ticker
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {filename}")

load_all_company_data()

def clean_word(word: str) -> str:
    '''
    Processes a word for querying.
    '''
    word = word.strip(string.punctuation)
    word = re.sub(r"'s$", "", word)
    return word

def get_ticker(query_word: str) -> str:
    '''
    Gets the ticker from the global variables, by matching substrings.
    '''
    cleaned_word = clean_word(query_word)
    for name in company_mapping:
        if cleaned_word in name:
            return company_mapping[name]
    return None

def kmp_search_with_threshold(text, target, threshold=0.8):
    '''
    Implements KMP algorithm to find if there's a [threshold] match of the target string in the text.
    '''
    
    def build_prefix_table(target):
        m = len(target)
        lps = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and target[i] != target[j]:
                j = lps[j - 1]
            if target[i] == target[j]:
                j += 1
                lps[i] = j
            else:
                lps[i] = 0
        return lps

    n = len(text)
    m = len(target)
    
    lps = build_prefix_table(target)
    
    i = 0
    j = jmax = 0
    
    while i < n:
        if text[i] == target[j]:
            i += 1
            j += 1
            if j == m:
                return True
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
        
        if j >= threshold * m:
            return True
        if j > jmax:
            jmax = j
    return False

def is_statistical_query(user_query: str) -> bool:
    '''
    Checks if the query is asking about stock-related stats.
    '''
    keywords = [
                    "Symbol",
                    "AssetType",
                    "Description", 
                    "CIK", 
                    "Exchange",
                    "Currency",
                    "Sector",
                    "Industry",
                    "Address",
                    "OfficialSite",
                    "FiscalYearEnd",
                    "LatestQuarter",
                    "MarketCapitalization",
                    "EBITDA",
                    "PERatio",
                    "PEGRatio",
                    "BookValue",
                    "DividendPerShare",
                    "DividendYield",
                    "EPS",
                    "RevenuePerShareTTM",
                    "ProfitMargin",
                    "OperatingMarginTTM",
                    "ReturnOnAssetsTTM",
                    "ReturnOnEquityTTM",
                    "RevenueTTM",
                    "GrossProfitTTM",
                    "DilutedEPSTTM",
                    "QuarterlyEarningsGrowthYOY",
                    "QuarterlyRevenueGrowthYOY",
                    "TrailingPE",
                    "ForwardPE",
                    "PriceToSalesRatioTTM",
                    "PriceToBookRatio",
                    "EVToRevenue",
                    "EVToEBITDA",
                    "Beta",
                    "52WeekHigh",
                    "52WeekLow",
                    "50DayMovingAverage",
                    "200DayMovingAverage",
                    "SharesOutstanding",
                    "DividendDate",
                    "ExDividendDate"
                ]
    return any(kmp_search_with_threshold(user_query.lower().replace(" ", ""), keyword.lower().replace(" ", "")) for keyword in keywords)

def get_statistical_answer(user_query: str) -> str:
    '''
    Finds the correct ticker and fetches financial data.
    '''
    words = user_query.lower().split()
    
    for word in words:
        ticker = get_ticker(word)
        if ticker:
            break
    else:
        return "Sorry, I couldn't identify the company. Try using a stock ticker, or recheck the company's name."

    data = company_data.get(ticker)
    if not data:
        return f"Sorry, no financial data found for {ticker}."
    
    for key, value in data.items():
        if kmp_search_with_threshold(user_query.lower().replace(" ", ""), key.lower()):
            return f"{data['Name']} ({ticker}) has a {key} of {value}."

    return f"Sorry, no matching statistic found for {ticker}."

template = (
    "You are a finance AI assistant. Use the provided financial data when necessary.\n\n"
    "If the user asks a question that is not related to finance or economics, don't answer it. \n'"
    "If you are unsure of an answer to a question, or, if there are any parts of the question that you do not understand, ask for clarification. \n"
    "Do not provide any financial advice.\n"
    "Do not answer any specific questions about you, the AI (e.g, database updates, knowledge cutoffs, etc.)\n"
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

def get_response(user_query: str) -> str:
    '''
    Determines whether to fetch financial data or answer freely.
    '''
    if is_statistical_query(user_query):
        return get_statistical_answer(user_query)
    
    return conversation.invoke({"user_query": user_query}, config={"configurable": {"session_id": "default"}})

def chat_with_ai() -> None:
    '''
    Runs an interactive chat session.
    '''
    print("💬 Finance AI Chatbot (Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        response = get_response(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    chat_with_ai()
