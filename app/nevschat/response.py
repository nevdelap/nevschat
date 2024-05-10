from nevschat.speakable import Speakable


class Response(Speakable):

    contains_japanese: bool = False
    model: str = ""

    def clear(self) -> None:
        super().clear()
        self.contains_japanese = False
        self.model = ""
