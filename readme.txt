# Run Mix Generator with Spotify Integration

## Table of Contents
- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Complete Setup Guide](#complete-setup-guide)
  - [1. Install Python](#1-install-python)
  - [2. Install FFmpeg](#2-install-ffmpeg)
  - [3. Download the Application](#3-download-the-application)
  - [4. Set Up Virtual Environment](#4-set-up-virtual-environment)
  - [5. Install Dependencies](#5-install-dependencies)
  - [6. Set Up Spotify Developer Account](#6-set-up-spotify-developer-account)
  - [7. Configure Environment Variables](#7-configure-environment-variables)
- [Usage Guide](#usage-guide)
  - [Downloading Music from Spotify](#downloading-music-from-spotify)
  - [Creating Run Mixes](#creating-run-mixes)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [Important Notes](#important-notes)
- [License](#license)

## Overview

This application provides two main functionalities:
1. **Spotify Playlist Downloader**: Download songs from Spotify playlists by searching and downloading them from YouTube
2. **Run Mix Generator**: Create custom running mixes by combining music tracks with interval instructions

## System Requirements
- Windows/macOS/Linux
- Python 3.8 or higher
- At least 500MB free disk space
- Internet connection
- Spotify account (for playlist access)
- Spotify Developer account (for API access)

## Complete Setup Guide

### 1. Install Python
1. Visit [Python's official website](https://www.python.org/downloads/)
2. Download the latest Python 3.x version for your operating system
3. Run the installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Verify installation by opening Command Prompt (Windows) or Terminal (macOS/Linux) and typing:
   ```
   python --version
   ```
   You should see the installed Python version number.

### 2. Install FFmpeg
FFmpeg is required for audio processing.

#### Windows:
1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the downloaded zip file
3. Add FFmpeg to your system PATH:
   - Open Windows Settings > System > About > Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit"
   - Click "New" and add the path to the `bin` folder inside the extracted FFmpeg folder
   - Click "OK" to save all dialogs

#### macOS (using Homebrew):
```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Download the Application

#### Option A: Using Git (recommended)
1. Install Git from [git-scm.com](https://git-scm.com/downloads)
2. Open Command Prompt/Terminal and run:
   ```bash
   git clone https://github.com/emmanuelshalu/startrunning.git
   cd startrunning
   ```

#### Option B: Download ZIP
1. Visit the GitHub repository: [https://github.com/emmanuelshalu/startrunning](https://github.com/emmanuelshalu/startrunning)
2. Click "Code" > "Download ZIP"
3. Extract the ZIP file to your preferred location
4. Open Command Prompt/Terminal and navigate to the extracted folder:
   ```bash
   cd path/to/startrunning
   ```

### 4. Set Up Virtual Environment
1. Create a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows (Command Prompt):**
     ```
     .\venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   You should see `(venv)` at the beginning of your command prompt when activated.

### 5. Install Dependencies
1. With the virtual environment activated, run:
   ```bash
   pip install -r requirements.txt
   ```

### 6. Set Up Spotify Developer Account
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the form:
   - App name: "RunMix Generator" (or your preferred name)
   - App description: "Application for creating running mixes from Spotify playlists"
   - Click "Create"
5. On the app page, click "Settings"
6. Under "Redirect URIs", add:
   ```
   http://127.0.0.1:8888/callback
   ```
7. Click "Save"
8. Note down your "Client ID" and click "Show Client Secret" to reveal and note down your "Client Secret"

### 7. Configure Environment Variables
1. In the project folder, create a new file named `.env`
2. Open the file in a text editor and add:
   ```
   SPOTIFY_CLIENT_ID='your_client_id_here'
   SPOTIFY_CLIENT_SECRET='your_client_secret_here'
   ```
3. Replace `your_client_id_here` and `your_client_secret_here` with the values from your Spotify Developer Dashboard
4. Save the file

## Usage Guide

### Downloading Music from Spotify
1. Ensure you've completed the setup steps above
2. Activate your virtual environment if not already active
3. Run the Spotify downloader:
   ```bash
   python spotify_downloader.py
   ```
4. When prompted, enter the URL of the Spotify playlist you want to download
5. The application will:
   - Authenticate with Spotify
   - Search for each song on YouTube
   - Download and convert them to MP3
   - Save them to the `music` folder

### Creating Run Mixes
1. Place your music files in the `music` folder (or use the Spotify downloader to get some)
2. Place instruction audio files (e.g., w1.mp3, r1.mp3, d1.mp3) in the `instructions` folder
3. Run the application:
   ```bash
   python runmix.py
   ```
4. When prompted, enter the day number (1, 2, 3, etc.)
5. The application will:
   - Combine music and instruction files according to the workout sequence
   - Save the generated mix in the current directory
   - Rename used music files to indicate they've been used

## Troubleshooting

### Common Issues
1. **Python not found**
   - Ensure Python is added to your system PATH during installation
   - Try using `python3` instead of `python` on some systems

2. **Module not found errors**
   - Make sure you've activated the virtual environment
   - Run `pip install -r requirements.txt` again

3. **FFmpeg not found**
   - Verify FFmpeg is installed and added to your system PATH
   - Restart your terminal/command prompt after installation

4. **Spotify authentication issues**
   - Double-check your Client ID and Secret in the `.env` file
   - Ensure the Redirect URI in your Spotify Developer Dashboard matches exactly

## File Structure
```
startrunmixer/
├── music/           # Store your music files here
│   └── (music files will be saved here by spotify_downloader.py)
├── instructions/    # Store instruction audio files
│   ├── w1.mp3       # Walking instruction 1
│   ├── r1.mp3       # Running instruction 1
│   └── d1.mp3       # Drill instruction 1
├── output/          # Generated run mixes are saved here
├── .env             # Store Spotify API credentials (create this file)
├── .gitignore       # Git ignore file
├── requirements.txt # Python dependencies
├── runmix.py        # Run mix generator
└── spotify_downloader.py # Spotify playlist downloader
```

## Important Notes
- The Spotify downloader uses YouTube as the source for downloads
- Downloading copyrighted material may violate terms of service
- Some tracks might not be found if the search query doesn't match any results
- Make sure to have enough free disk space for the downloaded music
- For best results, use high-quality audio files
- The application creates a backup of your music files before processing

## License
This project is for educational and personal use only. Please respect copyright laws and terms of service of Spotify and YouTube. Use at your own risk.