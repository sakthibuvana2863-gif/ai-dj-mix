# step4.py
import json
import os

# -----------------------------
# PARAMETERS
# -----------------------------
SEGMENTS_FILE = "best_segments_multi.json"  # from Step 3
OUTPUT_FILE = os.path.join("output", "mix_order.json")
TOP_SEGMENTS_PER_SONG = 3        # pick top N segments per song

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# -----------------------------
# LOAD ALL SONG SEGMENTS
# -----------------------------
with open(SEGMENTS_FILE, "r") as f:
    all_songs_segments = json.load(f)

# -----------------------------
# PICK TOP SEGMENTS PER SONG
# -----------------------------
song_segment_lists = []
for song_data in all_songs_segments:
    song = song_data["song"]
    segments = sorted(song_data["segments"], key=lambda x: x["energy"], reverse=True)

    # Pick top N segments per song
    top_segments = segments[:TOP_SEGMENTS_PER_SONG]

    # Add song info
    for seg in top_segments:
        seg["song"] = song

    song_segment_lists.append(top_segments)

# -----------------------------
# CREATE MIX ORDER (round-robin)
# -----------------------------
mix_order = []
segment_indices = [0] * len(song_segment_lists)  # track which segment of each song we used

while True:
    any_left = False
    # Loop over each song, pick next available segment
    for i, segments in enumerate(song_segment_lists):
        idx = segment_indices[i]
        if idx >= len(segments):
            continue  # no segments left for this song

        seg = segments[idx]
        segment_indices[i] += 1
        mix_order.append(seg)
        any_left = True

    if not any_left:
        break  # no segments left for any song

# -----------------------------
# SAVE MIX ORDER JSON
# -----------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(mix_order, f, indent=4)

# -----------------------------
# PRINT RESULT
# -----------------------------
print("\n🎧 DJ Mix Order (all songs included):")
for i, seg in enumerate(mix_order, start=1):
    print(f"{i}. {os.path.basename(seg['song'])} | Start: {seg['start']:.2f}s | "
          f"End: {seg['end']:.2f}s | Energy: {seg['energy']:.4f} | Tempo: {seg['tempo']:.2f} BPM")

print(f"\n✔ Mix order saved to {OUTPUT_FILE}")
