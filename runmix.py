from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import subprocess
import sys

# Ask user if they want to download music from Spotify
download_music = input("\nDo you want to download music from Spotify? (yes/no): ").strip().lower()
if download_music in ('yes', 'y'):
    print("\nLaunching Spotify downloader...")
    try:
        subprocess.run([sys.executable, 'spotify_downloader.py'], check=True)
        print("\nSpotify download completed. Continuing with run mix generation...")
    except subprocess.CalledProcessError as e:
        print(f"\nError running Spotify downloader: {e}")
        print("Continuing with existing music files...")
    except FileNotFoundError:
        print("\nError: spotify_downloader.py not found. Please make sure it's in the same directory.")
        print("Continuing with existing music files...")

# Time multipliers
instruction_times = {
    'w1': 60,  # in seconds
    'w2': 120,
    'w3': 180,
    'w4': 240,
    'w5': 300,
    'r1': 60,
    'r2': 120,
    'r3': 180,
    'r4': 240,
    'r5': 300,
    'r6': 360,
    'r7': 420
}

# Directory setup
music_folder = 'music'
instruction_folder = 'instructions'
output_folder = 'output'  # Added output folder
# Output filename will be set based on selected day

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created output folder: {output_folder}")

# Hardcoded preset sequences for different days
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
    12: 'w5,r4,w1,r5,w1,r7,w2,r5,w5'
}

# Prompt user for day selection with clear instructions
print("=" * 70)
print("RUN MIX GENERATOR")
print("=" * 70)

while True:
    try:
        day_input = input("Enter the day (1-12): ").strip()
        day = int(day_input)
        
        if day in day_sequences:
            sequence = day_sequences[day].split(',')
            output_file = os.path.join(output_folder, f'day{day}_run_mix.mp3')  # Set output filename in output folder
            print(f"Selected Day {day} sequence with {len(sequence)} intervals")
            print(f"Output will be saved as: {output_file}")
            break
        else:
            print("Invalid day! Please enter 1-12.")
    except ValueError:
        print("Invalid input! Please enter a number (1-12).")

# Calculate total music duration needed from sequence
# We'll add a 10% buffer to ensure we have enough music
total_sequence_duration = sum(instruction_times[code] for code in sequence) * 1.1  # in seconds
print(f"\nEstimated music duration needed: {int(total_sequence_duration)} seconds")

# Get list of music files, excluding those with '_taken' in the name
music_files = [f for f in os.listdir(music_folder) 
              if f.endswith('.mp3') and '_taken' not in f]
music_files.sort()  # Ensure consistent order
print(f"Found {len(music_files)} music files")

full_music = AudioSegment.empty()
song_boundaries = []  # Track start and end positions of each song
current_position = 0
loaded_duration = 0  # Track total loaded duration in milliseconds
required_duration = total_sequence_duration * 1000  # Convert to milliseconds

print("Loading music files (will stop when enough is loaded):")

for i, file in enumerate(music_files, 1):
    if loaded_duration >= required_duration:
        print(f"  Reached required duration of {required_duration//1000} seconds")
        break
        
    print(f"  [{i}] Loading: {file}")
    try:
        song = AudioSegment.from_mp3(os.path.join(music_folder, file))
        song_duration = len(song)
        song_start = current_position
        song_end = current_position + song_duration
        
        song_boundaries.append({
            'file': file,
            'start': song_start,
            'end': song_end
        })
        
        full_music += song
        current_position = song_end
        loaded_duration += song_duration
        
        print(f"    Added {song_duration // 1000} seconds of audio")
        print(f"    Total loaded: {loaded_duration // 1000} / {required_duration // 1000} seconds")
        
    except Exception as e:
        print(f"    Error loading {file}: {str(e)}")
        continue

print(f"\nFinished loading {len(song_boundaries)} files")
print(f"Total music loaded: {loaded_duration // 1000} seconds")

cursor = 0
final_track = AudioSegment.empty()
print(f"\nTotal music duration: {len(full_music) // 1000} seconds")

# Add the corresponding day mention audio at the beginning
print("\nAdding day announcement...")
day_mention_code = f'd{day}'
day_mention_path = os.path.join(instruction_folder, f'{day_mention_code}.mp3')
if os.path.exists(day_mention_path):
    print(f"  Adding day {day} announcement")
    day_mention_audio = AudioSegment.from_mp3(day_mention_path)
    final_track += day_mention_audio + AudioSegment.silent(duration=500)
    print(f"  Added {len(day_mention_audio) // 1000} seconds of day announcement")
else:
    print(f"  Warning: {day_mention_code}.mp3 not found in instructions folder. Skipping day mention audio.")

# Calculate total duration of the sequence first
total_duration = sum(instruction_times[code] for code in sequence) * 1000  # in ms
half_way_point = total_duration // 2
current_position = 0
half_way_reached = False

