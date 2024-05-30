import os
from typing import Final

import deepl

from nevschat.helpers import contains_japanese

_translator: Final = deepl.Translator(auth_key=os.environ['DEEPL_AUTH_KEY'])


ENGLISH: Final = 'EN-US'
FRENCH: Final = 'FR'
JAPANESE: Final = 'JA'


def get_translation(text: str, target_lang: str) -> str:
    """
    Return a translation for the given text.
    """
    if contains_japanese(text):
        print(f'Translating {text} to {target_lang}.')
        result = _translator.translate_text(text, target_lang=target_lang)
    else:
        print(f'Translating {text} to Japanese.')
        result = _translator.translate_text(text, target_lang=JAPANESE)
    assert isinstance(result, deepl.TextResult)
    translation = result.text
    print(f'Translated to {translation}.')
    return translation
