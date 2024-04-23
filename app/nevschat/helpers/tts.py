# https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3

import hashlib
import os

import google.cloud.texttospeech as tts

VOICES = [
    # Female
    "ja-JP-Neural2-B",
    "ja-JP-Standard-A",
    "ja-JP-Standard-B",
    "ja-JP-Wavenet-A",
    "ja-JP-Wavenet-B",
    # Male
    "ja-JP-Neural2-C",
    "ja-JP-Neural2-D",
    "ja-JP-Standard-C",
    "ja-JP-Standard-D",
    "ja-JP-Wavenet-C",
    "ja-JP-Wavenet-D",
]


def text_to_wav(text: str, voice: int = 1) -> str:
    """
    Write a wave file into assets/wav, if it doesn't already exist.
    """
    assert voice < len(VOICES)
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
        name=VOICES[voice],
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
