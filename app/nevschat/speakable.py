import os
import time
from abc import ABC
from urllib.parse import urljoin

import requests
from nevschat.helpers import Warnable
from nevschat.helpers import delete_old_wav_assets
from nevschat.helpers import get_default_voice
from nevschat.helpers import text_to_wav as tts_text_to_wav
from rxconfig import config
from rxconfig import site_runtime_assets_url

import reflex as rx


class Speakable(rx.Base, ABC):  # type: ignore
    """
    Base class for things that can be spoken aloud with TTS.
    """

    pitch: float = 0
    speaking_rate: float = 1
    text: str = ""
    tts_in_progress = False
    tts_wav_url = ""
    voice: str = get_default_voice()

    def clear(self) -> None:
        self.pitch = 0
        self.speaking_rate = 1
        self.text = ""
        self.tts_in_progress = False
        self.tts_wav_url = ""
        self.voice = get_default_voice()

    def text_to_wav(self, warnable: Warnable) -> None:
        """
        For calling from asynchronous handlers so that the UI watching its state
        updates as this runs. Sets tts_in_progress = True while it is running,
        and sets it to False when it is complete and tts_wav_url is set.
        """
        if self.text == "":  # pylint: disable=comparison-with-callable
            return
        try:
            print(f"Creating .wav for: {self.text}")
            self.tts_in_progress = True
            try:
                tts_wav_filename = tts_text_to_wav(
                    self.text,
                    self.voice,
                    self.speaking_rate,
                    self.pitch,
                )
                # Take advantage of a moment for the Nginx to make the wav available
                # by doing some housekeeping.
                delete_old_wav_assets()
                self.tts_wav_url = os.path.join(
                    config.frontend_path, f"{tts_wav_filename[len('assets/'):]}"
                )
                full_tts_wav_url = urljoin(site_runtime_assets_url, self.tts_wav_url)
                print(f"Checking that {full_tts_wav_url} is being served...", end="")
                for _ in range(0, 10):
                    try:
                        response = requests.head(full_tts_wav_url, timeout=10.0)
                        if response.status_code >= 200 and response.status_code < 400:
                            print(" OK")
                            return
                    except Exception as ex:  # pylint: disable=broad-exception-caught
                        print(ex)
                        warnable.warning = str(ex)
                    time.sleep(0.25)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(ex)
                warnable.warning = str(ex)
            else:
                print(" NOT OK")
                warning = (
                    "Some problem prevented the audio from being available to play."
                )
                print(warning)
                warnable.warning = warning
        finally:
            self.tts_in_progress = False
