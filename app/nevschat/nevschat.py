# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = 23
TITLE = f"Nev's Awesome ChatGPT v{VERSION}"


def index() -> rx.Component:
    return rx.vstack(
        rx.heading(
            TITLE,
            text_align="left",
            width="100%",
        ),
        rx.text(
            f"Reflex version {rx.constants.Reflex.VERSION}.",
            color="#aaa",
            width="100%",
        ),
        chat(),
        rx.button(
            rx.icon(tag="x"),
            color_scheme="tomato",
            disabled=State.cannot_clear_chat,
            on_click=State.clear_chat,
        ),
        rx.cond(
            State.warning,
            # TODO: How to do an alert.
            rx.text("temp", width="100%"),
            # rx.alert(
            #     rx.alert_icon(),
            #     rx.alert_title(
            #         State.warning,
            #     ),
            #     border_radius="0.5em",
            #     status="warning",
            # ),
            None,
        ),
        padding="1em",
        width="100%",
    )


app = rx.App(theme=rx.theme(
        accent_color="teal",
        appearance="light",
        has_background=True,
        radius="large",
        scaling="110%",
    )
)
app.add_page(
    index,
    title=TITLE,
)
