# app.py
import shutil
import streamlit as st
import os

from step1 import process_uploaded_files
from step2 import analyze_audio
from step3 import extract_segments
from step4 import create_mix_order
from step5 import generate_final_mix

# -----------------------------
# FFprobe check
# -----------------------------
if shutil.which("ffprobe") is None:
    st.error(
        "ffprobe not found! Make sure 'ffmpeg' is included in packages.txt and redeploy."
    )

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="AI DJ Mix Generator", layout="centered")
st.title("🎧 AI DJ Mix Generator")
st.write("Upload songs → Automatically generate a DJ mix")

# -----------------------------
# Create necessary folders
# -----------------------------
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

# -----------------------------
# Initialize session state
# -----------------------------
if "uploaded_songs" not in st.session_state:
    st.session_state.uploaded_songs = []

# -----------------------------
# Clear all uploaded songs button
# -----------------------------
# -----------------------------
# Clear all uploaded songs button (FIXED)
# -----------------------------
if st.button("🗑 Clear All Songs"):
    st.session_state.uploaded_songs = []

    # Clear uploads, processed, and output folders
    for folder in ["uploads", "processed", "output"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    st.success("All uploaded songs and cached files have been cleared!")


# -----------------------------
# Upload songs
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload songs (mp3 or wav)",
    type=["mp3", "wav"],
    accept_multiple_files=True
)

if uploaded_files:
    # Replace old uploads with new ones
    st.session_state.uploaded_songs = uploaded_files
    st.success(f"{len(uploaded_files)} song(s) uploaded!")

    # Save files to "uploads" folder
    for file in st.session_state.uploaded_songs:
        file_path = os.path.join("uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

# -----------------------------
# Display current uploaded songs
# -----------------------------
if st.session_state.uploaded_songs:
    st.subheader("Current Songs for Mixing:")
    for f in st.session_state.uploaded_songs:
        st.write(f.name)

# -----------------------------
# Generate DJ Mix
# -----------------------------
if st.button("🎶 Generate DJ Mix"):
    if not st.session_state.uploaded_songs:
        st.warning("Please upload songs first!")
    else:
        with st.spinner("Processing... Please wait"):
            try:
                # STEP 1
                processed_files = process_uploaded_files()
                if not processed_files:
                    st.error("No files were processed in Step 1")
                    st.stop()

                # STEP 2
                analysis = analyze_audio()
                if not analysis:
                    st.error("Audio analysis failed in Step 2")
                    st.stop()

                # STEP 3
                segments = extract_segments(analysis)
                if not segments:
                    st.error("Segment extraction failed in Step 3")
                    st.stop()

                # STEP 4
                mix_order = create_mix_order(segments)
                if not mix_order:
                    st.error("Mix ordering failed in Step 4")
                    st.stop()

                # STEP 5
                generate_final_mix(mix_order)

            except Exception as e:
                st.error(f"❌ Pipeline failed: {e}")

            else:
                st.success("✅ DJ Mix generated successfully!")

                mix_path = "output/final_dj_mix.wav"
                if os.path.exists(mix_path):
                    with open(mix_path, "rb") as f:
                        st.download_button(
                            "⬇ Download DJ Mix",
                            f,
                            file_name="final_dj_mix.wav"
                        )
                else:
                    st.warning("⚠ Final DJ Mix not found.")

