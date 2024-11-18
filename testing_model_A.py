from gtts import gTTS
import threading
from queue import Queue
from langdetect import detect

def generate_audio_instruction(text, language_code, file_name):
    """
    Generate an audio file with the given text and language code.

    :param text: The text to be converted to speech.
    :param language_code: The language code (e.g., 'en' for English, 'es' for Spanish).
    :param file_name: The name of the output audio file.
    """
    try:
        # Convert the text to speech
        tts = gTTS(text=text, lang=language_code)
        
        # Save the audio file
        tts.save(file_name)
        
        print(f"Audio instruction saved as '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_text_to_speech(queue):
    """
    Process text-to-speech conversions from a queue using multi-threading.

    :param queue: A queue containing tuples of (text, language_code, file_name).
    """
    while not queue.empty():
        text, language_code, file_name = queue.get()
        generate_audio_instruction(text, language_code, file_name)
        queue.task_done()

# Read text from a file
file_path = input("Enter the path to the text file: ")
with open(file_path, 'r') as file:
    text_to_convert = file.read()

# Detect the language of the input text
detected_language = detect(text_to_convert)
print(f"Detected language: {detected_language}")

# Define the language code and file name
language_code = detected_language if detected_language in ['en', 'es', 'fr'] else 'en'
file_name = f"instruction_{language_code}.mp3"

# Create a queue and add the text-to-speech task
task_queue = Queue()
task_queue.put((text_to_convert, language_code, file_name))

# Create and start a thread to process the queue
thread = threading.Thread(target=process_text_to_speech, args=(task_queue,))
thread.start()

# Wait for the thread to finish
thread.join()

print(f"Audio instruction saved as '{file_name}'.")