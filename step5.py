# step5.py
import librosa
import soundfile as sf
import numpy as np
import os

OUTPUT_FOLDER = "output"
CROSSFADE_DURATION = 2.0  # seconds


# -----------------------------
# Audio helpers
# -----------------------------
def normalize_audio(audio, target_peak=0.9):
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio * (target_peak / peak)


def time_stretch_to_bpm(audio, original_bpm, target_bpm):
    """
    Stretch audio to match target BPM
    """
    if original_bpm <= 0 or target_bpm <= 0:
        return audio

    rate = target_bpm / original_bpm

    # librosa fails on very short clips sometimes
    if len(audio) < 2048:
        return audio

    return librosa.effects.time_stretch(audio, rate=rate)


# -----------------------------
# Main mix generator
# -----------------------------
def generate_final_mix(mix_order):
    """
    Generate final DJ mix WAV using BPM matching,
    volume normalization, and crossfading.
    """
    if not mix_order:
        raise ValueError("Mix order is empty")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, "final_dj_mix.wav")

    # -----------------------------
    # Determine target BPM (median)
    # -----------------------------
    bpms = [seg["tempo"] for seg in mix_order if seg.get("tempo", 0) > 0]
    target_bpm = float(np.median(bpms)) if bpms else None

    final_mix = None
    sr_final = None

    for seg_data in mix_order:
        audio_path = os.path.join("processed", seg_data["song"])
        start_time = seg_data["start"]
        end_time = seg_data["end"]
        segment_bpm = seg_data.get("tempo", 0)

        if not os.path.exists(audio_path):
            continue

        # Load audio
        y, sr = librosa.load(audio_path, sr=None)

        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)

        if end_sample <= start_sample:
            continue

        segment_audio = y[start_sample:end_sample]

        # -----------------------------
        # BPM MATCHING (NEW)
        # -----------------------------
        if target_bpm:
            segment_audio = time_stretch_to_bpm(
                segment_audio,
                segment_bpm,
                target_bpm
            )

        # -----------------------------
        # VOLUME NORMALIZATION
        # -----------------------------
        segment_audio = normalize_audio(segment_audio)

        # First segment
        if final_mix is None:
            final_mix = segment_audio
            sr_final = sr
            continue

        # -----------------------------
        # Crossfade
        # -----------------------------
        fade_samples = int(CROSSFADE_DURATION * sr)
        fade_samples = min(
            fade_samples,
            len(final_mix),
            len(segment_audio)
        )

        fade_out = final_mix[-fade_samples:]
        fade_in = segment_audio[:fade_samples]

        fade_out_curve = np.linspace(1, 0, fade_samples)
        fade_in_curve = np.linspace(0, 1, fade_samples)

        crossfade = (
            fade_out * fade_out_curve +
            fade_in * fade_in_curve
        )

        final_mix = np.concatenate([
            final_mix[:-fade_samples],
            crossfade,
            segment_audio[fade_samples:]
        ])

    if final_mix is None:
        raise RuntimeError("Final mix generation failed")

    sf.write(output_path, final_mix, sr_final)
    return output_path


# -----------------------------
# Local testing only
# -----------------------------
if __name__ == "__main__":
    print("Run step5 via app.py, not directly.")
