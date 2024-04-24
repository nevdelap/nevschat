import glob
import os
import time


def delete_old_wav_assets() -> None:
    files = glob.glob("assets/wav/tts_*.wav")
    current_time = time.time()
    age_seconds = 60 * 60 * 24
    for file in files:
        file_mtime = os.path.getmtime(file)
        age = current_time - file_mtime
        if age > age_seconds:
            os.remove(file)
