from typing import Final

import requests
from bs4 import BeautifulSoup
from jamdict import Jamdict  # type: ignore

from .warnable import Warnable

_jam: Final = Jamdict()


def get_definition(text: str, warnable: Warnable) -> tuple[str, str]:
    """
    Return definitions for the given text, with exact matches first.
    """
    print(f'Looking up {text} in the dictionary.')
    try:
        response = requests.get(f'https://takoboto.jp/?q={text}', timeout=5)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a'):
            a.extract()
        results = soup.find_all('div', class_='ResultDiv')
        entries = [result.get_text(separator=' ') for result in results]
        definition = (
            ''.join(entry + '\n\n' for entry in entries)
            if len(entries) > 0
            else '何も見つからなかった。'
        )
        return (definition, 'takoboto')
    except Exception as ex:  # pylint: disable=broad-exception-caught
        warnable.warning = str(ex)
        # Fall back to jamdict.
        result = _jam.lookup(text)
        entries = [entry.text(True) for entry in result.entries]
        result = _jam.lookup(f'{text}%')
        entries += [
            text
            for entry in result.entries
            if (text := entry.text(True)) not in entries
        ]
        definition = (
            ''.join(entry + '\n\n' for entry in entries)
            if len(entries) > 0
            else '何も見つからなかった。'
        )
        return (definition, 'jamdict')
