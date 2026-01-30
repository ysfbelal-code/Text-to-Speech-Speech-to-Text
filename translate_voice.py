
import random
import pyttsx3
import speech_recognition as spe_rec
from googletrans import Translator  # Note: unofficial; may be unreliable

# ---------- Text-to-Speech (TTS) ----------
# Initialize engine once and reuse
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text: str, rate: int | None = None, volume: float | None = None) -> None:
    """Speak text using pyttsx3 with optional rate/volume overrides."""
    if not isinstance(text, str):
        text = str(text)

    # Save current settings
    old_rate = engine.getProperty('rate')
    old_volume = engine.getProperty('volume')

    if rate is not None:
        engine.setProperty('rate', rate)
    if volume is not None:
        engine.setProperty('volume', volume)

    engine.say(text)
    engine.runAndWait()

    # Restore original settings
    engine.setProperty('rate', old_rate)
    engine.setProperty('volume', old_volume)


# ---------- Speech Recognition ----------
def listen_and_recognize(timeout: float = 10, phrase_time_limit: float = 7, language: str = "en-GB") -> str:
    """
    Listen from the microphone and return recognized text (or "" on failure).
    language must be a valid BCP-47 code (e.g., 'en-GB', 'en-US').
    """
    recognizer = spe_rec.Recognizer()

    # Try to open microphone
    try:
        with spe_rec.Microphone() as source:
            greetings = [
                "Speak, I'll translate for you",
                "Go ahead, I'm listening",
                "Say something, I'm ready",
            ]
            speak(random.choice(greetings))

            # Ambient noise adjustment helps recognition
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except spe_rec.WaitTimeoutError:
                msg = "You did not say anything."
                print(msg)
                speak(msg)
                return ""

    except OSError as mic_err:
        # Covers cases like: No default input device available
        print(f"Microphone error: {mic_err}")
        speak("I could not access the microphone.")
        return ""

    # Recognize using Google Web Speech API (requires internet)
    try:
        print("Recognizing speech...")
        text_out = recognizer.recognize_google(audio, language=language)
        print(f"You said: {text_out}")
        return text_out
    except spe_rec.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        speak("Sorry, I could not understand the audio.")
    except spe_rec.RequestError as req_err:
        print(f"Speech recognition service error: {req_err}")
        speak("Speech recognition service error.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("An unexpected error occurred during recognition.")
    return ""


# ---------- Translation ----------
def translate_text(text: str, target_lang: str = 'es') -> str:
    """
    Translate given text to target_lang using googletrans.
    Returns translated text or "" on failure.
    """
    if not text.strip():
        return ""

    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        print(f"Translated text: {translation.text}")
        return translation.text
    except Exception as e:
        # googletrans may fail due to rate limits or site changes
        print(f"Translation error: {e}")
        speak("I could not translate your text just now.")
        return ""


# ---------- Language Selection ----------
_LANG_MENU = {
    1: ("Hindi", "hi"),
    2: ("Tamil", "ta"),
    3: ("Telugu", "te"),
    4: ("Marathi", "mr"),
    5: ("Gujarati", "gu"),
    6: ("French", "fr"),
    7: ("Malayalam", "ml"),
    8: ("Punjabi", "pa"),
    9: ("Bengali", "bn"),
    10: ("German", "de"),
    11: ("Spanish", "es"),
}

def display_language_menu(default_lang: str = "es") -> str:
    print("Available Languages:")
    for idx, (name, code) in _LANG_MENU.items():
        print(f"{idx}. {name} ({code})")
    print(f"Press Enter to use default: Spanish ({default_lang})")

    user_input = input("Enter your choice: ").strip()
    if not user_input:
        return default_lang

    try:
        ch = int(user_input)
        return _LANG_MENU.get(ch, (None, default_lang))[1]
    except ValueError:
        print("Invalid input. Using default language: Spanish (es).")
        return default_lang


# ---------- Main Loop ----------
def main():
    target_language = display_language_menu()  # defaults to 'es'
    print(f"Target language set to: {target_language}")

    while True:
        original_text = listen_and_recognize(language="en-GB")  # or 'en-US'
        if not original_text:
            continue

        if original_text.strip().lower() in {"exit", "stop", "quit"}:
            print("Goodbye!")
            speak("Goodbye!")
            break

        translated_text = translate_text(original_text, target_language)
        if translated_text:
            # Slower rate for potentially better intelligibility
            speak(translated_text, rate=130)


if __name__ == "__main__":
    main()
