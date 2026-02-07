# step2.py
import os
import librosa

PROCESSED_FOLDER = "processed"

def analyze_audio():
    if not os.path.exists(PROCESSED_FOLDER):
        return "Processed folder not found"

    analysis = []

    for file in os.listdir(PROCESSED_FOLDER):
        if file.endswith(".wav"):
            path = os.path.join(PROCESSED_FOLDER, file)

            y, sr = librosa.load(path, sr=None)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

            analysis.append({
                "file": file,
                "tempo": float(tempo)
            })

    return analysis
