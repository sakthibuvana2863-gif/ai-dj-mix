# step5_final_dj_mix.py
import json
import librosa
import soundfile as sf
import numpy as np
import os

# -----------------------------
# PARAMETERS
# -----------------------------
MIX_ORDER_FILE = "output/mix_order.json"  # from Step 4
OUTPUT_FILE = "output/final_dj_mix.wav"
CROSSFADE_DURATION = 2.0  # seconds

# -----------------------------
# LOAD MIX ORDER
# -----------------------------
with open(MIX_ORDER_FILE, "r") as f:
    mix_order = json.load(f)

print("🎛️ Mixing order loaded:")
for i, song_data in enumerate(mix_order, start=1):
    print(f"{i}. {os.path.basename(song_data['song'])} | "
          f"Start: {song_data['start']:.2f}s | End: {song_data['end']:.2f}s | "
          f"Energy: {song_data['energy']:.4f} | Tempo: {song_data['tempo']:.2f} BPM")

# -----------------------------
# MIXING LOGIC
# -----------------------------
final_mix = None
sr_final = None

for idx, seg_data in enumerate(mix_order):
    audio_path = seg_data["song"]
    start_time = seg_data["start"]
    end_time = seg_data["end"]

    # Load full audio
    y, sr = librosa.load(audio_path, sr=None)

    # Extract segment
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    segment_audio = y[start_sample:end_sample]

    # First segment
    if final_mix is None:
        final_mix = segment_audio
        sr_final = sr
        continue

    # Crossfade
    fade_samples = int(CROSSFADE_DURATION * sr)
    fade_samples = min(fade_samples, len(final_mix), len(segment_audio))

    fade_out = final_mix[-fade_samples:]
    fade_in = segment_audio[:fade_samples]

    fade_out_curve = np.linspace(1, 0, fade_samples)
    fade_in_curve = np.linspace(0, 1, fade_samples)

    crossfade = fade_out * fade_out_curve + fade_in * fade_in_curve

    # Concatenate: final_mix (excluding fade out) + crossfade + segment_audio (after fade in)
    final_mix = np.concatenate([final_mix[:-fade_samples], crossfade, segment_audio[fade_samples:]])

# -----------------------------
# SAVE FINAL MIX
# -----------------------------
os.makedirs("output", exist_ok=True)
sf.write(OUTPUT_FILE, final_mix, sr_final)

print(f"\n✔ Step 5 complete: Final DJ mix saved as {OUTPUT_FILE}")
