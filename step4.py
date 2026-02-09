# step4.py

def create_mix_order(all_songs_segments, top_segments_per_song=3):
    """
    Create DJ mix order using ENERGY CURVE method.
    Accepts output from step3.extract_segments()
    """
    if not all_songs_segments:
        return []

    # -----------------------------
    # Collect top segments from all songs
    # -----------------------------
    all_segments = []

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
            all_segments.append(seg_copy)

    if not all_segments:
        return []

    # -----------------------------
    # Sort segments by energy (low → high)
    # -----------------------------
    all_segments.sort(key=lambda x: x["energy"])

    n = len(all_segments)

    # -----------------------------
    # Energy Curve layout
    # -----------------------------
    intro = all_segments[: n // 4]                 # low energy
    buildup = all_segments[n // 4 : n // 2]        # medium
    peak = all_segments[n // 2 : (3 * n) // 4]     # high
    cooldown = all_segments[(3 * n) // 4 :]        # highest → drop later

    # Peak should feel intense → reverse it
    peak = list(reversed(peak))

    # -----------------------------
    # Final DJ mix order
    # -----------------------------
    mix_order = intro + buildup + peak + cooldown

    return mix_order


# -----------------------------
# Local testing only
# -----------------------------
if __name__ == "__main__":
    print("Run step4 via app.py, not directly.")
