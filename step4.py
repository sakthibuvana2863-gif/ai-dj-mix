# step4.py
import os

def create_mix_order(all_songs_segments, top_segments_per_song=3):
    """
    Create DJ mix order using round-robin selection.
    Accepts output from step3.extract_segments()
    """
    if not all_songs_segments:
        return []

    # -----------------------------
    # Pick top segments per song
    # -----------------------------
    song_segment_lists = []

    for song_data in all_songs_segments:
        song = song_data["song"]
        segments = sorted(
            song_data["segments"],
            key=lambda x: x["energy"],
            reverse=True
        )

        top_segments = segments[:top_segments_per_song]

        for seg in top_segments:
            seg_copy = seg.copy()
            seg_copy["song"] = song
            song_segment_lists.append(seg_copy)

    # -----------------------------
    # Round-robin ordering
    # -----------------------------
    mix_order = []
    song_buckets = {}

    for seg in song_segment_lists:
        song_buckets.setdefault(seg["song"], []).append(seg)

    indices = {song: 0 for song in song_buckets}

    while True:
        any_added = False

        for song, segs in song_buckets.items():
            idx = indices[song]
            if idx < len(segs):
                mix_order.append(segs[idx])
                indices[song] += 1
                any_added = True

        if not any_added:
            break

    return mix_order


# -----------------------------
# Local testing only
# -----------------------------
if __name__ == "__main__":
    print("Run step4 via app.py, not directly.")
