import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from urllib.parse import quote
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials (you'll need to set these up)
# Get these from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def setup_spotify():
    """Initialize Spotify client with credentials."""
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_tracks(spotify, playlist_url):
    """Extract track information from a Spotify playlist."""
    try:
        # Extract playlist ID from URL
        playlist_id = playlist_url.split('/')[-1].split('?')[0]
        
        # Get playlist tracks
        results = spotify.playlist_tracks(playlist_id)
        tracks = results['items']
        
        # Handle pagination if there are more tracks
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])
            
        return tracks
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []

def search_youtube(query):
    """Search YouTube for a video matching the query."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                return f"https://www.youtube.com/watch?v={result['entries'][0]['id']}"
    except Exception as e:
        print(f"Error searching YouTube: {e}")
    return None

def download_audio(url, output_path='music'):
    """Download audio from YouTube URL."""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        print(f"Error downloading audio: {e}")

def main():
    # Initialize Spotify client
    spotify = setup_spotify()
    
    # Get playlist URL from user
    playlist_url = input("Enter Spotify playlist URL: ")
    if not playlist_url:
        playlist_url = "https://open.spotify.com/playlist/20qc2TEShaQKMutv8qb1gf"
    
    # Get tracks from playlist
    print("Fetching playlist tracks...")
    tracks = get_playlist_tracks(spotify, playlist_url)
    
    if not tracks:
        print("No tracks found in the playlist or error occurred.")
        return
    
    print(f"Found {len(tracks)} tracks in the playlist.")
    
    # Create music directory
    if not os.path.exists('music'):
        os.makedirs('music')
    
    # Process each track
    for i, item in enumerate(tracks, 1):
        track = item['track']
        if not track:
            continue
            
        artist = track['artists'][0]['name']
        title = track['name']
        query = f"{artist} - {title} official audio"
        
        print(f"\n[{i}/{len(tracks)}] Searching for: {query}")
        
        # Search YouTube for the track
        youtube_url = search_youtube(query)
        if youtube_url:
            print(f"Found video: {youtube_url}")
            print("Downloading...")
            download_audio(youtube_url)
        else:
            print(f"Could not find video for: {query}")
    
    print("\nDownload complete!")

if __name__ == "__main__":
    main()
