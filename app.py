from gtts import gTTS
import os

def generate_audio_instruction(text, language, filename):
    """
    Generate an audio instruction file in the specified language.
    
    :param text: Instruction text to convert into audio.
    :param language: Language code (e.g., 'en' for English, 'es' for Spanish).
    :param filename: Name of the output audio file.
    """
    try:
        # Generate audio
        tts = gTTS(text=text, lang=language)
        tts.save(filename)
        print(f"Audio instruction saved as {filename}")
    except ValueError:
        print(f"Error: Language '{language}' is not supported.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    # Instruction text
    instruction_text = "Please place the robot vacuum on a flat surface before starting."

    # User's preferred language (e.g., 'en' for English, 'fr' for French, 'es' for Spanish)
    user_language = input("Enter the language code (e.g., 'en', 'es', 'fr'): ").strip().lower()

    # Output audio filename
    output_file = f"instruction_{user_language}.mp3"

    # Generate the audio instruction
    generate_audio_instruction(instruction_text, user_language, output_file)

    # Play the audio (optional, for testing)
    if os.path.exists(output_file):
        os.system(f"start {output_file}")  # Use 'start' for Windows, 'open' for macOS, 'xdg-open' for Linux
