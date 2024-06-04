from nevschat.speakable import Speakable


class Prompt(Speakable):
    contains_japanese: bool = False
    contains_non_japanese: bool = False

    def clear(self) -> None:
        super().clear()
        self.contains_japanese = False
        self.contains_non_japanese = False
