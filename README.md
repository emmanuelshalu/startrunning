# RunMix Generator

A web application for generating custom running mixes with interval training instructions and your favorite music.

## Features

- **Web-based Interface**: User-friendly interface for generating running mixes
- **Music Management**: Upload your own music files or import from Spotify
- **Custom Workouts**: 12 pre-defined workout sequences with different interval patterns
- **Progress Tracking**: Real-time progress updates during mix generation
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (for audio processing)
- Spotify Developer Account (for Spotify integration - optional)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/runmix-generator.git
   cd runmix-generator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following content:
   ```
   # Required for Spotify integration
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   
   # Optional: Flask secret key (will be auto-generated if not set)
   # FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Install FFmpeg**
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [FFmpeg's website](https://ffmpeg.org/download.html)

## Directory Structure

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
├── runmix.py             # Core run mix generation logic
├── spotify_downloader.py # Spotify integration
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your web browser**
   ```
   http://localhost:5000
   ```

## Usage

1. **Add Music**
   - Click "Upload" to add your own music files
   - Or import a Spotify playlist by pasting its URL

2. **Generate a RunMix**
   - Select a day (1-12) from the dropdown
   - Click "Generate RunMix"
   - Wait for the generation to complete
   - Download your custom run mix

## Spotify Integration (Optional)

To enable Spotify playlist importing:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Copy your Client ID and Client Secret to the `.env` file
4. Add `http://localhost:5000` as a Redirect URI in your Spotify app settings

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
