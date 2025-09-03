from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import sys
from pydub import AudioSegment
from pydub.utils import make_chunks
import json
from dotenv import load_dotenv
import threading
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MUSIC_FOLDER'] = 'music'
app.config['INSTRUCTION_FOLDER'] = 'instructions'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['SECRET_KEY'] = os.urandom(24)

# Ensure required directories exist
for folder in [app.config['UPLOAD_FOLDER'], 
               app.config['MUSIC_FOLDER'], 
               app.config['INSTRUCTION_FOLDER'],
               app.config['OUTPUT_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Time multipliers for different workout types
time_multipliers = {
    'w1': 60, 'w2': 120, 'w3': 180, 'w4': 240, 'w5': 300,
    'r1': 60, 'r2': 120, 'r3': 180, 'r4': 240, 'r5': 300, 'r6': 360, 'r7': 420
}

# Workout sequences for different days
day_sequences = {
    1: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    2: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    3: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    4: 'w5,r1,w1,r1,w1,r2,w1,r2,w2,r2,w2,r1,w1,r1,w5',
    5: 'w5,r1,w1,r2,w1,r2,w1,r2,w2,r2,w2,r2,w1,r1,w5',
    6: 'w5,r1,w1,r2,w1,r2,w1,r3,w2,r3,w2,r2,w1,r1,w5',
    7: 'w5,r2,w1,r2,w1,r3,w2,r4,w2,r4,w2,r3,w2,r2,w5',
    8: 'w5,r2,w1,r2,w1,r3,w2,r4,w2,r4,w1,r2,w5',
    9: 'w5,r2,w1,r4,w1,r5,w2,r4,w2,r3,w5',
    10: 'w5,r4,w1,r5,w2,r5,w2,r5,w5',
    11: 'w5,r4,w1,r5,w1,r6,w2,r5,w5',
    12: 'w5,r4,w1,r5,w1,r7,w2,r5,w5',
    13: 'w5,r4,w1,r6,w2,r8,w2,r4,w5',
    14: 'w5,r4,w1,r6,w2,r9,w2,r4,w5',
    15: 'w5,r4,w1,r6,w2,r10,w2,r4,w5',
    16: 'w5,r3,w1,r7,w2,r11,w2,r4,w5',
    17: 'w5,r3,w1,r7,w2,r12,w2,r4,w5',
    18: 'w5,r3,w1,r7,w2,r13,w2,r4,w5',
    19: 'w5,r6,w2,r14,w2,r8,w5',
    20: 'w5,r6,w2,r15,w2,r8,w5',
    21: 'w5,r6,w2,r16,w2,r8,w5',
    22: 'w5,r6,w2,r17,w2,r7,w5',
    23: 'w5,r6,w2,r18,w2,r6,w5',
    24: 'w5,r10,w3,r20,w5',
    25: 'w5,r8,w3,r22,w5',
    26: 'w5,r6,w2,r24,w5',
    27: 'w5,r4,w2,r26,w5',
    28: 'w5,r2,w2,r28,w5',
    29: 'w5,r30,w5',
    30: 'w5,r32,w5'
}

# Track generation status
generation_status = {
    'in_progress': False,
    'progress': 0,
    'message': '',
    'output_file': None,
    'error': None
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'ogg'}

def get_available_music():
    """Get list of available music files."""
    return [f for f in os.listdir(app.config['MUSIC_FOLDER']) 
            if f.endswith('.mp3') and '_taken' not in f]

@app.route('/')
def index():
    return render_template('index.html', 
                         days=day_sequences.keys(),
                         music_files=get_available_music())

@app.route('/generate', methods=['POST'])
def generate_mix():
    global generation_status
    
    if generation_status['in_progress']:
        return jsonify({'status': 'error', 'message': 'Generation already in progress'}), 400
    
    try:
        day = int(request.form.get('day', 1))
        if day not in day_sequences:
            return jsonify({'status': 'error', 'message': 'Invalid day selected'}), 400
        
        # Start generation in a separate thread
        thread = threading.Thread(target=generate_run_mix, args=(day,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'started', 'message': 'Generation started'})
        
    except Exception as e:
        generation_status['error'] = str(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

def generate_run_mix(day):
    """Generate run mix in a separate thread."""
    global generation_status
    
    try:
        generation_status = {
            'in_progress': True,
            'progress': 0,
            'message': 'Starting generation...',
            'output_file': None,
            'error': None
        }
        
        sequence = day_sequences[day].split(',')
        output_file = os.path.join(app.config['OUTPUT_FOLDER'], f'day{day}_run_mix.mp3')
        
        # Calculate total duration needed
        total_duration = sum(time_multipliers[code] for code in sequence) * 1.1  # 10% buffer
        
        # Get music files
        music_files = get_available_music()
        if not music_files:
            raise Exception("No music files found. Please upload some music first.")
        
        # Combine music files to create a long enough track
        full_music = AudioSegment.empty()
        current_duration = 0
        
        generation_status['message'] = 'Combining music tracks...'
        
        for music_file in music_files:
            if current_duration >= total_duration * 1000:  # Convert to milliseconds
                break
                
            music_path = os.path.join(app.config['MUSIC_FOLDER'], music_file)
            try:
                audio = AudioSegment.from_file(music_path)
                full_music += audio
                current_duration += len(audio)
                
                # Mark file as used
                os.rename(music_path, 
                         os.path.join(app.config['MUSIC_FOLDER'], 
                                     f"{os.path.splitext(music_file)[0]}_taken{os.path.splitext(music_file)[1]}"))
                
                generation_status['progress'] = min(50, int((current_duration / (total_duration * 1000)) * 50))
                
            except Exception as e:
                print(f"Error processing {music_file}: {e}")
        
        if current_duration < total_duration * 1000:
            raise Exception("Not enough music available. Please upload more music files.")
        
        # Add day announcement
        day_announcement = os.path.join(app.config['INSTRUCTION_FOLDER'], f'd{day}.mp3')
        if os.path.exists(day_announcement):
            generation_status['message'] = 'Adding day announcement...'
            announcement = AudioSegment.from_file(day_announcement)
            full_music = announcement + AudioSegment.silent(duration=1000) + full_music
        
        # Generate final mix with instructions
        generation_status['message'] = 'Mixing in instructions...'
        final_mix = AudioSegment.empty()
        position = 0
        
        for i, code in enumerate(sequence):
            if i < len(sequence) - 1:
                instruction_duration = time_multipliers[code] * 1000  # Convert to milliseconds
                segment = full_music[position:position + instruction_duration]
                final_mix += segment
                position += instruction_duration
                
                # Add instruction audio if available
                instruction_file = os.path.join(app.config['INSTRUCTION_FOLDER'], f'{code}.mp3')
                if os.path.exists(instruction_file):
                    instruction = AudioSegment.from_file(instruction_file)
                    final_mix = final_mix.overlay(instruction, position=len(final_mix) - len(instruction))
                
                generation_status['progress'] = 50 + int((i / len(sequence)) * 50)
        
        # Export final mix
        generation_status['message'] = 'Exporting final mix...'
        final_mix.export(output_file, format='mp3')
        
        generation_status.update({
            'in_progress': False,
            'progress': 100,
            'message': 'Generation complete!',
            'output_file': f'day{day}_run_mix.mp3'
        })
        
    except Exception as e:
        generation_status.update({
            'in_progress': False,
            'error': str(e),
            'message': f'Error: {str(e)}'
        })

@app.route('/status')
def status():
    return jsonify(generation_status)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['MUSIC_FOLDER'], filename))
        return jsonify({
            'status': 'success', 
            'message': 'File uploaded successfully',
            'filename': filename
        })
    
    return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400

@app.route('/spotify', methods=['POST'])
def import_spotify():
    try:
        playlist_url = request.json.get('playlist_url')
        if not playlist_url:
            return jsonify({'status': 'error', 'message': 'No playlist URL provided'}), 400
        
        # Run spotify_downloader.py as a subprocess
        process = subprocess.Popen(
            [sys.executable, 'spotify_downloader.py', playlist_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Return immediately, client will poll for updates
        return jsonify({
            'status': 'started',
            'message': 'Spotify import started in the background'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
