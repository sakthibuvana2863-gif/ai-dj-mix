# app.py
import streamlit as st
import os
import subprocess

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="AI DJ Mix Generator", layout="centered")

st.title("🎧 AI DJ Mix Generator")
st.write("Upload songs → Automatically generate a DJ mix")

# -----------------------------
# Create necessary folders
# -----------------------------
os.makedirs("uploads", exist_ok=True)     # user uploads go here
os.makedirs("processed", exist_ok=True)   # normalized WAV files
os.makedirs("output", exist_ok=True)      # final results

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

    # Save uploaded files to 'uploads/'
    for file in uploaded_files:
        file_path = os.path.join("uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

    # -----------------------------
    # Run pipeline
    # -----------------------------
    if st.button("🎶 Generate DJ Mix"):
        with st.spinner("Processing... This may take a few minutes"):

            try:
                # Step 1: Normalize uploaded songs
                subprocess.run(["python", "step1.py"], check=True)

                # Step 2: Analyze audio
                subprocess.run(["python", "step2.py"], check=True)

                # Step 3: Extract multiple segments
                subprocess.run(["python", "step3.py"], check=True)

                # Step 4: Create DJ mix order
                subprocess.run(["python", "step4.py"], check=True)

                # Step 5: Mix and generate final DJ track
                subprocess.run(["python", "step5.py"], check=True)

            except subprocess.CalledProcessError as e:
                st.error(f"❌ Pipeline failed: {e}")
            else:
                st.success("✅ DJ Mix generated successfully!")

                # -----------------------------
                # Download final mix
                # -----------------------------
                mix_path = "output/final_dj_mix.wav"
                if os.path.exists(mix_path):
                    with open(mix_path, "rb") as f:
                        st.download_button(
                            "⬇ Download DJ Mix",
                            f,
                            file_name="final_dj_mix.wav"
                        )
                else:
                    st.warning("⚠ Final DJ Mix not found. Check pipeline steps.")
