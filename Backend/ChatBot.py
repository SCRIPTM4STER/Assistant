#SECTION - Importing the necessary libraries
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

#* Initialize an empty list to store chat messages
messages = []

#*NOTE - Define a system message that provides context to the AI chatbot about its role and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

#STUB - Attempt to load the chat log from a JSON file
try:
    with open(r"Data\Chatlog.json", "r") as f:
        messages = load(f) # load existing messages
except FileNotFoundError:
    #NOTE if file doesn`t exist create a new JSON file to store Data
    with open(r"Data\Chatlog.json", "w") as f:
        dump([], f)
  

#STUB - function to get realtime date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now() #NOTE Get current date and time
    day = current_date_time.strftime("%A")    #Day of the week
    date = current_date_time.strftime("%d")   #Day of the month
    month = current_date_time.strftime("%B")  #Month name
    year = current_date_time.strftime("%Y")   #Year
    hour = current_date_time.strftime("%H")   #Hour in 24 hour format
    minute = current_date_time.strftime("%M") #Minute
    second = current_date_time.strftime("%S") #Second

    # Format info into str
    data = f"Please use this realtime information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours |{minute} minutes |{second} seconds\n"
    return data


#STUB - Function to format the Chat response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Main Function to handel querys
def ChatBot(Query):
    try:
        # load chat log
        with open(r"Data\Chatlog.json", "r") as f:
            messages = load(f) # load existing messages
        
        # append the user querys to the messages list 
        messages.append({"role": "user", "content": f"{Query}"})

        # Post request to Groq API to fetch answer
        completion = client.chat.completions.create(
            model="llama3-70b-8192", #specify the AI model (e.g ollama`s llama3-70b)
            messages=SystemChatBot + [{"role":"system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
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

        Answer = Answer.replace("</s>", "") #Clean up unwanted tokens

        # Append the cahtbot`s response 
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\Chatlog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)
    


#*NOTE - exicute the script
if __name__ == '__main__':
    #* Use a while loop to continuously prompt the for query
    while True:
        user_input = input("Enter Your Question:")
        if user_input == "bye".lower():
            break
        print(ChatBot(user_input))

