import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize recognizer and TTS
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "pub_a410f3ef5f5f44c7b949569beabad24e"

def speak(text):
    """Convert text to speech using gTTS + pygame"""
    try:
        tts = gTTS(text)
        tts.save("temp.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print("TTS error:", e)

def aiProcess(command):
    """Send user command to Gemini AI"""
    try:
        response = model.generate_content(
            f"You are Jarvis, a helpful virtual assistant. Keep answers short. User asked: {command}"
        )
        return response.text
    except Exception as e:
        return f"AI processing failed: {e}"

def processCommand(c):
    """Process user commands"""
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        try:
            song = c.split(" ")[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Sorry, I couldn't find that song.")
        except Exception:
            speak("Please specify a song name after 'play'.")
    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                for article in articles[:5]:
                    speak(article["title"])
            else:
                speak("Unable to fetch news.")
        except Exception as e:
            speak(f"Error fetching news: {e}")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.WaitTimeoutError:
            print("Listening timed out...")
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except Exception as e:
            print(f"Error: {e}")
