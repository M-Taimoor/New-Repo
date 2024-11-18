from gtts import gTTS

# Define the text and the target language
instruction_text = "Please clean the dustbin after every use."
language = 'en'  # 'en' for English, 'es' for Spanish, 'fr' for French, etc.

# Convert the text to speech
tts = gTTS(text=instruction_text, lang=language)

# Save the audio file
tts.save("instruction.mp3")

print("Audio instruction saved as 'instruction.mp3'.")
