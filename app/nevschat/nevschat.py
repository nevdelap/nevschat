# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = "0.0.91"
TITLE = f"ネヴの素晴らしいチャットジーピーティー v{VERSION}"


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(TITLE),
            rx.text(
                f"リフレックス v{rx.constants.Reflex.VERSION}",
                color="rgba(0, 0, 0, 0.4)",
            ),
            chat(),
            rx.button(
                rx.icon(
                    tag="x",
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme="tomato",
                disabled=State.cannot_clear_chat,
                on_click=State.clear_chat,
            ),
            rx.cond(
                State.warning,
                rx.callout(
                    State.warning,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
                None,
            ),
            max_width="800px",
            spacing="2",
            width="100%",
        ),
        align="center",
        direction="column",
        justify="start",
        margin="2em 1em 1em 1em",
    )


app = rx.App(
    theme=rx.theme(
        accent_color="bronze",
        appearance="light",
        has_background=True,
        radius="medium",
        scaling="100%",
    )
)
app.add_page(
    index,
    title=TITLE,
)
