from nevschat.speakable import Speakable


class LearningAide(Speakable):
    expects_japanese: bool = True
    contains_japanese: bool = False
    model: str = ''
    prompt: str = ''
    system_instruction: str = ''
    target_lang: str = ''

    def clear(self) -> None:
        super().clear()
        self.contains_japanese: bool = False
        self.model = ''
        self.prompt = ''
        self.system_instruction = ''
        self.target_lang = ''
