import reflex as rx

from nevschat.state import State


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                rx.breadcrumb(
                    rx.breadcrumb_item(
                        rx.heading("Nev's GPTChat", size="sm"),
                    ),
                    rx.breadcrumb_item(
                        rx.text(State.current_chat, size="sm", font_weight="normal"),
                    ),
                ),
            ),
            rx.hstack(
                rx.button(
                    "+ New chat",
                    px="4",
                    py="2",
                    h="auto",
                    on_click=State.toggle_modal,
                ),
            ),
            justify="space-between",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        position="sticky",
        top="0",
        z_index="100",
    )
