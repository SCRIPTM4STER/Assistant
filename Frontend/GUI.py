from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
AssistantNama = env_vars.get("Assistantname")
current_dir = os.getcwd()
Old_Chat_Message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicDirPath = rf"{current_dir}\Frontend\Graphics"

#STUB - Function to format the Chat response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "whats", "wheres", "hows", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['-','?','!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicStatus(Command):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicStatus():
    with open(rf"{TempDirPath}\Mic.data", "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}\Status.data", "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data", "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicBtnInitiated():
    SetMicStatus("False")

def MicBtnClosed():
    SetMicStatus("True")

def GraphicDirectoryPath(Filename):
    Path = rf"{GraphicDirPath}\{Filename}"
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def ShowText(Text):
    with open(rf"{TempDirPath}\Response.dat", 'w', encoding='utf-8') as file:
        file.write(Text)



