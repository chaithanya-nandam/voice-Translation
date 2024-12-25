import speech_recognition as spr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Creating Recogniser() class object
recog1 = spr.Recognizer()
mc = spr.Microphone()

# Function to capture voice and recognize text
def recognize_speech(recog, source, language):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)
        audio = recog.listen(source)
        recognized_text = recog.recognize_google(audio, language=language)  # Recognizing in specified language
        return recognized_text
    except spr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return None
    except spr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Mapping user input to language codes
language_map = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Portuguese': 'pt',
    'Bengali': 'bn',
    'Malayalam': 'ml',
    'Tamil': 'ta',
    'Kannada': 'kn'
}

# Display available languages
print("Available languages:")
for lang in language_map.keys():
    print(f"- {lang}")

# Input for source language
source_language_input = input("Enter the source language: ").strip()
if source_language_input not in language_map:
    print(f"Invalid source language: {source_language_input}. Exiting.")
    exit()

# Input for target language
target_language_input = input("Enter the target language: ").strip()
if target_language_input not in language_map:
    print(f"Invalid target language: {target_language_input}. Exiting.")
    exit()

source_language_code = language_map[source_language_input]
target_language_code = language_map[target_language_input]

# Ensure the outputs folder exists
if not os.path.exists('outputs'):
    os.makedirs('outputs')  # Create the folder if it doesn't exist

# Capture voice and directly translate
with mc as source:
    print(f"Speak now in {source_language_input} for translation to {target_language_input}...")
    MyText = recognize_speech(recog1, source, source_language_code)

# If the recognized text is valid, proceed with translation
if MyText:
    print(f"Recognized Text: {MyText}")

    try:
        # Translate the recognized sentence into the target language
        translated_text = GoogleTranslator(source=source_language_code, target=target_language_code).translate(MyText)

        if translated_text is None:
            print("Translation failed; received None.")
        else:
            print(f"Translated Text in {target_language_input}: {translated_text}")

            # Generate audio for the translated text
            speak = gTTS(text=translated_text, lang=target_language_code, slow=False)
            audio_file = f"outputs/captured_voice_{target_language_input}.mp3"
            speak.save(audio_file)
            os.system(f"start {audio_file}")  # For Windows; use 'open' for macOS and 'xdg-open' for Linux
    except Exception as e:
        print(f"An error occurred during translation: {e}")
else:
    print("No speech input detected. Exiting.")