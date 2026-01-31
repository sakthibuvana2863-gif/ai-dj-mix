# step1.py
from pydub import AudioSegment
import os

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Loop over all uploaded files
for file in os.listdir(UPLOAD_FOLDER):
    if file.endswith(".mp3") or file.endswith(".wav"):
        input_path = os.path.join(UPLOAD_FOLDER, file)
        output_path = os.path.join(PROCESSED_FOLDER, os.path.splitext(file)[0] + ".wav")

        # Convert and normalize
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(44100).set_channels(2)
        audio.export(output_path, format="wav")

        print(f"✔ Processed: {output_path}")
