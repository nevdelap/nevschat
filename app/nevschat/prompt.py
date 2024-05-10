from nevschat.speakable import Speakable


class Prompt(Speakable):

    contains_japanese: bool = False

    def clear(self) -> None:
        super().clear()
        self.contains_japanese = False
