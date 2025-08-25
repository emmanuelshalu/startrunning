

# Run Mix Generator with Spotify Integration

This project provides two main functionalities:
1. **Spotify Playlist Downloader**: Download songs from Spotify playlists by searching and downloading them from YouTube
2. **Run Mix Generator**: Create custom running mixes by combining music tracks with interval instructions

## Features

### Spotify Playlist Downloader
- Download all songs from any public Spotify playlist
- Automatic YouTube search and download
- Save songs as MP3 files
- Secure credential management using environment variables

### Run Mix Generator
- Create custom running workouts with music and voice instructions
- Support for different workout types (walking, running, drills)
- Automatic music file management
- Customizable interval timing

## Prerequisites
- Python 3.6+
- FFmpeg (for audio conversion)
- Spotify Developer Account (for playlist downloader)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd startrunmixer
   ```

2. Install the required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

3. For Spotify Playlist Downloader, set up your credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Add `http://127.0.0.1:8888/callback` as a Redirect URI
   - Create a `.env` file with your credentials:
     ```
     SPOTIFY_CLIENT_ID='your_client_id_here'
     SPOTIFY_CLIENT_SECRET='your_client_secret_here'
     ```

## Usage

### 1. Download Music from Spotify Playlist
```bash
python3 spotify_downloader.py
```
- When prompted, enter the Spotify playlist URL
- Downloaded songs will be saved in the `music/` directory

### 2. Create a Run Mix
```bash
python3 runmix.py
```
- Place your music files in the `music/` folder
- Place instruction audio files (e.g., w1.mp3, r1.mp3, d1.mp3) in the `instructions/` folder
- When prompted, enter the day number (1, 2, 3, etc.)
- The generated run mix will be saved in the current directory
- Used music files will be renamed to indicate they've been used

## File Structure
```
startrunmixer/
├── music/           # Store your music files here
├── instructions/    # Store instruction audio files
├── output/          # Generated run mixes are saved here
├── .env             # Store Spotify API credentials
├── requirements.txt # Python dependencies
├── runmix.py        # Run mix generator
└── spotify_downloader.py # Spotify playlist downloader
```

## Notes
- The Spotify downloader uses YouTube as the source for downloads
- Downloading copyrighted material may violate terms of service
- Some tracks might not be found if the search query doesn't match any results
- Make sure to have enough free disk space for the downloaded music

## License
This project is for educational purposes only. Use at your own risk.

// Instructions for using this app:

// 1. Place your music .mp3 files in the "music" folder.
// 2. Place your instruction .mp3 files (e.g., w1.mp3, r1.mp3, d1.mp3, etc.) in the "instructions" folder.
// 3. Run the script (runmix.py).
// 4. When prompted, enter the day number (1, 2, 3.....)
// 5. The app will generate a run mix and save it as an .mp3 file in the current directory.
// 6. Used music files will be mentioned in their names once output is generated