# https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3

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


def text_to_wav(text: str, voice: int = 0) -> str:
    assert voice < len(VOICES)
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
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    filename = "/tmp/tts.wav"  # nosec
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    return filename
