import librosa
import numpy as np
import os

# -----------------------------
# Step 2: Audio Analysis
# -----------------------------

def get_key(y, sr):
    """
    Estimate the musical key of the audio using chroma features.
    Returns a key as a string (C, C#, D, etc.)
    """
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key_index = np.argmax(np.mean(chroma, axis=1))
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F',
            'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key_index]


def analyze_audio_file(audio_path):
    """
    Analyze a single audio file.
    Returns tempo, energy, key, and duration.
    """
    y, sr = librosa.load(audio_path, sr=None)

    # Tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Energy (RMS)
    rms = librosa.feature.rms(y=y)[0]
    avg_energy = float(np.mean(rms))

    # Key
    key = get_key(y, sr)

    # Duration (seconds)
    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "song": os.path.basename(audio_path),
        "tempo": float(tempo),
        "energy": avg_energy,
        "key": key,
        "duration": float(duration)
    }


def analyze_all_songs(file_list):
    """
    Analyze multiple audio files.
    """
    results = []
    for f in file_list:
        print(f"Analyzing: {f}")
        results.append(analyze_audio_file(f))
    return results


def analyze_audio():
    """
    ENTRY POINT for Streamlit app.
    This is the function app.py should import.
    """
    processed_folder = "processed"

    if not os.path.exists(processed_folder):
        return []

    wav_files = [
        os.path.join(processed_folder, f)
        for f in os.listdir(processed_folder)
        if f.endswith(".wav")
    ]

    if not wav_files:
        return []

    return analyze_all_songs(wav_files)


# -----------------------------
# Local testing only
# -----------------------------
if __name__ == "__main__":
    results = analyze_audio()
    for r in results:
        print(r)
