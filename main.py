import speech_recognition as sr
import webbrowser
import pyttsx3
import Musiclibrary
import requests

recogniser = sr.Recognizer()
engine = pyttsx3.init()
News_API_Key = "cd75505fd8d340c48b72e9f380144a76"


def processcommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open unreal engine documentation" in c.lower():
        webbrowser.open("https://dev.epicgames.com/documentation/en-us/unreal-engine")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        Link = Musiclibrary.Music[song]
        webbrowser.open(Link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=apple&from=2025-03-18&to=2025-03-18&sortBy=popularity&apiKey={News_API_Key}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Initializing Jarvis ......")
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=10,phrase_time_limit=5)
            word =  r.recognize_google(audio)
            print(word)
            if(word.lower() == "jarvis"):
                speak("Yes Boss")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    Command =  r.recognize_google(audio)
                    processcommand(Command)
        except Exception as e:
            print("Error; {0}".format(e))