from typing import Final

from jamdict import Jamdict  # type: ignore

_jam: Final = Jamdict()


def get_definition(text: str) -> str | None:
    result = _jam.lookup(f'{text}%')
    if len(result.entries) > 0:
        return ''.join(entry.text(True) + '\n' for entry in result.entries)
    return 'Nothing found.'
