#SECTION - Importing the necessary libraries
from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values 

#ANCHOR - load env variables from .env file
env_vars = dotenv_values(".env")

#*NOTE - Retrive the enviroment variables for Username, assistant name and API key *# 
Username = env_vars.get("Username")
Assistantname = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the API key
client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

#STUB - Attempt to load the chat log from a JSON file
try:
    with open(r"Data\Chatlog.json", "r") as f:
        messages = load(f) # load existing messages
except FileNotFoundError:
    #NOTE if file doesn`t exist create a new JSON file to store Data
    with open(r"Data\Chatlog.json", "w") as f:
        dump([], f)

# Function to perform google search and format the result
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

#STUB - Function to get realtime info
def Information():
    data = ""
    current_date_time = datetime.datetime.now() #NOTE Get current date and time
    day = current_date_time.strftime("%A")    #Day of the week
    date = current_date_time.strftime("%d")   #Day of the month
    month = current_date_time.strftime("%B")  #Month name
    year = current_date_time.strftime("%Y")   #Year
    hour = current_date_time.strftime("%H")   #Hour in 24 hour format
    minute = current_date_time.strftime("%M") #Minute
    second = current_date_time.strftime("%S") #Second
    data = f"Use this realtime information if needed, \n"
    data += f"Day: {day}\n"
    data +=f"Date: {date}\n"
    data +=f"Month: {month}\n"
    data +=f"Year: {year}\n"
    data +=f"Time: {hour} hours, {minute} minute, {second} second.\n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # load chat log
    with open(r"Data\Chatlog.json", "r") as f:
        messages = load(f) # load existing messages
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Search results to the system
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    #*ANCHOR - Generate response using Groq client
    completion = client.chat.completions.create(
            model="llama3-70b-8192", #specify the AI model (e.g ollama`s llama3-70b)
            messages=SystemChatBot + [{"role":"system", "content": Information()}] + messages,
            max_tokens=3072,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
    Answer = "" #*Initialize an empty string to store the AI`s response
# Process response chunks
    for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

#  Save updated chat log
    with open(r"Data\Chatlog.json", "w") as f:
        dump(messages, f, indent=4)

        SystemChatBot.pop()
        return AnswerModifier(Answer=Answer)
    

#*NOTE - exicute the script
if __name__ == '__main__':
    #* Use a while loop to continuously prompt the for query
    while True:
        prompt = input("Enter Your query:")
        print(RealtimeSearchEngine(prompt))