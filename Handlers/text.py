import json
from colorama import Fore, Style
import random
import logging
import os
from rank_bm25 import BM25Okapi  # pip install rank_bm25
from Handlers.DynamicResponseHandler import DynamicResponseHandler  # Import the new module

# Ensure the DB directory exists
os.makedirs('DB', exist_ok=True)

# File paths
knowledge_base_path = os.path.join('DB', 'knowledge_base.json')
learning_log_path = os.path.join('DB', 'learning_log.txt')
errors_log_path = os.path.join('DB', 'bot_errors.log')

# Load the configuration from .config.json
config_path = "alpha.config.json"

# Load the config file
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the Logging configuration
logging_config = config.get("Logging", {})
log_level_str = logging_config.get("Level", "ERROR").upper()  # Default to ERROR if not set
log_file_path = logging_config.get("FilePath", "DB/bot_errors.log")  # Default path if not set

# Map logging levels from string to actual logging constants
log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
log_level = log_levels.get(log_level_str, logging.ERROR)  # Default to ERROR if invalid level is provided

# Initialize the message containers
debug_msg = "Debug message: All systems operational."
info_msg = "Info message: Data processing complete."
warning_msg = "Warning message: Low disk space."
error_msg = "Error message: Unable to connect to database."
critical_msg = "Critical message: System failure."

# Custom handler to capture logs in variables
class LogCaptureHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        if record.levelno == logging.DEBUG:
            global debug_msg
            debug_msg += msg + "\n"
        elif record.levelno == logging.INFO:
            global info_msg
            info_msg += msg + "\n"
        elif record.levelno == logging.WARNING:
            global warning_msg
            warning_msg += msg + "\n"
        elif record.levelno == logging.ERROR:
            global error_msg
            error_msg += msg + "\n"
        elif record.levelno == logging.CRITICAL:
            global critical_msg
            critical_msg += msg + "\n"

# Configure logging
logging.basicConfig(level=log_level, filename=log_file_path, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add the custom handler to the logger
log_capture_handler = LogCaptureHandler()
log_capture_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(log_capture_handler)

# Initialize the DynamicResponseHandler
dynamic_handler = DynamicResponseHandler()

def load_data(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(Fore.YELLOW + f"File '{file_path}' not found. Starting with an empty knowledge base." + Style.RESET_ALL)
        return {"questions": []}
    except json.JSONDecodeError:
        print(Fore.RED + f"Error decoding JSON from file '{file_path}'. Starting fresh." + Style.RESET_ALL)
        return {"questions": []}

def save_data(file_path: str, data: dict):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(Fore.RED + f"Error saving data: {e}" + Style.RESET_ALL)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    tokenized_questions = [q.split() for q in questions]
    bm25 = BM25Okapi(tokenized_questions)
    user_question_tokens = user_question.split()
    scores = bm25.get_scores(user_question_tokens)
    best_match_index = scores.argmax()
    return questions[best_match_index] if scores[best_match_index] > 0 else None

def get_answer(matched_question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == matched_question.lower():
            return random.choice(q["answers"])
    return None

def log_learning(question: str, answer: str):
    try:
        with open(learning_log_path, 'a') as log_file:
            log_file.write(f"Question: {question}\nAnswer: {answer}\n\n")
    except Exception as e:
        print(Fore.RED + f"Error logging new knowledge: {e}" + Style.RESET_ALL)

def bot():
    print(Fore.GREEN + "Bot: Hello! How can I help you today?" + Style.RESET_ALL)
    knowledge_base = load_data(knowledge_base_path)
    data_modified = False

    if not knowledge_base["questions"]:
        print(Fore.YELLOW + "Bot: Starting with an empty knowledge base. Feel free to teach me!" + Style.RESET_ALL)

    try:
        while True:
            user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()

            if not user_input:
                print(Fore.RED + "Bot: Please enter a valid question." + Style.RESET_ALL)
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print(Fore.GREEN + "Bot: Goodbye!" + Style.RESET_ALL)
                break

            dynamic_response = dynamic_handler.get_context_aware_response()
            dynamic_handler.add_to_conversation_history(user_input)

            best_match = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])

            if best_match:
                answer = get_answer(best_match, knowledge_base)
                print(Fore.CYAN + f"Bot: {answer}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Bot: I'm sorry, I don't understand." + Style.RESET_ALL)
                new_answer = input(Fore.YELLOW + "Enter the answer (or type 'skip' to ignore): " + Style.RESET_ALL).strip()

                if new_answer.lower() != "skip":
                    log_learning(user_input, new_answer)
                    for q in knowledge_base["questions"]:
                        if q["question"].lower() == user_input.lower():
                            q["answers"].append(new_answer)
                            break
                    else:
                        knowledge_base["questions"].append({"question": user_input, "answers": [new_answer]})
                    data_modified = True
                    print(Fore.GREEN + "Bot: Thank you for teaching me. I've saved your response." + Style.RESET_ALL)

        if data_modified:
            save_data(knowledge_base_path, knowledge_base)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(Fore.RED + "Bot: An error occurred. Please try again later." + Style.RESET_ALL)

if __name__ == "__main__":
    bot()
