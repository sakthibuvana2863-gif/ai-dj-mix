# step5.py
import librosa
import soundfile as sf
import numpy as np
import os

OUTPUT_FOLDER = "output"
CROSSFADE_DURATION = 2.0  # seconds


def normalize_audio(audio, target_peak=0.9):
    """
    Normalize audio to a target peak level.
    Prevents loud/quiet jumps between segments.
    """
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio * (target_peak / peak)


def generate_final_mix(mix_order):
    """
    Generate final DJ mix WAV using segment timestamps and crossfading.
    Accepts output from step4.create_mix_order()
    """
    if not mix_order:
        raise ValueError("Mix order is empty")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, "final_dj_mix.wav")

    final_mix = None
    sr_final = None

    for idx, seg_data in enumerate(mix_order):
        audio_path = os.path.join("processed", seg_data["song"])
        start_time = seg_data["start"]
        end_time = seg_data["end"]

        if not os.path.exists(audio_path):
            continue

        # Load audio
        y, sr = librosa.load(audio_path, sr=None)

        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)

        if end_sample <= start_sample:
            continue

        segment_audio = y[start_sample:end_sample]

        # 🔥 NORMALIZE SEGMENT (NEW)
        segment_audio = normalize_audio(segment_audio)

        # First segment
        if final_mix is None:
            final_mix = segment_audio
            sr_final = sr
            continue

        # Crossfade
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
