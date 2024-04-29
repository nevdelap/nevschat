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
                    border_color="#C2A499",
                    border_style="solid",
                    border_width="3px",
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
                    color_scheme="jade",
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
                    rx.markdown(
                        prompt_response.prompt,
                        width="100%",
                    ),
                    background_color="#ffefd6",
                    border_color="#c2a499",
                    border_style="solid",
                    border_width="3px",
                    padding="0 1em 0 1em",
                    width="100%",
                ),
                rx.button(
                    rx.icon(
                        tag="square-pen",
                        size=20,
                        stroke_width=1.5,
                    ),
                    color_scheme="jade",
                    disabled=State.cannot_enter_new_prompt_or_edit,
                    is_loading=State.processing,
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
                rx.vstack(
                    rx.cond(
                        ~State.using_profile  # pylint: disable=invalid-unary-operand-type
                        | State.male,
                        rx.box(
                            rx.markdown(
                                prompt_response.response,
                                width="100%",
                            ),
                            background_color="#e1f6fd",
                            border_color="#60b3d7",
                            border_style="solid",
                            border_width="3px",
                            padding="0 1em 0 1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.markdown(
                                prompt_response.response,
                                width="100%",
                            ),
                            background_color="#fee9f5",
                            border_color="#dd93c2",
                            border_radius="10px",
                            border_style="solid",
                            border_width="3px",
                            padding="0 1em 0 1em",
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        prompt_response.tts_in_progress,
                        rx.center(
                            rx.chakra.spinner(
                                color="#888",
                                margin_top="0.5em",
                                size="md",
                            ),
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        prompt_response.has_tts,
                        rx.audio(
                            height="32px",
                            margin_top="0.5em",
                            playing=True,
                            url=prompt_response.tts_wav_url,
                            width="100%",
                        ),
                    ),
                    rx.flex(
                        rx.spacer(
                            width="100%",
                        ),
                        rx.text(prompt_response.model),
                        rx.cond(
                            prompt_response.has_tts,
                            rx.text(prompt_response.voice),
                        ),
                        color="#aaa",
                        font_size="0.4em",
                        margin_bottom="0.75em",
                        margin_top="-0.5em",
                        padding_right="1em",
                        width="100%",
                    ),
                    width="100%",
                ),
                rx.cond(
                    State.processing,
                    rx.button(
                        rx.icon(
                            tag="x",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="tomato",
                        margin_top="0.75em",
                        on_click=State.cancel_chatgpt,
                    ),
                ),
                rx.hstack(
                    rx.cond(
                        ~State.processing & prompt_response.contains_japanese,
                        rx.button(
                            rx.icon(
                                tag="volume-2",
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme="blue",
                            disabled=(
                                prompt_response.tts_in_progress
                                | prompt_response.has_tts
                            ),
                            on_click=lambda: State.speak(  # pylint: disable=no-value-for-parameter
                                index,
                                prompt_response.response,
                            ),
                        ),
                    ),
                    rx.button(
                        rx.icon(
                            tag="copy",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="gray",
                        on_click=rx.set_clipboard(prompt_response.response),
                    ),
                    margin_top="0.75em",
                ),
                margin_top="0.5em",
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.flex(
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
            rx.select(
                list(SYSTEM_INSTRUCTIONS.keys()),
                default_value=DEFAULT_SYSTEM_INSTRUCTION,
                on_change=State.set_system_instruction,
                value=State.system_instruction,
                variant="surface",
            ),
            rx.checkbox(
                "日本語のオートスピーク",
                checked=State.auto_speak,
                color="#333",
                on_change=State.set_auto_speak,
            ),
            align="center",
            spacing="2",
            width="100%",
            wrap="wrap",
        ),
        rx.cond(
            State.using_profile,
            rx.hstack(
                rx.vstack(
                    rx.cond(
                        ~State.using_profile  # pylint: disable=invalid-unary-operand-type
                        | State.male,
                        rx.box(
                            rx.markdown(
                                State.who_am_i,
                                width="100%",
                            ),
                            background_color="#e1f6fd",
                            border_color="#60b3d7",
                            border_style="solid",
                            border_width="3px",
                            padding="0 1em 0 1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.markdown(
                                State.who_am_i,
                                width="100%",
                            ),
                            background_color="#fee9f5",
                            border_color="#dd93c2",
                            border_radius="10px",
                            border_style="solid",
                            border_width="3px",
                            padding="0 1em 0 1em",
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        State.profile_tts_in_progress,
                        rx.center(
                            rx.chakra.spinner(
                                color="#888",
                                margin_top="0.5em",
                                size="md",
                            ),
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        State.profile_has_tts,
                        rx.audio(
                            height="32px",
                            # margin_top="0.5em",
                            playing=True,
                            url=State.profile_tts_wav_url,
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        State.profile_has_tts,
                        rx.flex(
                            rx.spacer(
                                width="100%",
                            ),
                            rx.text(State.profile_voice),
                            color="#aaa",
                            font_size="0.4em",
                            margin_top="-0.5em",
                            padding_right="1em",
                            width="100%",
                        ),
                    ),
                ),
                rx.vstack(
                    rx.button(
                        rx.icon(
                            tag="refresh-cw",
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme="jade",
                        on_click=lambda: State.change_profile,
                        margin_top="0.75em",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.icon(
                                tag="volume-2",
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme="blue",
                            disabled=(
                                State.profile_tts_in_progress | State.profile_has_tts
                            ),
                            on_click=lambda: State.speak(  # pylint: disable=no-value-for-parameter
                                -1,
                                State.who_am_i,
                            ),
                        ),
                        rx.button(
                            rx.icon(
                                tag="copy",
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme="gray",
                            on_click=rx.set_clipboard(
                                State.who_am_i,
                            ),
                        ),
                        width="100%",
                        spacing="2",
                    ),
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
        rx.flex(
            rx.text_area(
                border_color="#C2A499",
                border_style="solid",
                border_width="3px",
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
            ),
            rx.button(
                rx.icon(
                    tag="send-horizontal",
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme="jade",
                disabled=State.cannot_chatgpt_with_new_prompt,
                is_loading=State.processing,
                on_click=State.chatgpt,
            ),
            align="center",
            margin_top="-0.25em",
            spacing="2",
            width="100%",
        ),
        width="100%",
    )
