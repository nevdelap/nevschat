"""The main Chat app."""

import reflex as rx

from nevschat.components import chat, modal, navbar, sidebar
from nevschat.state import State


def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
