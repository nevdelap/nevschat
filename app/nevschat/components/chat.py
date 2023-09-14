# mypy: disable-error-code="attr-defined,name-defined"

import reflex as rx

from nevschat.state import DEFAULT_OTHER
from nevschat.state import OTHER
from nevschat.state import PromptResponse
from nevschat.state import State


def prompt_response_box(prompt_response: PromptResponse, index: int) -> rx.Component:
    return rx.box(
        rx.cond(  # type: ignore
            prompt_response.is_editing,
            rx.hstack(
                rx.debounce_input(
                    rx.text_area(
                        on_blur=State.cancel_control,
                        on_change=State.update_edited_prompt,  # type: ignore  # pylint: disable=no-value-for-parameter
                        on_key_down=State.handle_key_down,
                        on_key_up=State.handle_key_up,
                        width="100%",
                    ),
                    debounce_timeout=250,
                    value=State.edited_prompt,
                ),
                rx.button(
                    rx.icon(tag="close"),
                    _hover={"background_color": "#f8f8f8"},
                    background_color="white",
                    is_disabled=State.cannot_clear_or_send_edited_prompt,
                    on_click=lambda: State.clear_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                rx.button(
                    rx.icon(tag="arrow_right"),
                    _hover={"color": "white", "background_color": "green"},
                    background_color="green",
                    color="white",
                    is_disabled = State.cannot_clear_or_send_edited_prompt,
                    on_click=lambda: State.send_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                rx.button(
                    rx.icon(tag="close"),
                    _hover={"color": "white", "background_color": "darkred"},
                    background_color="darkred",
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
                    background_color="#f8f8f8",
                    border_radius="10px",
                    padding="0.5em 1em 0.5em 1em",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="edit"),
                    _hover={"color": "white", "background_color": "green"},
                    background_color="green",
                    color="white",
                    is_disabled=State.cannot_enter_new_prompt_or_edit,
                    is_loading=State.is_processing,
                    on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                ),
                rx.button(
                    rx.icon(tag="copy"),
                    _hover={"background_color": "#f8f8f8"},
                    background_color="white",
                    on_click=rx.set_clipboard(prompt_response.prompt),
                ),
                width="100%",
            ),
        ),
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.markdown(
                            prompt_response.response,
                        ),
                        width="100%",
                    ),
                    rx.button(
                        rx.icon(tag="copy"),
                        _hover={"background_color": "#f8f8f8"},
                        background_color="white",
                        on_click=rx.set_clipboard(prompt_response.response),
                    ),
                    width="100%",
                ),
                padding="0.5em 0em 0em 1.5em",
                width="100%",
            ),
            rx.center(
                rx.text(
                    prompt_response.model,
                    color="#aaa",
                    font_size="0.75em",
                    padding="0",
                    width="100%",
                ),
                margin="0 !important",
                padding="0 0 0.5em 0",
            ),
            width="100%",
        ),
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.wrap(
            rx.checkbox(
                "GPT4",
                color="#333",
                on_change=State.set_gpt_4,  # type: ignore
                value=State.gpt_4,
            ),
            rx.checkbox(
                "Terse",
                color="#333",
                on_change=State.set_terse,  # type: ignore
                value=State.terse,
            ),
            rx.hstack(
                rx.radio_group(
                    rx.hstack(
                        rx.foreach(
                            ["Normal", "Translate", "Other:"],
                            rx.radio,
                        ),
                        spacing="0.5em",
                    ),
                    color="#333",
                    default_value="Normal",
                    default_checked=True,
                    on_change=State.set_mode,
                ),
                rx.select(
                    sorted(OTHER.keys()),
                    default_value=DEFAULT_OTHER,
                    is_disabled=State.is_not_other,
                    on_change=State.set_other,
                    variant="unstyled",
                ),
            ),
        ),
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
                    is_disabled=State.cannot_enter_new_prompt_or_edit,
                    on_blur=State.cancel_control,
                    on_change=State.set_new_prompt,  # type: ignore  # pylint: disable=no-value-for-parameter
                    on_key_down=State.handle_key_down,
                    on_key_up=State.handle_key_up,
                    placeholder = "Ask something.",
                ),
                debounce_timeout=250,
                value=State.new_prompt,
            ),
            rx.button(
                rx.icon(tag="close"),
                _hover={"background_color": "#f8f8f8"},
                background_color="white",
                is_disabled=State.cannot_send_new_prompt,
                on_click=lambda: State.clear_new_prompt,  # type: ignore  # pylint: disable=no-value-for-parameter
            ),
            rx.button(
                rx.icon(tag="arrow_right"),
               _hover={"color": "white", "background_color": "green"},
                background_color="green",
                color="white",
                is_disabled=State.cannot_send_new_prompt,
                is_loading=State.is_processing,
                on_click=State.send,
            ),
            width="100%",
        ),
        width="100%",
    )
