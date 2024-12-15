import requests

# Wolfram Alpha API Key
WOLFRAM_API_KEY = "APER4E-58XJGHAVAK"

def ask_wolfram_alpha(query):
    """Send a query to Wolfram Alpha API and return the response."""
    base_url = "http://api.wolframalpha.com/v1/result"
    params = {
        "appid": WOLFRAM_API_KEY,
        "i": query
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return "Sorry, I couldn't fetch the answer."

def chatbot():
    print("Wolfram Alpha Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        answer = ask_wolfram_alpha(user_input)
        print(f"Chatbot: {answer}")

if __name__ == "__main__":
    chatbot()
