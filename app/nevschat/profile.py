import random
import time

import reflex as rx

from nevschat.helpers import age_to_kanji
from nevschat.helpers import get_pitch
from nevschat.helpers import get_random_age
from nevschat.helpers import get_random_city
from nevschat.helpers import get_random_foods_and_drinks
from nevschat.helpers import get_random_hobbies
from nevschat.helpers import get_random_mood
from nevschat.helpers import get_random_name
from nevschat.helpers import get_random_profession
from nevschat.helpers import get_random_speaking_rate
from nevschat.helpers import get_random_voice
from nevschat.speakable import Speakable

random.seed(time.time())


def get_random_is_male() -> bool:
    return random.choice([True, False])  # nosec


class Profile(Speakable):

    male: bool = True
    age: int = 20
    name: str = ""
    city: str = ""
    profession: str = ""
    hobbies: str = ""
    foods_and_drinks: str = ""
    mood: str = ""

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.reset()

    def reset(self) -> None:
        super().reset()
        self.male = get_random_is_male()
        self.age = get_random_age()
        self.name = get_random_name(self.male)
        self.city = get_random_city()
        self.profession = get_random_profession(self.age)
        self.hobbies = get_random_hobbies(self.age)
        self.foods_and_drinks = get_random_foods_and_drinks()
        self.mood = get_random_mood()

    def _text(self) -> str:
        return (
            f"{self.name}、{age_to_kanji(self.age)}歳で、"
            f"{self.city}に住んでいます。{self.profession}で、"
            f"趣味は{self.hobbies}です。{self.foods_and_drinks}が好きです。"
            f"今私は{self.mood}"
        )
