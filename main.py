import speech_recognition as sr
import webbrowser
import pyttsx3
import Musiclibrary
import requests
import logging
from datetime import datetime
import time
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize speech recognition and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure TTS engine using config settings
engine.setProperty('rate', config.TTS_RATE)
engine.setProperty('volume', config.TTS_VOLUME)


def speak(text):
    """Convert text to speech with error handling."""
    try:
        logger.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        print(f"Error speaking: {text}")


def get_news():
    """Fetch and return latest news articles."""
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        url = f"https://newsapi.org/v2/everything?q={config.NEWS_QUERY}&from={current_date}&to={current_date}&sortBy=popularity&apiKey={config.NEWS_API_KEY}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('articles', [])
        
        if not articles:
            speak("Sorry, no news articles found for today.")
            return
            
        speak(f"Here are the top {min(config.MAX_NEWS_ARTICLES, len(articles))} news headlines:")
        for i, article in enumerate(articles[:config.MAX_NEWS_ARTICLES]):
            title = article.get('title', 'No title available')
            speak(f"News {i + 1}: {title}")
            time.sleep(1)  # Brief pause between articles
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news right now. Please check your internet connection.")
    except Exception as e:
        logger.error(f"Unexpected error in get_news: {e}")
        speak("Sorry, there was an error getting the news.")


def play_music(song_name):
    """Play music from the music library."""
    try:
        if song_name in Musiclibrary.Music:
            link = Musiclibrary.Music[song_name]
            logger.info(f"Playing song: {song_name}")
            speak(f"Playing {song_name}")
            webbrowser.open(link)
        else:
            available_songs = list(Musiclibrary.Music.keys())
            speak(f"Sorry, I don't have {song_name} in my library. Available songs are: {', '.join(available_songs)}")
    except Exception as e:
        logger.error(f"Error playing music: {e}")
        speak("Sorry, I couldn't play the music.")


def open_website(site_name, url):
    """Open a website with logging and feedback."""
    try:
        logger.info(f"Opening {site_name}")
        speak(f"Opening {site_name}")
        webbrowser.open(url)
    except Exception as e:
        logger.error(f"Error opening {site_name}: {e}")
        speak(f"Sorry, I couldn't open {site_name}")


def process_command(command):
    """Process voice commands with improved structure and error handling."""
    command = command.lower().strip()
    logger.info(f"Processing command: {command}")
    
    try:
        if "open youtube" in command:
            open_website("YouTube", "https://www.youtube.com/")
        elif "open google" in command:
            open_website("Google", "https://www.google.com/")
        elif "open facebook" in command:
            open_website("Facebook", "https://www.facebook.com/")
        elif "open unreal engine documentation" in command:
            open_website("Unreal Engine Documentation", "https://dev.epicgames.com/documentation/en-us/unreal-engine")
        elif command.startswith("play") and len(command.split()) > 1:
            # Extract song name from command
            song_parts = command.split(" ", 1)
            if len(song_parts) > 1:
                song_name = song_parts[1]
                play_music(song_name)
            else:
                speak("Please specify which song you want to play.")
        elif "news" in command:
            get_news()
        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "date" in command:
            current_date = datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")
        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day!")
            return False
        else:
            speak("Sorry, I didn't understand that command. Try saying 'open YouTube', 'play music', 'news', 'time', or 'date'.")
    except Exception as e:
        logger.error(f"Error processing command '{command}': {e}")
        speak("Sorry, there was an error processing your command.")
    
    return True


def listen_for_command():
    """Listen for voice commands with improved error handling."""
    try:
        with sr.Microphone() as source:
            print("Jarvis Active... Speak your command:")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=config.TIMEOUT, phrase_time_limit=config.PHRASE_TIME_LIMIT)
        
        command = recognizer.recognize_google(audio)
        print(f"Command recognized: {command}")
        return command
    except sr.WaitTimeoutError:
        speak("I didn't hear anything. Try again.")
        return None
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Please try again.")
        return None
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        speak("Sorry, there's an issue with the speech recognition service.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in listen_for_command: {e}")
        speak("Sorry, there was an error listening for your command.")
        return None


def listen_for_wake_word():
    """Listen for the wake word 'Jarvis'."""
    try:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=config.TIMEOUT, phrase_time_limit=config.PHRASE_TIME_LIMIT)
        
        word = recognizer.recognize_google(audio)
        print(f"Heard: {word}")
        return word.lower() == config.WAKE_WORD
    except sr.WaitTimeoutError:
        return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in listen_for_wake_word: {e}")
        return False

def main():
    """Main function to run the Jarvis voice assistant."""
    speak("Initializing Jarvis...")
    speak("Hello! I'm Jarvis, your voice assistant. Say 'Jarvis' to wake me up.")
    
    consecutive_errors = 0
    
    while True:
        try:
            if listen_for_wake_word():
                speak("Yes Boss! How can I help you?")
                consecutive_errors = 0  # Reset error counter on successful wake word detection
                
                command = listen_for_command()
                if command:
                    # Process the command and check if we should continue
                    should_continue = process_command(command)
                    if not should_continue:
                        break
            else:
                consecutive_errors += 1
                if consecutive_errors >= config.MAX_CONSECUTIVE_ERRORS:
                    print(f"Too many consecutive errors ({consecutive_errors}). Taking a short break...")
                    time.sleep(config.ERROR_SLEEP_TIME)
                    consecutive_errors = 0
                    
        except KeyboardInterrupt:
            print("\nShutting down Jarvis...")
            speak("Goodbye! Shutting down now.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            consecutive_errors += 1
            if consecutive_errors >= config.MAX_CONSECUTIVE_ERRORS:
                speak("I'm experiencing some technical difficulties. Restarting...")
                time.sleep(config.ERROR_SLEEP_TIME)
                consecutive_errors = 0


if __name__ == "__main__":
    main()