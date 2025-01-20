#SECTION - Importing the necessary libraries
import os
from asyncio import run
from dotenv import dotenv_values

from Backend.Model import FirsLayerDMM
from Backend.Automation import Automation
from Backend.RealtimeSearchEngien import RealtimeSearchEngine
from Frontend.GUI import QueryModifier
from Backend import TextToSpeech
from Backend.ChatBot import ChatBot 
from Backend.Coder import generate_code
from Backend.ENGINE.natural_voice import speak, initiate_proxies

#ANCHOR - load env variables from .env file
env_vars = dotenv_values(".env")

#*NOTE - Retrive the enviroment variables for Username, assistant name and API key *# 
Username = env_vars.get("Username")
Assistantname = env_vars.get("AssistantName")

Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
Coder_functions = ["write", "code", "create"]


def Main(Query):
    TaskExecution = False
    Decision = FirsLayerDMM(Query)

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i == G or i == R]
    )

    for queries in Decision:
        if "generate " in queries:
            pass
    
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    if G and R or R:
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        print(f'AGI: {Answer}')
        TextToSpeech.TTS(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                print(f'AGI: {Answer}')
                TextToSpeech.TTS(Answer)
                return True
            
            elif "realtime" in Queries:
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                print(f'AGI: {Answer}')
                TextToSpeech.TTS(Answer)
                return True
            elif any(coder_function in Queries for coder_function in Coder_functions):
                QueryFinal = Query
                Answer = generate_code(QueryModifier(QueryFinal))
            
            elif "exit" in Queries:
                QueryFinal = "Okey, Bye !"
                Answer = ChatBot(QueryModifier(QueryFinal))
                TextToSpeech.TTS(Answer)
                os.exit(2)


if __name__ == "__main__":
    while True:
        User_Input = input(f"{Username}>>>")
        Main(Query=User_Input)