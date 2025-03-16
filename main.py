import speech_recognition as sr
import webbrowser
import pyttsx3

recogniser = sr.Recognizer()
engine = pyttsx3.init()

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
                speak("Ya")
        except Exception as e:
            print("Error; {0}".format(e))