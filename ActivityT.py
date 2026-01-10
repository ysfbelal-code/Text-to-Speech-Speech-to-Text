import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import asyncio

def speak(text, language="en"):
  engine = pyttsx3.init()
  engine.setProperty('rate', 150)
  voices = engine.getProperty('voices')
  voice = int(input('Choose a voice: 0 - Man, 1 - Woman: '))
  if voice != 0 and voice != 1:
    print('Invalid input! Setting voice to default.')
    engine.setProperty('voice', voices[0].id)
  else:
    engine.setProperty('voice', voices[voice].id)
  engine.say(text)
  engine.runAndWait()

def speech_to_text():
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    print("Please speak now in English")
    audio = recognizer.listen(source)
  try:
    print("Recognising speech...")
    text = recognizer.recognize_google(audio, language='en-US')
    print(f"You said: {text}")
    return text
  except Exception as e:
    print(f'Error: {e}')
  return ''

async def translate_text(text, dest_language):
  translator = Translator()
  translation = await translator.translate(text, dest=dest_language)
  print(translation)
  return translation.text

def display_language_options():
    print("Choose a language to translate to:")
    print("1. Spanish (sp)")
    print("2. French (fr)")
    print("3. German (ge)")
    print("4. Italian (it)")
    print("5. Dutch (du)")
    choice = int(input("Please select the target language number (1-5): "))
    if not choice or choice > 5 or choice < 1:
      print('Invalid input! Defaulting choice to Spanish.')
    language_dict = {
        "1": "sp",
        "2": "fr",
        "3": "ge",
        "4": "it",
        "5": "du"

    }
    return language_dict.get(choice, "es")

async def main():
  target_lang = display_language_options()
  original_txt = speech_to_text()
  if original_txt:
    translated_txt = await translate_text(original_txt, target_lang)
    speak(translated_txt, language='en')
    print(f'Translated text: {translated_txt}')

if __name__ == "__main__":
  asyncio.run(main())
  
  
