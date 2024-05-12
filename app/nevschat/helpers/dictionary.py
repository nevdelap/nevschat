from typing import Final

from jamdict import Jamdict  # type: ignore

_jam: Final = Jamdict()


def get_definition(text: str) -> str | None:
    """
    Return definitions for the given text, with exact matches first.
    """
    result = _jam.lookup(text)
    entries = [entry.text(True) for entry in result.entries]
    result = _jam.lookup(f'{text}%')
    entries += [
        text for entry in result.entries if (text := entry.text(True)) not in entries
    ]
    if len(entries) == 0:
        return '何も見つからなかった。'
    return ''.join(entry + '\n\n' for entry in entries)
