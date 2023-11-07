# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = 5


def index() -> rx.Component:
    return rx.vstack(
        rx.heading(
            f"Nev's Awesome ChatGPT v{VERSION}",
            text_align="left",
            size="lg",
            width="100%",
        ),
        chat(),
        rx.button(
            rx.icon(tag="close"),
            _hover={"background_color": "#f8f8f8"},
            background_color="white",
            is_disabled=State.cannot_clear_chat,
            on_click=State.clear_chat,
        ),
        rx.cond(
            State.warning,
            rx.alert(
                rx.alert_icon(),
                rx.alert_title(
                    State.warning,
                ),
                border_radius="0.5em",
                status="warning",
            ),
            None,
        ),
        padding="1em",
        width="100%",
    )


app = rx.App(state=State)
app.add_page(
    index,
    title="Nev's ChatGPT",
)
app.compile()
