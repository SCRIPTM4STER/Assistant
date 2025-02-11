import os
from playsound import playsound

def neural_speak(text: str, voice: str = 'en-CA-ClaraNeural', subtitle_file: str = 'Subtitles_File.srt') -> None:
    """
    Function to convert text to speech using Edge TTS.

    Args:
        text (str): The text to be spoken.
        voice (str): The voice to use for speech synthesis. Defaults to "en-US-JennyNeural".
        subtitle_file (str): The path to the subtitle file. Defaults to "Subtitles_File.srt".

    Notes:
        This function utilizes the Edge TTS command line tool to convert text to speech.
        Users can choose from a variety of available voices for different accents and tones.
        Uncomment the corresponding line in the function to select the preferred voice.

    Available voices:
        - en-US-JennyNeural: Clear and professional-sounding American female voice
        - en-SG-LunaNeural: Friendly and approachable Singaporean female voice
        - en-AU-NatashaNeural: Warm and friendly Australian female voice
        - en-CA-ClaraNeural: Crisp and articulate Canadian female voice
        - en-CA-LiamNeural: Confident and professional Canadian male voice (currently selected)
    """

    # Define the absolute path for the output MP3 file
    mp3_file = "Data/speech.mp3"

    # Build the edge-tts command string, including voice, text, and output media
    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{mp3_file}" --write-subtitles {subtitle_file}'

    # Execute the edge-tts command using the system shell
    os.system(command)

    # Play the generated speech file
    playsound(mp3_file)

    # Remove the subtitle and MP3 files after playing
    os.remove(subtitle_file)
    os.remove(mp3_file)

if __name__ == "__main__": 
    neural_speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.")
