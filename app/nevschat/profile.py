import random
import time
from typing import Any

from nevschat.helpers import age_to_kanji
from nevschat.helpers import get_pitch
from nevschat.helpers import get_random_age
from nevschat.helpers import get_random_city
from nevschat.helpers import get_random_foods_and_drinks
from nevschat.helpers import get_random_hobbies
from nevschat.helpers import get_random_mood
from nevschat.helpers import get_random_name
from nevschat.helpers import get_random_personal_feature
from nevschat.helpers import get_random_profession
from nevschat.helpers import get_random_speaking_rate
from nevschat.helpers import get_random_voice
from nevschat.speakable import Speakable

random.seed(time.time())


class Profile(Speakable):
    canned: bool = False
    male: bool = True

    def __init__(self, canned: bool = False, **data: Any) -> None:
        super().__init__(**data)
        self.canned = canned
        self.clear()

    def clear(self) -> None:
        super().clear()

        if not self.canned:
            self.male = random.choice([True, False])  # nosec

            age = get_random_age()
            name = get_random_name(self.male)
            city = get_random_city()
            profession = get_random_profession(age)
            hobbies = get_random_hobbies(age)
            foods_and_drinks = get_random_foods_and_drinks()
            personal_feature = get_random_personal_feature(age)
            mood = get_random_mood()

            self.pitch = get_pitch(self.male, age)
            self.speaking_rate = get_random_speaking_rate()
            self.text = (
                f'私は{name}、'
                f'{age_to_kanji(age)}歳で、'
                f'{city}に住んでいます。'
                f'{profession}です。'
                f'趣味は{hobbies}です。'
                f'{foods_and_drinks}が好きです。'
                f'私は{personal_feature}'
                f'今、{mood}'
            )
            self.voice = get_random_voice(self.male)
        else:
            self.male = True
            self.text = (
                '私は前川勝、五十三歳で、大阪に住んでいます。農家です。趣味はパズルを'
                '解くとバレーボールです。ドーナツやあたたかい水が好きです。'
                '私は消化不良がよくあります。今、失望しています。'
            )
