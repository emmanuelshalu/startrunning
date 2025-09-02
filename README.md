# 🏃‍♂️ RunMix Generator

A high-performance application for creating custom running mixes with precise interval training instructions and your favorite music. Optimized for reliability and production use.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   # Install Python 3.8+ and FFmpeg
   # On macOS:
   brew install python ffmpeg
   
   # On Ubuntu/Debian:
   sudo apt update && sudo apt install python3 python3-pip ffmpeg
   
   # On Windows (using Chocolatey):
   choco install python ffmpeg
   ```

2. **Set Up Project**:
   ```bash
   # Clone the repository
   git clone https://github.com/emmanuelshalu/startrunning.git
   cd startrunning
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Add Your Music**:
   - Place your MP3 files in the `music/` folder
   - Ensure instruction files are in `instructions/` folder

4. **Run the Generator**:
   ```bash
   python runmix.py
   ```

## 📋 Table of Contents
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [File Structure](#-file-structure)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Features

### Core Features
- **Smart Music Selection**: Automatically selects and manages music files
- **Precise Timing**: Accurate interval training with second-level precision
- **Progress Tracking**: Real-time updates during mix generation
- **File Management**: Automatically renames used files to prevent reuse
- **Efficient Processing**: Optimized for large music libraries

### Workout Sequences
- 12 pre-defined interval patterns (Day 1-12)
- Customizable workout durations
- Half-time announcements for longer sessions
- Support for custom instruction audio files

## 💻 System Requirements

### Minimum
- Python 3.8+
- FFmpeg
- 500MB free disk space
- 2GB RAM

### Recommended
- Python 3.10+
- 1GB+ free disk space
- 4GB+ RAM
- SSD storage for faster processing

## 📥 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/emmanuelshalu/startrunning.git
cd startrunning
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Usage

### Basic Usage
1. Add your MP3 files to the `music/` folder
2. Run the script:
   ```bash
   python runmix.py
   ```
3. Follow the on-screen prompts to select your workout day
4. Find your generated mix in the `output/` folder

### Advanced Options
```bash
# Run for a specific day
python runmix.py --day 7

# Specify custom music directory
python runmix.py --music-dir /path/to/music

# Disable file renaming
python runmix.py --no-rename
```

## 📁 File Structure
```
startrunning/
├── music/           # Your music files go here
├── instructions/    # Audio instruction files
├── output/          # Generated running mixes
├── runmix.py        # Main script
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🔧 Troubleshooting

### Common Issues
1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **FFmpeg Not Found**
   - Ensure FFmpeg is installed and in your system PATH
   - Verify with: `ffmpeg -version`

3. **Audio Quality Issues**
   - Use high-quality source files (192kbps or higher)
   - Ensure proper file permissions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📞 Support

For support, please open an issue on our [GitHub repository](https://github.com/emmanuelshalu/startrunning/issues).

## 🎵 Adding Music

### Supported Audio Formats
- MP3 (recommended)
- WAV
- OGG
- FLAC

### File Naming Conventions
- Place all music files in the `music/` directory
- Instruction files should be in `instructions/` with names like:
  - `w1.mp3`, `w2.mp3` - Workout instructions
  - `r1.mp3`, `r2.mp3` - Rest instructions
  - `d1.mp3`, `d2.mp3` - Day announcements

## 🔄 Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📚 Documentation

For detailed documentation, please visit our [Wiki](https://github.com/emmanuelshalu/startrunning/wiki).

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
