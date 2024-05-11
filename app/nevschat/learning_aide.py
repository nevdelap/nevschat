from nevschat.speakable import Speakable


class LearningAide(Speakable):
    contains_japanese: bool = False
    model: str = ''
    prompt: str = ''
    system_instruction: str = ''

    def clear(self) -> None:
        super().clear()
        self.contains_japanese: bool = False
        self.model = ''
        self.prompt = ''
        self.system_instruction = ''
