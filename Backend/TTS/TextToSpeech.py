import pygame
import random  # Import random for generating random choices
import asyncio  # Import asyncio for asynchronous operations
import edge_tts  # Import edge_tts for text-to-speech functionality
import os  # Import os for file path handling
from dotenv import dotenv_values  # Import dotenv for reading environment variables
import time  # For adding pauses in TTS

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
Assistantvoice = env_vars.get("Assistantvoice")


async def TextToAudioFile(text) -> None:
    """Converts text to an audio file using edge_tts with pauses."""
    file_path = r"Data/speech.mp3"

    # Remove the existing file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate speech audio with edge_tts
    communicate = edge_tts.Communicate(text, Assistantvoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)


def preprocess_text(text):
    """
    Removes all punctuation except ., ?, and , from the input text.
    Adds pauses based on punctuation marks (without SSML tags).
    """
    allowed_punctuation = {'.', '?', ','}
    modified_text = ''

    # Add pauses based on punctuation marks
    for char in text:
        if char in allowed_punctuation:
            modified_text += char + '  '  # Just adding a space for pause
        else:
            modified_text += char

    return modified_text


def TTS(Text, func=lambda r=None: True):
    """Plays the generated audio file using pygame."""
    while True:
        try:
            # Preprocess the text to add pauses and remove unwanted punctuation
            cleaned_text = preprocess_text(Text)

            # Generate the audio file
            asyncio.run(TextToAudioFile(cleaned_text))

            # Initialize pygame mixer
            pygame.mixer.init()

            # Load and play the audio file
            pygame.mixer.music.load(r"Data/speech.mp3")
            pygame.mixer.music.play()

            # Wait for the audio to finish or a stop condition
            while pygame.mixer.music.get_busy():
                if func() is False:
                    break
                pygame.time.Clock().tick(10)

            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")


def TextToSpeech(Text, func=lambda r=None: True):
    """Converts text to speech and handles long texts by splitting them."""
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out, sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out, sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer.",
    ]

    # Handle long texts by splitting and adding a response
    if len(Data) > 6 and len(Text) >= 400:
        TTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)


if __name__ == "__main__":
    # Prompt the user for text input
    TextToSpeech(input("Enter text: "))
