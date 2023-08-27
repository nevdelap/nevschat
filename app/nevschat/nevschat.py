import reflex as rx

from nevschat.components import chat
from nevschat.state import State


def index() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Nev's ChatGPT",
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
        padding="1em",
        width="100%",
    )


app = rx.App(state=State)
app.add_page(index)
app.compile()
