"""
Configuration file for Jarvis Voice Assistant
Contains API keys and other configuration settings
"""

# API Keys (Consider using environment variables for production)
NEWS_API_KEY = "cd75505fd8d340c48b72e9f380144a76"

# Voice Assistant Settings
WAKE_WORD = "jarvis"
TIMEOUT = 10
PHRASE_TIME_LIMIT = 5

# TTS Engine Settings
TTS_RATE = 150  # Speed of speech
TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)

# News Settings
MAX_NEWS_ARTICLES = 3
NEWS_QUERY = "technology"

# Error Handling
MAX_CONSECUTIVE_ERRORS = 5
ERROR_SLEEP_TIME = 2
