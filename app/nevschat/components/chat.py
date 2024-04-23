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
                    disabled=State.cannot_clear_or_chatgpt_with_edited_prompt,
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
                    disabled=State.cannot_clear_or_chatgpt_with_edited_prompt,
                    on_click=lambda: State.chatgpt_with_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
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
                        on_click=State.cancel_chatgpt,
                        margin_top="0.75em",
                    ),
                    None,
                ),
                rx.hstack(
                    rx.cond(
                        ~State.is_processing & prompt_response.is_japanese,
                        rx.button(
                            rx.icon(
                                tag="volume-2",
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme="blue",
                            disabled=prompt_response.has_tts,
                            margin_top="0.75em",
                            on_click=lambda: State.speak(  # pylint: disable=no-value-for-parameter
                                index, prompt_response.response
                            ),
                        ),
                        None,
                    ),
                    rx.button(
                        rx.icon(
                            tag="copy",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="gray",
                        margin_top="0.75em",
                        on_click=rx.set_clipboard(prompt_response.response),
                    ),
                ),
                width="100%",
            ),
            rx.cond(
                prompt_response.has_tts,
                rx.audio(
                    height="32px",
                    playing=True,
                    url=prompt_response.tts_wav_url,
                    width="100%",
                ),
                None,
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
                "簡潔な返答",
                checked=State.terse,
                color="#333",
                on_change=State.set_terse,
            ),
            rx.hstack(
                rx.radio(
                    ["通常モード", "システム指示:"],
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
            rx.checkbox(
                "日本語のオートスピーク",
                checked=State.auto_speak,
                color="#333",
                on_change=State.set_auto_speak,
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
                placeholder="何か質問はありますか？",
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
                disabled=State.cannot_chatgpt_with_new_prompt,
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
                disabled=State.cannot_chatgpt_with_new_prompt,
                is_loading=State.is_processing,
                on_click=State.chatgpt,
                margin_top="0.75em",
            ),
            width="100%",
        ),
        width="100%",
    )
