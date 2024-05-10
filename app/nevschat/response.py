from nevschat.speakable import Speakable


class Response(Speakable):

    model: str = ""
    contains_japanese: bool = False

    def clear(self) -> None:
        super().clear()
        self.model = ""
        self.contains_japanese = False
