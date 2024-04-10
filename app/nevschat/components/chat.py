# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.state import DEFAULT_SYSTEM_INSTRUCTION
from nevschat.state import SYSTEM_INSTRUCTIONS
from nevschat.state import PromptResponse
from nevschat.state import State

import reflex as rx


def prompt_response_box(prompt_response: PromptResponse, index: int) -> rx.Component:
    return rx.box(
        rx.cond(
            prompt_response.is_editing,
            rx.form(
                rx.hstack(
                    # rx.debounce_input(
                    rx.text_area(
                        enter_key_submit=True,
                        on_change=State.update_edited_prompt,
                        width="100%",
                        # ),
                        # debounce_timeout=250,
                        # value=State.edited_prompt,
                    ),
                    rx.button(
                        rx.icon(tag="eraser"),
                        color_scheme="red",
                        disabled=State.cannot_clear_or_send_edited_prompt,
                        on_click=lambda: State.clear_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                        margin_top="0.75em",
                    ),
                    rx.button(
                        rx.icon(tag="send-horizontal"),
                        color_scheme="grass",
                        disabled=State.cannot_clear_or_send_edited_prompt,
                        on_click=lambda: State.send_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                        margin_top="0.75em",
                        type="submit",
                    ),
                    rx.button(
                        rx.icon(tag="x"),
                        color_scheme="tomato",
                        on_click=lambda: State.cancel_edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                        margin_top="0.75em",
                    ),
                    width="100%",
                ),
                on_submit=lambda _form_data_unused: State.send_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                width="100%",
            ),
            rx.hstack(
                rx.box(
                    rx.markdown(prompt_response.prompt),
                    background_color="#f8f8f8",
                    border_radius="10px",
                    padding="0 1em 0 1em",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="square-pen"),
                    color_scheme="grass",
                    disabled=State.cannot_enter_new_prompt_or_edit,
                    is_loading=State.is_processing,
                    on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    margin_top="0.75em",
                ),
                rx.button(
                    rx.icon(tag="copy"),
                    color_scheme="gray",
                    on_click=rx.set_clipboard(prompt_response.prompt),
                    margin_top="0.75em",
                ),
                width="100%",
            ),
        ),
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.markdown(
                        prompt_response.response,
                        margin_left="1em",
                        width="100%",
                    ),
                    width="100%",
                ),
                rx.cond(
                    State.is_processing,
                    rx.button(
                        rx.icon(tag="x"),
                        color_scheme="tomato",
                        on_click=State.cancel_send,
                        margin_top="0.75em",
                    ),
                    None,
                ),
                rx.button(
                    rx.icon(tag="copy"),
                    color_scheme="gray",
                    on_click=rx.set_clipboard(prompt_response.response),
                    margin_top="0.75em",
                ),
                width="100%",
            ),
            rx.text(
                prompt_response.model,
                color="#aaa",
                font_size="0.5em",
                margin_bottom="0.5em",
                text_align="center",
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.hstack(
            rx.checkbox(
                "GPT4",
                checked=State.gpt_4,
                color="#333",
                on_change=State.set_gpt_4,
            ),
            rx.checkbox(
                "Terse",
                checked=State.terse,
                color="#333",
                on_change=State.set_terse,
            ),
            rx.hstack(
                rx.radio(
                    ["Normal", "Instruction:"],
                    color="#333",
                    direction="row",
                    spacing="2",
                    on_change=State.set_mode,
                    value=State.mode,
                ),
                rx.select(
                    list(SYSTEM_INSTRUCTIONS.keys()),
                    default_value=DEFAULT_SYSTEM_INSTRUCTION,
                    disabled=State.is_not_system_instruction,
                    on_change=State.set_system_instruction,
                    value=State.system_instruction,
                    variant="surface",
                ),
                align="center",
                direction="row",
                spacing="2",
                wrap="wrap",
            ),
            align="center",
            direction="row",
            spacing="2",
            wrap="wrap",
        ),
        rx.box(
            rx.foreach(
                State.prompts_responses,
                prompt_response_box,
            ),
            width="100%",
        ),
        rx.form(
            rx.hstack(
                # rx.debounce_input(
                rx.text_area(
                    disabled=State.cannot_enter_new_prompt_or_edit,
                    enter_key_submit=True,
                    on_change=State.set_new_prompt,
                    placeholder="Ask something.",
                    width="100%",
                    # ),
                    # debounce_timeout=250,
                    # value=State.new_prompt,
                ),
                rx.button(
                    rx.icon(tag="eraser"),
                    color_scheme="red",
                    disabled=State.cannot_send_new_prompt,
                    on_click=lambda: State.clear_new_prompt,
                    margin_top="0.75em",
                ),
                rx.button(
                    rx.icon(tag="send-horizontal"),
                    color_scheme="grass",
                    disabled=State.cannot_send_new_prompt,
                    is_loading=State.is_processing,
                    on_click=State.send,
                    margin_top="0.75em",
                    type="submit",
                ),
                width="100%",
            ),
            on_submit=lambda _form_data_unused: State.send(),  # type: ignore  # pylint: disable=no-value-for-parameter
            width="100%",
        ),
        width="100%",
    )
