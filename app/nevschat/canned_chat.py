from nevschat.helpers import get_default_voice
from nevschat.prompt import Prompt
from nevschat.prompt_response import PromptResponse
from nevschat.response import Response


def get_canned_chat() -> list[PromptResponse]:
    return [
        PromptResponse(
            prompt=Prompt(
                contains_japanese=True,
                pitch=0,
                speaking_rate=1,
                text='そうですか？',
                tts_wav_url=(
                    'wav/tts_ja-JP-Neural2-B_1.0_0.0_'
                    '3a26eb6e7ff37e88b995d6bbe579cfa1.wav'
                ),
                voice=get_default_voice(),
            ),
            response=Response(
                contains_japanese=True,
                model='gpt-canned',
                pitch=0,
                speaking_rate=1,
                text='はい、そうです。',
                tts_wav_url=(
                    'wav/tts_ja-JP-Neural2-B_1.0_0.0_'
                    'f01aa1dd97e1bc6798f739b4ab06094a.wav'
                ),
                voice=get_default_voice(),
            ),
            editing=False,
        ),
        PromptResponse(
            prompt=Prompt(
                contains_japanese=True,
                pitch=0,
                speaking_rate=1,
                text='いいです？',
                tts_wav_url=(
                    'wav/tts_ja-JP-Neural2-B_1.0_0.0_'
                    '4ff62a3d772146da7c906eaa2099fbe7.wav'
                ),
                voice=get_default_voice(),
            ),
            response=Response(
                contains_japanese=True,
                model='gpt-canned',
                pitch=0,
                speaking_rate=1,
                text='はい、いいですよ！',
                tts_wav_url=(
                    'wav/tts_ja-JP-Neural2-B_1.0_0.0_'
                    'ccba5ccc5754fca6737a099281019854.wav'
                ),
                voice=get_default_voice(),
            ),
            editing=False,
        ),
    ]
