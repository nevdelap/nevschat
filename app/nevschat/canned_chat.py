from nevschat.helpers import get_default_voice
from nevschat.prompt import Prompt
from nevschat.prompt_response import PromptResponse
from nevschat.response import Response


def get_canned_chat() -> list[PromptResponse]:
    return [
        PromptResponse(
            prompt=Prompt(
                pitch=0,
                text='そうですか？',
                speaking_rate=1,
                voice=get_default_voice(),
                contains_japanese=True,
            ),
            response=Response(
                model='gpt-canned',
                pitch=0,
                speaking_rate=1,
                text='はい、そうです。',
                voice=get_default_voice(),
                contains_japanese=True,
            ),
            editing=False,
        ),
        PromptResponse(
            prompt=Prompt(
                pitch=0,
                text='いいです？',
                speaking_rate=1,
                voice=get_default_voice(),
                contains_japanese=True,
            ),
            response=Response(
                model='gpt-canned',
                pitch=0,
                speaking_rate=1,
                text='はい、いいですよ！',
                voice=get_default_voice(),
                contains_japanese=True,
            ),
            editing=False,
        ),
    ]
