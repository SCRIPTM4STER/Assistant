import random
from textblob import TextBlob
from datetime import datetime

class DynamicResponseHandler:
    
    def __init__(self):
        self.conversation_history = []  # Tracks the conversation context
        self.last_interaction_time = None  # Time of the last interaction
    
    def get_sentiment_based_response(self, user_input: str) -> str:
        sentiment = TextBlob(user_input).sentiment.polarity
        if sentiment > 0.1:
            return "I'm glad you're feeling positive!"
        elif sentiment < -0.1:
            return "I'm sorry you're upset. How can I help?"
        else:
            return "Got it. How can I assist you further?"
    
    def get_random_response(self, response_type: str) -> str:
        responses = {
            'error': [
                "Oops, I missed that.",
                "Sorry, I didn't catch that.",
                "Could you repeat that, please?"
            ],
            'greeting': [
                "Hi there! How can I assist you today?",
                "Hello! What can I do for you today?",
                "Hey! Need help with something?"
            ],
            'thanks': [
                "You're welcome!",
                "Glad I could help!",
                "Anytime!"
            ]
        }
        
        return random.choice(responses.get(response_type, ["Sorry, I don't understand."]))
    
    def get_context_aware_response(self) -> str:
        if not self.conversation_history:
            return self.get_random_response('greeting')
        
        last_interaction = self.conversation_history[-1]
        if 'movie' in last_interaction.lower():
            return "Would you like to know about any movies today?"
        elif 'weather' in last_interaction.lower():
            return "How's the weather on your side?"
        else:
            return "What else can I help you with?"
    
    def add_to_conversation_history(self, user_input: str):
        """ Adds the user's input to the conversation history for context-aware responses. """
        self.conversation_history.append(user_input)
    
    def time_based_response(self) -> str:
        """ Greets based on the time of day. """
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "Good morning!"
        elif 12 <= current_hour < 18:
            return "Good afternoon!"
        else:
            return "Good evening!"
    
