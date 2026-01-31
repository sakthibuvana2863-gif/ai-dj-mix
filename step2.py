import librosa
import numpy as np
import os

# -----------------------------
# Step 2: Audio Analysis
# -----------------------------
def get_key(y, sr):
    """
    Estimate the key of the audio using chroma.
    Returns a musical key as a string (C, C#, D, etc.)
    """
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key_index = np.argmax(np.mean(chroma, axis=1))
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F',
            'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key_index]

def analyze_audio_file(audio_path):
    """
    Analyze tempo, energy, key, and duration of a song.
    Returns a dictionary.
    """
    y, sr = librosa.load(audio_path, sr=None)
    
    # Tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # Energy (average RMS)
    rms = librosa.feature.rms(y=y)[0]
    avg_energy = float(np.mean(rms))
    
    # Key
    key = get_key(y, sr)
    
    # Duration
    duration = librosa.get_duration(y=y, sr=sr)
    
    return {
        "song": audio_path,
        "tempo": float(tempo),
        "energy": avg_energy,
        "key": key,
        "duration": float(duration)
    }

def analyze_all_songs(file_list):
    """
    Analyze multiple songs and return a list of analysis dictionaries.
    """
    analysis_results = []
    for f in file_list:
        print(f"Analyzing: {f}")
        analysis = analyze_audio_file(f)
        analysis_results.append(analysis)
    return analysis_results

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    processed_folder = "processed"
    wav_files = [os.path.join(processed_folder, f)
                 for f in os.listdir(processed_folder) if f.endswith(".wav")]
    
    all_analysis = analyze_all_songs(wav_files)
    
    for a in all_analysis:
        print(f"\nSong: {a['song']}")
        print(f"  Tempo:  {a['tempo']:.2f} BPM")
        print(f"  Energy: {a['energy']:.5f}")
        print(f"  Key:    {a['key']}")
        print(f"  Duration: {a['duration']:.2f}s")
