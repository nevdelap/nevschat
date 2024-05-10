from nevschat.speakable import Speakable


class LearningAide(Speakable):

    model: str = ""
    system_instruction: str = ""
    prompt: str = ""
    contains_japanese: bool = False

    def clear(self) -> None:
        super().clear()
        self.model = ""
        self.system_instruction = ""
        self.prompt = ""
        self.contains_japanese: bool = False
