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
            rx.hstack(
                rx.text_area(
                    on_blur=State.cancel_control,
                    on_change=State.update_edited_prompt,
                    on_key_down=State.handle_key_down,
                    on_key_up=State.handle_key_up,
                    value=State.edited_prompt,
                    width="100%",
                ),
                rx.button(
                    rx.icon(
                        tag="eraser",
                        size=20,
                        stroke_width=1.5,
                    ),
                    color_scheme="red",
                    disabled=State.cannot_clear_or_send_edited_prompt,
                    on_click=lambda: State.clear_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    margin_top="0.75em",
                ),
                rx.button(
                    rx.icon(
                        tag="send-horizontal",
                        size=20,
                        stroke_width=1.5,
                    ),
                    color_scheme="grass",
                    disabled=State.cannot_clear_or_send_edited_prompt,
                    on_click=lambda: State.send_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    margin_top="0.75em",
                ),
                rx.button(
                    rx.icon(
                        tag="x",
                        size=20,
                        stroke_width=1.5,
                    ),
                    color_scheme="tomato",
                    on_click=lambda: State.cancel_edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    margin_top="0.75em",
                ),
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
                    rx.icon(
                        tag="square-pen",
                        size=20,
                        stroke_width=1.5,
                    ),
                    color_scheme="grass",
                    disabled=State.cannot_enter_new_prompt_or_edit,
                    is_loading=State.is_processing,
                    on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    margin_top="0.75em",
                ),
                rx.button(
                    rx.icon(
                        tag="copy",
                        size=20,
                        stroke_width=1.5,
                    ),
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
                        width="100%",
                    ),
                    margin_left="1em",
                    width="100%",
                ),
                rx.cond(
                    State.is_processing,
                    rx.button(
                        rx.icon(
                            tag="x",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="tomato",
                        on_click=State.cancel_send,
                        margin_top="0.75em",
                    ),
                    None,
                ),
                rx.vstack(
                    rx.button(
                        rx.icon(
                            tag="copy",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="gray",
                        on_click=rx.set_clipboard(prompt_response.response),
                        margin_top="0.75em",
                    ),
                    rx.cond(
                        prompt_response.is_japanese,
                        rx.vstack(
                            rx.button(
                                "スピーチ",
                                color_scheme="green",
                                on_click=lambda: State.speak(prompt_response.response),  # type: ignore  # pylint: disable=no-value-for-parameter
                                width="6em",
                            ),
                            rx.audio(
                                url="/tmp/tts.wav",
                            )
                        ),
                        None,
                    )
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
        rx.hstack(
            rx.text_area(
                disabled=State.cannot_enter_new_prompt_or_edit,
                on_blur=State.cancel_control,
                on_change=State.set_new_prompt,
                on_key_down=State.handle_key_down,
                on_key_up=State.handle_key_up,
                placeholder="Ask something.",
                value=State.new_prompt,
                width="100%",
            ),
            rx.button(
                rx.icon(
                    tag="eraser",
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme="red",
                disabled=State.cannot_send_new_prompt,
                on_click=lambda: State.clear_new_prompt,
                margin_top="0.75em",
            ),
            rx.button(
                rx.icon(
                    tag="send-horizontal",
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme="grass",
                disabled=State.cannot_send_new_prompt,
                is_loading=State.is_processing,
                on_click=State.send,
                margin_top="0.75em",
            ),
            width="100%",
        ),
        width="100%",
    )
