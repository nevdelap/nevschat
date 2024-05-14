import os
from typing import Final

import deepl

from nevschat.helpers import contains_japanese

_translator: Final = deepl.Translator(auth_key=os.environ['DEEPL_AUTH_KEY'])


def get_translation(text: str) -> str | None:
    """
    Return a translation for the given text.
    """
    if contains_japanese(text):
        print(f'Translating {text} to English.')
        result = _translator.translate_text(text, target_lang='EN-US')
    else:
        print(f'Translating {text} to Japanese.')
        result = _translator.translate_text(text, target_lang='JA')
    assert isinstance(result, deepl.TextResult)
    return result.text
