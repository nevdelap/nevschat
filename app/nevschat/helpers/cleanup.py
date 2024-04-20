import glob
import os
import time


def delete_old_wave_assets() -> None:
    files = glob.glob("assets/tts_*.wav")
    current_time = time.time()
    age_seconds = 3600
    for file in files:
        file_mtime = os.path.getmtime(file)
        age = current_time - file_mtime
        if age > age_seconds:
            os.remove(file)
