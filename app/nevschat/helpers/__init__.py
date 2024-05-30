from .dictionary import get_definition
from .dictionary import get_kanji
from .japanese_text import age_to_kanji
from .japanese_text import contains_japanese
from .japanese_text import contains_kanji
from .japanese_text import strip_non_japanese_and_split_sentences
from .japanese_text import strip_spaces_in_japanese
from .random_things import get_pitch
from .random_things import get_random_age
from .random_things import get_random_city
from .random_things import get_random_foods_and_drinks
from .random_things import get_random_hobbies
from .random_things import get_random_mood
from .random_things import get_random_name
from .random_things import get_random_personal_feature
from .random_things import get_random_profession
from .random_things import get_random_speaking_rate
from .translation import ENGLISH
from .translation import FRENCH
from .translation import get_translation
from .tts import get_default_voice
from .tts import get_random_voice
from .tts import text_to_wav
from .warnable import Warnable

__all__ = [
    'ENGLISH',
    'FRENCH',
    'age_to_kanji',
    'contains_japanese',
    'contains_kanji',
    'get_definition',
    'get_kanji',
    'get_pitch',
    'get_random_age',
    'get_random_city',
    'get_random_foods_and_drinks',
    'get_random_hobbies',
    'get_random_mood',
    'get_random_name',
    'get_random_personal_feature',
    'get_random_profession',
    'get_random_speaking_rate',
    'get_default_voice',
    'get_random_voice',
    'get_translation',
    'strip_non_japanese_and_split_sentences',
    'strip_spaces_in_japanese',
    'text_to_wav',
    'Warnable',
]
