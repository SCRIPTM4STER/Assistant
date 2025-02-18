from flask import Flask, render_template, request, jsonify
import os
from asyncio import run
from dotenv import dotenv_values

from Backend.Model import FirsLayerDMM
from Backend.Automation import Automation
from Backend.RealtimeSearchEngien import RealtimeSearchEngine
from Backend.ChatBot import ChatBot 
from Backend.Coder import generate_code

from Backend.TTS.TextToSpeech import TTS

app = Flask(__name__)

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("AssistantName")

Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
Coder_functions = ["write", "code", "create"]

def QueryModifier(Query):
    new_query = Query.strip().lower()
    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose", "whom",
        "what's", "where's", "how's", "can you"
    ]
    is_question = any(new_query.startswith(word + " ") for word in question_words)
    if new_query.endswith((".", "?", "!")):
        new_query = new_query[:-1]
    if is_question:
        new_query += "?"
    else:
        new_query += "."
    return new_query.capitalize()

def Main(Query):
    TaskExecution = False
    Decision = FirsLayerDMM(Query)
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    Mearged_query = " and ".join([
        " ".join(i.split()[1:]) for i in Decision if i == G or i == R
    ])
    for queries in Decision:
        if "generate " in queries:
            pass
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
    if G and R:
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        return Answer
    else:
        for Queries in Decision:
            if "general" in Queries:
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                return Answer
            elif "realtime" in Queries:
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                return Answer
            elif any(coder_function in Queries for coder_function in Coder_functions):
                QueryFinal = Query
                Answer = generate_code(QueryModifier(QueryFinal))
                return Answer
            elif "exit" in Queries:
                return "Okey, Bye !"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("query")
    response = Main(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
