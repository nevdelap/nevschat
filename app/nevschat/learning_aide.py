import reflex as rx

from nevschat.helpers import contains_japanese
from nevschat.speakable import Speakable


class LearningAide(Speakable):

    model: str = ""
    system_instruction: str = ""
    prompt: str = ""
    response: str = ""

    @rx.var
    def has_response(self) -> bool:
        return self.response != ""

    @rx.var
    def response_contains_japanese(self) -> bool:
        return contains_japanese(self.response)

    def reset(self) -> None:
        super().reset()
        self.model = ""
        self.system_instruction = ""
        self.prompt = ""
        self.response = ""

    def _text(self) -> str:
        return response
