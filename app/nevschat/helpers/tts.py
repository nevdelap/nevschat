# https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3

import hashlib
import os
import random

import google.cloud.texttospeech as tts

USE_BEST_VOICES = True

VOICES = (
    [
        # Female
        "ja-JP-Neural2-B",
        # Male
        "ja-JP-Neural2-C",
        "ja-JP-Neural2-D",
    ]
    if USE_BEST_VOICES
    else [
        # Female
        "ja-JP-Standard-A",
        "ja-JP-Standard-B",
        # Male
        "ja-JP-Standard-C",
        "ja-JP-Standard-D",
    ]
)


def get_random_voice() -> str:
    return VOICES[random.randrange(0, len(VOICES))]  # nosec


def text_to_wav(text: str, voice: str = VOICES[0]) -> str:
    """
    Write a wave file into assets/wav, if it doesn't already exist.
    """
    assert voice in VOICES
    try:
        hash_ = hashlib.md5(text.encode(encoding="utf-8")).hexdigest()  # nosec
        tts_wav_filename = f"assets/wav/tts_{hash_}.wav"
        if os.path.isfile(tts_wav_filename):
            print("Skipping tts.")
            return tts_wav_filename
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(ex)

    print("Doing tts.")
    client = tts.TextToSpeechClient(
        client_options={
            "api_key": os.environ["GOOGLE_TTS_KEY"],
            "quota_project_id": "nevs-chat",
        }
    )
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code="ja-JP",
        name=voice,
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=0.9,
    )
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    with open(tts_wav_filename, "wb") as f:
        f.write(response.audio_content)
    print("Done tts.")
    return tts_wav_filename
