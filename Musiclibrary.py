"""
Music Library for Jarvis Voice Assistant
Contains a dictionary of songs and their YouTube links
"""

# Music dictionary with song names as keys and YouTube links as values
Music = {
    "adele skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI&pp=ygUHc2t5ZmFsbA%3D%3D",
    "begging": "https://youtu.be/Qdkt3I5-FG4?si=XbUF02aY9nISEFij",
    "slaver": "https://youtu.be/yOb9Xaug35M?si=u2EGLASLzPsdEhkv",
    "run": "https://youtu.be/Fc7XWW_Ehb8?si=oCsR7l3psTCOxc-E"
}

def get_available_songs():
    """Return a list of available songs."""
    return list(Music.keys())

def add_song(name, url):
    """Add a new song to the music library."""
    Music[name.lower()] = url

def remove_song(name):
    """Remove a song from the music library."""
    if name.lower() in Music:
        del Music[name.lower()]
        return True
    return False

def search_song(query):
    """Search for songs containing the query string."""
    query = query.lower()
    return [song for song in Music.keys() if query in song]