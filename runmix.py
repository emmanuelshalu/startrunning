from pydub import AudioSegment
from pydub.utils import make_chunks
import os

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
    'r5': 300
}

# Directory setup
music_folder = 'music'
instruction_folder = 'instructions'
# Output filename will be set based on selected day

# Hardcoded preset sequences for different days
day_sequences = {
    1: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    2: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    3: 'w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5',
    4: 'w5,r1,w1,r1,w1,r2,w1,r2,w2,r2,w2,r1,w1,r1,w5'
}

# Prompt user for day selection with clear instructions
print("=" * 50)
print("RUN MIX GENERATOR")
print("=" * 50)
print("Available preset sequences:")
print("Day 1: 12 intervals (w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5)")
print("Day 2: 14 intervals (w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5)")
print("Day 3: 16 intervals (w5,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w1,r1,w5)")
print("Day 4: 14 intervals (w5,r1,w1,r1,w1,r2,w1,r2,w2,r2,w2,r1,w1,r1,w5)")
print("=" * 50)

while True:
    try:
        day_input = input("Enter the day (1-4): ").strip()
        day = int(day_input)
        
        if day in day_sequences:
            sequence = day_sequences[day].split(',')
            output_file = f'day{day}_run_mix.mp3'  # Set output filename based on selected day
            print(f"Selected Day {day} sequence with {len(sequence)} intervals")
            print(f"Output will be saved as: {output_file}")
            break
        else:
            print("Invalid day! Please enter 1-4.")
    except ValueError:
        print("Invalid input! Please enter a number (1-4).")

# Combine all music files into one big track
music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
music_files.sort()  # Ensure consistent order
full_music = AudioSegment.empty()
song_boundaries = []  # Track start and end positions of each song
current_position = 0

for file in music_files:
    song = AudioSegment.from_mp3(os.path.join(music_folder, file))
    song_start = current_position
    song_end = current_position + len(song)
    song_boundaries.append({
        'file': file,
        'start': song_start,
        'end': song_end
    })
    full_music += song
    current_position = song_end

cursor = 0
final_track = AudioSegment.empty()

# Add the corresponding day mention audio at the beginning
# d1.mp3 for Day 1, d2.mp3 for Day 2, d3.mp3 for Day 3
# These files should be placed in the instructions folder

day_mention_code = f'd{day}'
day_mention_path = os.path.join(instruction_folder, f'{day_mention_code}.mp3')
if os.path.exists(day_mention_path):
    day_mention_audio = AudioSegment.from_mp3(day_mention_path)
    final_track += day_mention_audio + AudioSegment.silent(duration=500)
else:
    print(f"Warning: {day_mention_code}.mp3 not found in instructions folder. Skipping day mention audio.")

# Process sequence
for i, code in enumerate(sequence):
    # Load instruction MP3
    instruction_path = os.path.join(instruction_folder, f'{code}.mp3')
    instruction = AudioSegment.from_mp3(instruction_path)
    
    # Add instruction to final track
    final_track += instruction + AudioSegment.silent(duration=500)
    
    # Get time in ms
    duration_ms = instruction_times[code] * 1000
    
    # Check if this is the last instruction in the sequence
    is_last_instruction = (i == len(sequence) - 1)
    
    if is_last_instruction:
        # For the last instruction, play the current song until its end
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
    else:
        # For all other instructions, use the normal duration
        music_segment = full_music[cursor:cursor + duration_ms]
        final_track += music_segment
        cursor += duration_ms

# Export the final track
final_track.export(output_file, format='mp3')
print(f"Output saved to {output_file}")

# Determine which songs are actually used in the final output
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
for file in used_files:
    old_path = os.path.join(music_folder, file)
    # Extract filename without extension
    name_without_ext = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
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
