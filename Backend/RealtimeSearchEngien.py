#SECTION - Importing the necessary libraries
from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

#ANCHOR - load env variables from .env file
env_vars = dotenv_values(".env")

#*NOTE - Retrieve the environment variables for Username, assistant name, and API key *# 
Username = env_vars.get("Username")
Assistantname = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the API key
client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

#STUB - Attempt to load the chat log from a JSON file
def load_messages():
    try:
        with open(r"Data\Chatlog.json", "r") as f:
            return load(f)
    except FileNotFoundError:
        return []

def save_messages(messages):
    with open(r"Data\Chatlog.json", "w") as f:
        dump(messages, f, indent=4)

# Load messages initially
messages = load_messages()

# Function to validate messages
def validate_messages(messages):
    for msg in messages:
        if "role" not in msg or "content" not in msg or not msg["content"]:
            raise ValueError(f"Invalid message format: {msg}")

# Function to perform Google search and format the result
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

#STUB - Function to format the Chat response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"},
]

#STUB - Function to get real-time info
def Information():
    current_date_time = datetime.datetime.now()  # NOTE Get current date and time
    day = current_date_time.strftime("%A")      # Day of the week
    date = current_date_time.strftime("%d")     # Day of the month
    month = current_date_time.strftime("%B")    # Month name
    year = current_date_time.strftime("%Y")     # Year
    hour = current_date_time.strftime("%H")     # Hour in 24-hour format
    minute = current_date_time.strftime("%M")   # Minute
    second = current_date_time.strftime("%S")   # Second
    data = f"Use this real-time information if needed, \n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minute, {second} second.\n"
    return data

#STUB - Function to process real-time queries
def RealtimeSearchEngine(prompt):
    global messages

    # Load messages from file
    messages = load_messages()
    
    # Add user input to messages
    messages.append({"role": "user", "content": prompt})

    # Local copy of SystemChatBot to avoid growth
    local_system_chatbot = SystemChatBot.copy()
    local_system_chatbot.append({"role": "system", "content": GoogleSearch(prompt)})

    try:
        # Validate all messages
        validate_messages(local_system_chatbot + [{"role": "system", "content": Information()}] + messages)

        # Generate response using Groq client
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=local_system_chatbot + [{"role": "system", "content": Information()}] + messages,
            max_tokens=3072,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Process response chunks
        Answer = ""  # Initialize an empty string to store the AI's response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        save_messages(messages)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error during API call: {e}")
        return "An error occurred while processing your request."

#*NOTE - Execute the script
if __name__ == '__main__':
    while True:
        prompt = input("Enter Your Query (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        print(RealtimeSearchEngine(prompt))
