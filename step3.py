# step3.py
import librosa
import numpy as np
from os import listdir
from os.path import join
import json

# -----------------------------
# Function: Extract segments
# -----------------------------
def extract_segments(audio_path, segment_duration=8.0, overlap=4.0, top_n=None):
    """
    Extract overlapping segments from a song.
    If top_n is None → return all segments sorted by energy
    Otherwise → return top_n segments
    """
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    audio_duration = librosa.get_duration(y=y, sr=sr)

    # Beat tracking
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # RMS energy
    rms = librosa.feature.rms(y=y)[0]
    rms_smooth = np.convolve(rms, np.ones(10)/10, mode='same')
    energy_times = librosa.frames_to_time(np.arange(len(rms_smooth)), sr=sr)

    segments = []
    start_time = 0.0

    while start_time + segment_duration <= audio_duration:
        end_time = start_time + segment_duration

        # Energy in this window
        idx = np.where((energy_times >= start_time) & (energy_times <= end_time))[0]
        if len(idx) == 0:
            start_time += overlap
            continue

        avg_energy = np.mean(rms_smooth[idx])

        # Align start to nearest beat
        nearest_beat = beat_times[np.argmin(np.abs(beat_times - start_time))]

        segments.append({
            "start": float(nearest_beat),
            "end": float(nearest_beat + segment_duration),
            "energy": float(avg_energy),
            "tempo": float(tempo)
        })

        start_time += overlap

    # Sort segments by energy
    sorted_segments = sorted(segments, key=lambda x: x["energy"], reverse=True)

    if top_n is not None:
        sorted_segments = sorted_segments[:top_n]

    return sorted_segments

# -----------------------------
# Step 3: Loop through all WAV files
# -----------------------------
processed_folder = "processed"
wav_files = [join(processed_folder, f) for f in listdir(processed_folder) if f.endswith(".wav")]

all_segments = []

for f in wav_files:
    print(f"\nExtracting segments for: {f}")
    # Return ALL segments for now (flexible)
    segments = extract_segments(f, segment_duration=8.0, overlap=4.0, top_n=None)
    
    song_segments = {
        "song": f,
        "segments": segments
    }
    all_segments.append(song_segments)
    
    # Print top 5 segments for preview
    print("Top 5 segments (by energy):")
    for i, seg in enumerate(segments[:5]):
        print(f" Segment {i+1}: Start {seg['start']:.2f}s, End {seg['end']:.2f}s, "
              f"Energy {seg['energy']:.5f}, Tempo {seg['tempo']:.2f} BPM")

# -----------------------------
# Save all segments to JSON
# -----------------------------
with open("best_segments_multi.json", "w") as f:
    json.dump(all_segments, f, indent=4)

print("\n✔ All segments saved to best_segments_multi.json")
