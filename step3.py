# step3.py
import librosa
import numpy as np
import os

# -----------------------------
# Low-level segment extraction
# -----------------------------
def extract_segments_from_file(audio_path, segment_duration=8.0, overlap=4.0):
    """
    Extract overlapping segments from a single audio file.
    """
    y, sr = librosa.load(audio_path, sr=None)
    audio_duration = librosa.get_duration(y=y, sr=sr)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    rms = librosa.feature.rms(y=y)[0]
    rms_smooth = np.convolve(rms, np.ones(10) / 10, mode="same")
    energy_times = librosa.frames_to_time(
        np.arange(len(rms_smooth)), sr=sr
    )

    segments = []
    start_time = 0.0

    while start_time + segment_duration <= audio_duration:
        end_time = start_time + segment_duration

        idx = np.where(
            (energy_times >= start_time) & (energy_times <= end_time)
        )[0]

        if len(idx) == 0:
            start_time += overlap
            continue

        avg_energy = float(np.mean(rms_smooth[idx]))
        nearest_beat = float(
            beat_times[np.argmin(np.abs(beat_times - start_time))]
        )

        segments.append({
            "start": nearest_beat,
            "end": nearest_beat + segment_duration,
            "energy": avg_energy,
            "tempo": float(tempo)
        })

        start_time += overlap

    return sorted(segments, key=lambda x: x["energy"], reverse=True)

# -----------------------------
# ENTRY POINT for app.py
# -----------------------------
def extract_segments(analysis):
    """
    Extract segments for all analyzed songs.
    Accepts output from step2.analyze_audio()
    """
    if not analysis:
        return []

    processed_folder = "processed"
    all_segments = []

    for song in analysis:
        wav_path = os.path.join(processed_folder, song["song"])

        if not os.path.exists(wav_path):
            continue

        segments = extract_segments_from_file(wav_path)

        all_segments.append({
            "song": song["song"],
            "tempo": song["tempo"],
            "key": song["key"],
            "segments": segments
        })

    return all_segments


# -----------------------------
# Local testing only
# -----------------------------
if __name__ == "__main__":
    print("Run step3 via app.py, not directly.")
