# https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3

import hashlib
import os
import random
import time

import google.cloud.texttospeech as tts

random.seed(time.time())


def get_default_voice() -> str:
    return 'ja-JP-Neural2-C'


def get_random_voice(male: bool) -> str:
    if male:
        return random.choice(
            [  # nosec
                'ja-JP-Neural2-C',
                'ja-JP-Neural2-D',
            ]
        )
    return 'ja-JP-Neural2-B'  # nosec


def text_to_wav(text: str, voice: str, speaking_rate: float, pitch: float) -> str:
    """
    Write a wave file into assets/wav, if it doesn't already exist.
    """
    try:
        hash_ = hashlib.md5(text.encode(encoding='utf-8')).hexdigest()  # nosec
        tts_wav_filename = f'assets/wav/tts_{voice}_{speaking_rate}_{pitch}_{hash_}.wav'
        if os.path.isfile(tts_wav_filename):
            print('Skipping tts.')
            return tts_wav_filename
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(ex)

    print('Doing tts.')
    client = tts.TextToSpeechClient(
        client_options={
            'api_key': os.environ['GOOGLE_TTS_KEY'],
            'quota_project_id': 'nevs-chat',
        }
    )
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code='ja-JP',
        name=voice,
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    with open(tts_wav_filename, 'wb') as f:
        f.write(response.audio_content)
    print('Done tts.')
    return tts_wav_filename
