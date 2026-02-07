# app.py
import streamlit as st
import os

from step1 import process_uploaded_files
from step2 import analyze_audio
from step3 import extract_segments
from step4 import create_mix_order
from step5 import generate_final_mix

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
# Upload songs
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload songs (mp3 or wav)",
    type=["mp3", "wav"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} song(s) uploaded!")

    for file in uploaded_files:
        file_path = os.path.join("uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

    if st.button("🎶 Generate DJ Mix"):
        with st.spinner("Processing... Please wait"):

            try:
                process_uploaded_files()
                analyze_audio()
                extract_segments()
                create_mix_order()
                generate_final_mix()

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
