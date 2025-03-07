import os
import time
from abc import ABC
from urllib.parse import urljoin

import requests
from rxconfig import config
from rxconfig import site_runtime_assets_url

import reflex as rx
from nevschat.helpers import Warnable
from nevschat.helpers import contains_non_japanese
from nevschat.helpers import get_default_voice
from nevschat.helpers import replace_punctuation_with_commas
from nevschat.helpers import strip_duplicate_sentences
from nevschat.helpers import strip_non_japanese_and_split_sentences
from nevschat.helpers import strip_sentences_without_kanji
from nevschat.helpers import strip_spaces_in_japanese
from nevschat.helpers import text_to_wav as tts_text_to_wav


class Speakable(rx.Base, ABC):  # type: ignore
    """
    Base class for things that can be spoken aloud with TTS.
    """

    pitch: float = 0
    speaking_rate: float = 1
    text: str = ''
    tts_in_progress = False
    tts_wav_url = ''
    voice: str = get_default_voice()

    def clear(self) -> None:
        self.pitch = 0
        self.speaking_rate = 1
        self.text = ''
        self.tts_in_progress = False
        self.tts_wav_url = ''
        self.voice = get_default_voice()

    def text_to_wav(self, warnable: Warnable) -> None:
        """
        For calling from asynchronous handlers so that the UI watching its state
        updates as this runs. Sets tts_in_progress = True while it is running,
        and sets it to False when it is complete and tts_wav_url is set.
        """
        # Set before calling text_to_wav and yield to allow UI update.
        assert self.tts_in_progress
        try:
            if self.text == '':  # pylint: disable=comparison-with-callable
                return
            try:
                # Android puts spaces in voice input where it shouldn't.
                text = strip_spaces_in_japanese(self.text)
                if contains_non_japanese(text):
                    text = strip_non_japanese_and_split_sentences(self.text)
                    text = strip_sentences_without_kanji(text)
                    text = replace_punctuation_with_commas(text)
                    text = strip_duplicate_sentences(text)
                if text == '':
                    text = '仮名、以外ではない。'
                print(f'Creating .wav for: {text}')
                tts_wav_filename = tts_text_to_wav(
                    text,
                    self.voice,
                    self.speaking_rate,
                    self.pitch,
                )
                self.tts_wav_url = os.path.join(
                    config.frontend_path, f'{tts_wav_filename[len("assets/") :]}'
                )
                full_tts_wav_url = urljoin(site_runtime_assets_url, self.tts_wav_url)
                print(f'Checking that {full_tts_wav_url} is being served...', end='')
                for _ in range(0, 10):
                    try:
                        response = requests.head(full_tts_wav_url, timeout=5.0)
                        if response.status_code >= 200 and response.status_code < 400:
                            print(' OK')
                            return
                    except Exception as ex:  # pylint: disable=broad-exception-caught
                        print(ex)
                        warnable.warning = str(ex)
                    time.sleep(0.25)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(ex)
                warnable.warning = str(ex)
            else:
                print(' NOT OK')
                warning = (
                    'Some problem prevented the audio from being available to play.'
                )
                print(warning)
                warnable.warning = warning
        finally:
            self.tts_in_progress = False
