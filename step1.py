# step1.py
from pydub import AudioSegment
import os

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"


def process_uploaded_files():
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    if not os.path.exists(UPLOAD_FOLDER):
        return "Uploads folder not found"

    results = []

    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".mp3") or file.endswith(".wav"):
            input_path = os.path.join(UPLOAD_FOLDER, file)
            output_path = os.path.join(
                PROCESSED_FOLDER,
                os.path.splitext(file)[0] + ".wav"
            )

            audio = AudioSegment.from_file(input_path)
            audio = audio.set_frame_rate(44100).set_channels(2)
            audio.export(output_path, format="wav")

            results.append(output_path)

    return results
