# step4.py
def create_mix_order(all_songs_segments, top_segments_per_song=3, bpm_tolerance=6):
    """
    Create DJ mix order using BPM-aware + round-robin selection.
    Accepts output from step3.extract_segments()
    """

    if not all_songs_segments:
        return []

    # -----------------------------
    # Sort songs by tempo (BPM)
    # -----------------------------
    sorted_songs = sorted(
        all_songs_segments,
        key=lambda x: x["tempo"]
    )

    mix_order = []

    # -----------------------------
    # Group songs with similar BPM
    # -----------------------------
    bpm_groups = []
    current_group = [sorted_songs[0]]

    for song in sorted_songs[1:]:
        last_bpm = current_group[-1]["tempo"]

        if abs(song["tempo"] - last_bpm) <= bpm_tolerance:
            current_group.append(song)
        else:
            bpm_groups.append(current_group)
            current_group = [song]

    bpm_groups.append(current_group)

    # -----------------------------
    # Round-robin inside each BPM group
    # -----------------------------
    for group in bpm_groups:
        buckets = {}

        for song_data in group:
            song = song_data["song"]
            segments = sorted(
                song_data["segments"],
                key=lambda x: x["energy"],
                reverse=True
            )[:top_segments_per_song]

            buckets[song] = segments

        indices = {song: 0 for song in buckets}

        while True:
            added = False
            for song in buckets:
                idx = indices[song]
                if idx < len(buckets[song]):
                    seg = buckets[song][idx].copy()
                    seg["song"] = song
                    mix_order.append(seg)
                    indices[song] += 1
                    added = True

            if not added:
                break

    return mix_order


if __name__ == "__main__":
    print("Run step4 via app.py, not directly.")
