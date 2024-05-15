import reflex as rx
from nevschat.prompt import Prompt
from nevschat.response import Response


class PromptResponse(rx.Base):  # type: ignore
    prompt: Prompt = Prompt()
    response: Response = Response()
    editing: bool
