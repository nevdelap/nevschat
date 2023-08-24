import reflex as rx

from nevschat.state import PromptResponse, State


def prompt_response_box(prompt_response: PromptResponse, index: int) -> rx.Component:
    return rx.box(
        rx.cond(
            prompt_response.is_editing,
            rx.hstack(
                rx.debounce_input(
                    rx.input(
                        width="100%",
                    ),
                    debounce_timeout=250,
                    value=prompt_response.prompt,
                ),
                rx.button(
                    rx.icon(tag="arrow_right"),
                    bg="green",
                    color="white",
                    on_click=lambda: State.send_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                rx.button(
                    rx.icon(tag="close"),
                    bg="red",
                    color="white",
                    on_click=lambda: State.cancel_edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                width="100%",
            ),
            rx.hstack(
                rx.box(
                    rx.markdown(
                        prompt_response.prompt,
                    ),
                    background_color="#fafafa",
                    border_radius="10px",
                    padding="0.5em 1em 0.5em 1em",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="edit"),
                    bg="green",
                    color="white",
                    is_disabled=State.is_editing,
                    on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                width="100%",
            ),
        ),
        rx.box(
            rx.markdown(
                prompt_response.response,
            ),
            padding="1em",
            padding_left="1.5em",
        ),
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(
            rx.foreach(
                State.prompts_responses,
                prompt_response_box,
            ),
            width="100%",
        ),
        rx.hstack(
            rx.debounce_input(
                rx.text_area(
                    is_disabled=State.cannot_enter_new_prompt,
                    on_change=State.set_next_prompt,
                    on_key_down=State.handle_key_down,  # type: ignore
                    on_key_up=State.handle_key_up,
                    placeholder = "Ask something.",
                ),
                debounce_timeout=250,
                value=State.next_prompt,
            ),
            rx.button(
                rx.icon(tag="arrow_right"),
                bg="green",
                color="white",
                is_disabled=State.cannot_send,
                is_loading=State.is_processing,
                on_click=State.send,
            ),
            width="100%",
        ),
        width="100%",
    )
