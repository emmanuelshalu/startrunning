# RunMix Generator

A powerful application for creating custom running mixes with interval training instructions and your favorite music. Available both as a command-line interface (CLI) and a user-friendly web application.

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [1. Install Python](#1-install-python)
  - [2. Install FFmpeg](#2-install-ffmpeg)
  - [3. Download the Application](#3-download-the-application)
  - [4. Set Up Virtual Environment](#4-set-up-virtual-environment)
  - [5. Install Dependencies](#5-install-dependencies)
  - [6. Set Up Spotify Developer Account](#6-set-up-spotify-developer-account-optional)
  - [7. Configure Environment Variables](#7-configure-environment-variables)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Features

### Web Interface
- **User-friendly Interface**: Intuitive web-based interface for generating running mixes
- **Music Management**: Upload your own music files or import from Spotify
- **Custom Workouts**: 12 pre-defined workout sequences with different interval patterns
- **Progress Tracking**: Real-time progress updates during mix generation
- **Responsive Design**: Works on desktop and mobile devices

### Command Line Interface
- **Spotify Integration**: Download songs from Spotify playlists
- **Flexible Audio Processing**: Combine music with interval instructions
- **Batch Processing**: Generate multiple running mixes in sequence
- **File Management**: Automatic organization of used/unused music files

## System Requirements
- Windows/macOS/Linux
- Python 3.8 or higher
- FFmpeg (for audio processing)
- At least 500MB free disk space
- Internet connection
- Spotify account (for playlist access, optional)
- Spotify Developer account (for API access, optional)

## Installation

### 1. Install Python
1. Visit [Python's official website](https://www.python.org/downloads/)
2. Download the latest Python 3.x version for your operating system
3. Run the installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Verify installation by opening Command Prompt (Windows) or Terminal (macOS/Linux) and typing:
   ```bash
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
```bash
git clone https://github.com/emmanuelshalu/startrunning.git
cd startrunning
```

#### Option B: Download ZIP
1. Visit the GitHub repository: [https://github.com/emmanuelshalu/startrunning](https://github.com/emmanuelshalu/startrunning)
2. Click "Code" > "Download ZIP"
3. Extract the ZIP file to your preferred location
4. Open Command Prompt/Terminal and navigate to the extracted folder

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
With the virtual environment activated, run:
```bash
pip install -r requirements.txt
```

### 6. Set Up Spotify Developer Account (Optional)
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
   http://127.0.0.1:5000/callback
   ```
7. Click "Save"
8. Note down your "Client ID" and click "Show Client Secret" to reveal and note down your "Client Secret"

### 7. Configure Environment Variables
1. In the project folder, create a new file named `.env`
2. Open the file in a text editor and add:
   ```
   # Required for Spotify integration
   SPOTIFY_CLIENT_ID='your_client_id_here'
   SPOTIFY_CLIENT_SECRET='your_client_secret_here'
   
   # Optional: Flask secret key (will be auto-generated if not set)
   # FLASK_SECRET_KEY='your_secret_key_here'
   ```
3. Replace `your_client_id_here` and `your_client_secret_here` with the values from your Spotify Developer Dashboard
4. Save the file

## Usage

### Web Interface
1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your web browser**
   ```
   http://localhost:5000
   ```

3. **Add Music**
   - Click "Upload" to add your own music files
   - Or import a Spotify playlist by pasting its URL

4. **Generate a RunMix**
   - Select a day (1-12) from the dropdown
   - Click "Generate RunMix"
   - Wait for the generation to complete
   - Download your custom run mix

### Command Line Interface (CLI)

#### Downloading Music from Spotify
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

#### Creating Run Mixes (CLI)
1. Place your music files in the `music` folder (or use the Spotify downloader to get some)
2. Place instruction audio files (e.g., w1.mp3, r1.mp3, d1.mp3) in the `instructions` folder
3. Run the application:
   ```bash
   python runmix.py
   ```
4. When prompted, enter the day number (1-12)
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
runmix-generator/
├── static/               # Static files (CSS, JS, images)
│   └── js/
│       └── main.js       # Main JavaScript file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── index.html        # Main page
├── uploads/              # User-uploaded files (created automatically)
├── music/                # Music files (created automatically)
├── instructions/         # Audio instruction files (pre-loaded)
├── output/               # Generated run mixes (created automatically)
├── .env                  # Environment variables
├── app.py                # Main Flask application
├── runmix.py             # Core run mix generation logic (CLI)
├── spotify_downloader.py # Spotify integration
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Spotify Integration (Optional)

To enable Spotify playlist importing in both web and CLI interfaces:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Copy your Client ID and Client Secret to the `.env` file
4. Add the following Redirect URIs in your Spotify app settings:
   - `http://localhost:5000/callback` (for web interface)
   - `http://127.0.0.1:8888/callback` (for CLI interface)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [pydub](https://github.com/jiaaro/pydub) - Audio processing
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - For music integration
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube video/audio downloader
