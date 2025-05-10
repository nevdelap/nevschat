# mypy: disable-error-code="attr-defined,name-defined"

# from __future__ import annotations

from typing import Any

import reflex as rx
from reflex.components.component import NoSSRComponent
from reflex.vars import Var

assert not hasattr(rx.constants.EventTriggers, 'ON_ENDED'), (
    "It looks like this mightn't be needed now."
)


class MyAudio(NoSSRComponent):
    """
    Duplicated from Reflex's audio.py until it supports the ended event. It is
    not exposed in the interface of the reflex.components.audio module, so it
    cannot be used from there without modifying Reflex, which I might do, but
    not now.
    """

    library = 'react-player@2.12.0'

    tag = 'ReactPlayer'

    is_default = True

    # The url of a video or song to play
    url: Var[str]

    # Set to true or false to pause or play the media
    playing: Var[bool]

    # Set to true or false to loop the media
    loop: Var[bool]

    # Set to true or false to display native player controls.
    controls: Var[bool] = Var.create(True)

    # Set to true to show just the video thumbnail, which loads the full player on click
    light: Var[bool]

    # Set the volume of the player, between 0 and 1
    volume: Var[float]

    # Mutes the player
    muted: Var[bool]

    # Set the width of the player: ex:640px
    width: Var[str]

    # Set the height of the player: ex:640px
    height: Var[str]

    def get_event_triggers(self) -> dict[str, Any]:
        return {'on_pause': lambda e0: [e0]}


my_audio = MyAudio.create