# Process sequence
print("\nProcessing sequence:")
total_segments = len(sequence)
for i, code in enumerate(sequence, 1):
    # Load instruction MP3
    print(f"\n[{i}/{total_segments}] Processing segment: {code} ({instruction_times[code]}s)")
    instruction_path = os.path.join(instruction_folder, f'{code}.mp3')
    print(f"  Loading instruction: {code}.mp3")
    instruction = AudioSegment.from_mp3(instruction_path)
    print(f"  Adding {len(instruction) // 1000} seconds of instruction audio")
    
    # Add instruction to final track
    final_track += instruction + AudioSegment.silent(duration=500)
    print(f"  Added instruction to track")
    
    # Get time in ms
    duration_ms = instruction_times[code] * 1000
    
    # Check if this is the last instruction in the sequence
    is_last_instruction = (i == len(sequence) - 1)
    
    # Handle the last instruction separately
    if is_last_instruction:
        # Find the current song that's playing at cursor position
        current_song_start = 0
        current_song_end = 0
        
        # Calculate which song we're currently in
        for file in music_files:
            song_path = os.path.join(music_folder, file)
            song = AudioSegment.from_mp3(song_path)
            song_duration = len(song)
            
            if current_song_start <= cursor < current_song_start + song_duration:
                # We found the current song
                current_song_end = current_song_start + song_duration
                break
            current_song_start += song_duration
        
        # Extract music from cursor to the end of the current song
        remaining_duration = current_song_end - cursor
        music_segment = full_music[cursor:cursor + remaining_duration]
        final_track += music_segment
        break  # Exit the loop after handling the last instruction
    
    # For non-last instructions, get the music segment for this interval
    print(f"  Adding {duration_ms // 1000} seconds of music")
    music_segment = full_music[cursor:cursor + duration_ms]
    
    # Check if we've reached or passed the halfway point
    if not half_way_reached and (current_position + duration_ms >= half_way_point):
        # Calculate position to insert half-time announcement
        insert_pos = half_way_point - current_position
        
        # Split the current music segment
        first_half = music_segment[:insert_pos]
        second_half = music_segment[insert_pos:]
        
        # Add first half of music
        final_track += first_half
        
        # Add half-time announcement if the file exists
        half_announcement_path = os.path.join(instruction_folder, 'half.mp3')
        if os.path.exists(half_announcement_path):
            half_announcement = AudioSegment.from_mp3(half_announcement_path)
            final_track += half_announcement + AudioSegment.silent(duration=500)
        
        # Add second half of music
        final_track += second_half
        half_way_reached = True
    else:
        # Normal processing if we haven't reached or already passed halfway
        final_track += music_segment
    
    # Update position and cursor
    current_position += duration_ms
    cursor += duration_ms
    print(f"  Progress: {current_position // 1000} / {total_duration // 1000} seconds ({int((current_position / total_duration) * 100)}%)")

# Export the final track
print("\nExporting final mix...")
final_track.export(output_file, format='mp3')
print(f"\n✅ Success! Output saved to: {output_file}")
print(f"Total duration: {len(final_track) // 1000} seconds")

# Determine which songs are actually used in the final output
print("\nAnalyzing music usage...")
# Calculate the total duration of the final track (excluding day mention and instructions)
total_music_duration = 0
temp_cursor = 0  # Use a separate cursor for calculation

for i, code in enumerate(sequence):
    if i == len(sequence) - 1:
        # For the last instruction, calculate the actual duration used
        current_song_end = 0
        
        # Find which song we're currently in
        for boundary in song_boundaries:
            if boundary['start'] <= temp_cursor < boundary['end']:
                current_song_end = boundary['end']
                break
        
        remaining_duration = current_song_end - temp_cursor
        total_music_duration += remaining_duration
    else:
        # For all other instructions, use the normal duration
        duration_ms = instruction_times[code] * 1000
        total_music_duration += duration_ms
        temp_cursor += duration_ms

# Find which songs are actually used in the output
used_files = []
for boundary in song_boundaries:
    # Check if any part of this song is used in the final output
    if boundary['start'] < total_music_duration and boundary['end'] > 0:
        used_files.append(boundary['file'])

# Rename only the music files that are actually used in the output
print("\nRenaming music files used in the output...")
print(f"\nRenaming used music files ({len(used_files)} files):")
for file in used_files:
    old_path = os.path.join(music_folder, file)
    # Extract filename without extension
    name_without_ext = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    print(f"  Renaming: {file}")
    new_filename = f"{name_without_ext}_taken{extension}"
    new_path = os.path.join(music_folder, new_filename)
    
    try:
        os.rename(old_path, new_path)
        print(f"Renamed: {file} → {new_filename}")
    except FileNotFoundError:
        print(f"Warning: Could not rename {file} (file not found)")
    except PermissionError:
        print(f"Warning: Could not rename {file} (permission denied)")
    except Exception as e:
        print(f"Warning: Could not rename {file} (error: {e})")

print(f"\nProcess completed! {len(used_files)} music files have been renamed with '_taken' suffix.")
print("\nPlease remove those files from the music folder to avoid reusing them.")
print("\nYou can now run the script again to generate a new run mix.")
print("\n")
print("=" * 70)
