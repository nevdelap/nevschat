import re
from typing import Final

import requests
from bs4 import BeautifulSoup
from jamdict import Jamdict  # type: ignore

from .japanese_text import contains_japanese

_jam: Final = Jamdict()


def get_definition(text: str) -> tuple[str, str]:
    """
    Return definitions for the given text, with exact matches from jamdict
    first, otherwise try takoboto.
    """
    if not contains_japanese(text):
        return ('テキストは日本語ではない。', '')

    # Look for an exact match in jamdict.
    print(f'Looking up {text} in jamdict.')
    result = _jam.lookup(text)
    if len(result.entries) > 0:
        entries = [_clean_spaces(entry.text(True)) for entry in result.entries]
        definition = ''.join(entry + '\n\n' for entry in entries)
        # jmdict definitions containing long series of words separated by
        # slashes don't break in a markdown component.
        definition = definition.replace('/', ', ')
        return (definition, 'jamdict')

    # Only if no match is found use Takoboto.
    print(f'Looking up {text} in takoboto.')
    response = requests.get(f'https://takoboto.jp/?q={text}', timeout=5)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a'):
        a.extract()
    results = soup.find_all('div', class_='ResultDiv')
    entries = [result.get_text(separator=' ') for result in results]
    definition = (
        ''.join(_clean_spaces(entry) + '\n\n' for entry in entries)
        if len(entries) > 0
        else '何も見つからなかった。'
    )
    # The separator causes there to be extra spaces. Tidy some up.
    definition = definition.replace(' ,', ',')
    return (definition, 'takoboto')


def get_kanji(text: str) -> tuple[str, str]:
    """
    Return kanji for the given text, from jamdict.
    """
    if not contains_japanese(text):
        return ('テキストは日本語ではない。', '')

    # Look for an exact match in jamdict.
    print(f'Looking up {text} in jamdict.')
    result = _jam.lookup(text)
    if len(result.chars) > 0:
        entries = [
            f'{char} - {', '.join(char.meanings(english_only=True))}'
            for char in result.chars
            if str(char) in text
        ]
        kanji = ''.join(entry + '\n\n' for entry in entries)
    else:
        kanji = '何も見つからなかった。'
    return (kanji, 'jamdict')


def _clean_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()
