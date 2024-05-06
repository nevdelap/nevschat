import random
import time

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

import reflex as rx

random.seed(time.time())


def get_random_is_male() -> bool:
    return random.choice([True, False])  # nosec


class Profile(rx.Base):  # type: ignore

    male = get_random_is_male()
    age = get_random_age()
    name = get_random_name(male)
    city = get_random_city()
    profession = get_random_profession(age)
    hobbies = get_random_hobbies(age)
    foods_and_drinks = get_random_foods_and_drinks()
    mood = get_random_mood()
    pitch = get_pitch(male, age)
    speaking_rate = get_random_speaking_rate()
    voice = get_random_voice(male)
    # Set by tts.
    tts_in_progress = False
    tts_wav_url = ""
    has_tts = False

    def new(self) -> None:
        self.male = get_random_is_male()
        self.age = get_random_age()
        self.name = get_random_name(self.male)
        self.city = get_random_city()
        self.profession = get_random_profession(self.age)
        self.hobbies = get_random_hobbies(self.age)
        self.foods_and_drinks = get_random_foods_and_drinks()
        self.mood = get_random_mood()
        self.pitch = get_pitch(self.male, self.age)
        self.speaking_rate = get_random_speaking_rate()
        self.voice = get_random_voice(self.male)
        self.tts_in_progress = False
        self.tts_wav_url = ""
        self.has_tts = False

    def render(self, pronoun: str) -> str:
        return (
            f"{pronoun}は{self.name}、{age_to_kanji(self.age)}歳で、"
            f"{self.city}に住んでいます。{self.profession}で、"
            f"趣味は{self.hobbies}です。{self.foods_and_drinks}が好きです。"
            f"今私は{self.mood}"
        )