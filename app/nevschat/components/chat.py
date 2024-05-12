# mypy: disable-error-code="attr-defined,name-defined"

import reflex as rx
from nevschat.state import DEFAULT_SYSTEM_INSTRUCTION
from nevschat.state import SYSTEM_INSTRUCTIONS
from nevschat.state import PromptResponse
from nevschat.state import State


def prompt_response_box(prompt_response: PromptResponse, index: int) -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.cond(
                prompt_response.editing,
                rx.hstack(
                    rx.text_area(
                        border_color=rx.color('bronze', 3),
                        border_style='solid',
                        border_width='3px',
                        on_blur=State.cancel_control,
                        on_change=State.update_edited_prompt,
                        on_key_down=State.handle_key_down,
                        on_key_up=State.handle_key_up,
                        value=State.edited_prompt,
                        width='100%',
                    ),
                    rx.button(
                        rx.icon(
                            tag='eraser',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='red',
                        disabled=State.cannot_clear_or_chatgpt_with_edited_prompt,
                        margin_top='0.5em',
                        on_click=lambda: State.clear_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    ),
                    rx.button(
                        rx.icon(
                            tag='send-horizontal',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='jade',
                        disabled=State.cannot_clear_or_chatgpt_with_edited_prompt,
                        margin_top='0.5em',
                        on_click=lambda: State.chatgpt_with_edited_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    ),
                    rx.button(
                        rx.icon(
                            tag='x',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='tomato',
                        margin_top='0.5em',
                        on_click=lambda: State.cancel_edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    ),
                    width='100%',
                ),
                rx.hstack(
                    rx.vstack(
                        rx.flex(
                            rx.box(
                                rx.markdown(
                                    prompt_response.prompt.text,
                                    width='100%',
                                ),
                                background_color=rx.color('bronze', 3),
                                border_color=rx.color('bronze', 8),
                                border_style='solid',
                                border_width='3px',
                                padding='0 1em 0 1em',
                            ),
                            rx.spacer(
                                width='100%',
                            ),
                            spacing='2',
                            width='100%',
                        ),
                        rx.cond(
                            prompt_response.prompt.tts_in_progress,
                            rx.center(
                                rx.chakra.spinner(
                                    color=rx.color('gray', 8),
                                    size='md',
                                ),
                                width='100%',
                            ),
                        ),
                        width='100%',
                    ),
                    rx.button(
                        rx.icon(
                            tag='square-pen',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='jade',
                        disabled=State.cannot_enter_new_prompt_or_edit,
                        is_loading=State.processing,
                        margin_top='0.5em',
                        on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    ),
                    rx.cond(
                        ~State.processing & prompt_response.prompt.contains_japanese,
                        rx.button(
                            rx.icon(
                                tag='volume-2',
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme='blue',
                            disabled=(
                                prompt_response.prompt.tts_in_progress
                                | (prompt_response.prompt.tts_wav_url != '')
                            ),
                            margin_top='0.5em',
                            on_click=lambda: State.speak_prompt(  # pylint: disable=no-value-for-parameter
                                index,
                                prompt_response.prompt,
                            ),
                        ),
                    ),
                    rx.button(
                        rx.icon(
                            tag='copy',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='gray',
                        margin_top='0.5em',
                        on_click=rx.set_clipboard(prompt_response.prompt.text),
                    ),
                    width='100%',
                ),
            ),
            rx.cond(
                prompt_response.prompt.tts_wav_url != '',
                rx.audio(
                    height='32px',
                    playing=True,
                    url=prompt_response.prompt.tts_wav_url,
                    width='100%',
                ),
            ),
            width='100%',
        ),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.flex(
                            rx.spacer(
                                width='100%',
                            ),
                            rx.cond(
                                ~State.using_profile  # pylint: disable=invalid-unary-operand-type
                                | State.profile.male,
                                rx.box(
                                    rx.markdown(
                                        prompt_response.response.text,
                                    ),
                                    background_color=rx.color('sky', 3),
                                    border_color=rx.color('sky', 8),
                                    border_style='solid',
                                    border_width='3px',
                                    min_width='10em',
                                    padding='0 1em 0 1em',
                                ),
                                rx.box(
                                    rx.markdown(
                                        prompt_response.response.text,
                                    ),
                                    background_color=rx.color('pink', 3),
                                    border_color=rx.color('pink', 8),
                                    border_radius='10px',
                                    border_style='solid',
                                    border_width='3px',
                                    min_width='10em',
                                    padding='0 1em 0 1em',
                                ),
                            ),
                            spacing='2',
                            width='100%',
                        ),
                        rx.hstack(
                            rx.text(prompt_response.response.model),
                            rx.cond(
                                prompt_response.response.tts_wav_url != '',
                                rx.text(prompt_response.response.voice),
                            ),
                            color=rx.color('gray', 8),
                            font_size='0.4em',
                            padding_bottom='1em',
                            padding_right='1.5em',
                            position='absolute',
                            bottom='0',
                            right='0',
                        ),
                        position='relative',
                        width='100%',
                    ),
                    rx.cond(
                        prompt_response.response.tts_in_progress,
                        rx.center(
                            rx.chakra.spinner(
                                color=rx.color('gray', 8),
                                size='md',
                            ),
                            width='100%',
                        ),
                    ),
                    width='100%',
                ),
                rx.cond(
                    State.processing,
                    rx.button(
                        rx.icon(
                            tag='x',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='tomato',
                        margin_top='0.5em',
                        on_click=State.cancel_chatgpt,
                    ),
                ),
                rx.hstack(
                    rx.cond(
                        ~State.processing & prompt_response.response.contains_japanese,
                        rx.button(
                            rx.icon(
                                tag='volume-2',
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme='blue',
                            disabled=(
                                prompt_response.response.tts_in_progress
                                | (prompt_response.response.tts_wav_url != '')
                            ),
                            margin_top='0.5em',
                            on_click=lambda: State.speak_response(  # pylint: disable=no-value-for-parameter
                                index,
                                prompt_response.response,
                            ),
                        ),
                    ),
                    rx.button(
                        rx.icon(
                            tag='copy',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='gray',
                        margin_top='0.5em',
                        on_click=rx.set_clipboard(prompt_response.response.text),
                    ),
                ),
                width='100%',
            ),
            rx.cond(
                prompt_response.response.tts_wav_url != '',
                rx.audio(
                    height='32px',
                    playing=True,
                    url=prompt_response.response.tts_wav_url,
                    width='100%',
                ),
            ),
            width='100%',
        ),
        width='100%',
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.flex(
            rx.checkbox(
                'GPT4',
                checked=State.gpt_4,
                on_change=State.set_gpt_4,
            ),
            rx.checkbox(
                '簡潔な返答',
                checked=State.terse,
                on_change=State.set_terse,
            ),
            rx.select(
                list(SYSTEM_INSTRUCTIONS.keys()),
                default_value=DEFAULT_SYSTEM_INSTRUCTION,
                on_change=State.set_system_instruction,
                value=State.system_instruction,
                variant='surface',
            ),
            rx.checkbox(
                '日本語のオートスピーク',
                checked=State.auto_speak,
                on_change=State.set_auto_speak,
            ),
            align='center',
            width='100%',
            spacing='2',
            wrap='wrap',
        ),
        rx.cond(
            State.using_profile,
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.box(
                            rx.cond(
                                ~State.using_profile  # pylint: disable=invalid-unary-operand-type
                                | State.profile.male,
                                rx.box(
                                    rx.markdown(
                                        State.profile.text,
                                        width='100%',
                                    ),
                                    background_color=rx.color('sky', 3),
                                    border_color=rx.color('sky', 8),
                                    border_style='solid',
                                    border_width='3px',
                                    min_width='10em',
                                    padding='0 1em 0 1em',
                                    width='100%',
                                ),
                                rx.box(
                                    rx.markdown(
                                        State.profile.text,
                                        width='100%',
                                    ),
                                    background_color=rx.color('pink', 3),
                                    border_color=rx.color('pink', 8),
                                    border_radius='10px',
                                    border_style='solid',
                                    border_width='3px',
                                    min_width='10em',
                                    padding='0 1em 0 1em',
                                    width='100%',
                                ),
                            ),
                            rx.cond(
                                State.profile.tts_wav_url != '',
                                rx.box(
                                    rx.text(State.profile.voice),
                                    color=rx.color('gray', 8),
                                    font_size='0.4em',
                                    padding_bottom='1em',
                                    padding_right='1.5em',
                                    position='absolute',
                                    bottom='0',
                                    right='0',
                                ),
                            ),
                            position='relative',
                        ),
                        rx.cond(
                            State.profile.tts_in_progress,
                            rx.center(
                                rx.chakra.spinner(
                                    color=rx.color('gray', 8),
                                    size='md',
                                ),
                                width='100%',
                            ),
                        ),
                    ),
                    rx.vstack(
                        rx.button(
                            rx.icon(
                                tag='refresh-cw',
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme='jade',
                            margin_top='0.5em',
                            on_click=lambda: State.change_profile,
                        ),
                        rx.hstack(
                            rx.button(
                                rx.icon(
                                    tag='volume-2',
                                    size=20,
                                    stroke_width=1.5,
                                ),
                                color_scheme='blue',
                                disabled=(
                                    State.profile.tts_in_progress
                                    | (State.profile.tts_wav_url != '')
                                ),
                                on_click=State.speak_profile,  # pylint: disable=no-value-for-parameter
                            ),
                            rx.button(
                                rx.icon(
                                    tag='copy',
                                    size=20,
                                    stroke_width=1.5,
                                ),
                                color_scheme='gray',
                                on_click=rx.set_clipboard(State.profile.text),
                            ),
                            width='100%',
                        ),
                    ),
                ),
                rx.cond(
                    State.profile.tts_wav_url != '',
                    rx.audio(
                        height='32px',
                        playing=True,
                        url=State.profile.tts_wav_url,
                        width='100%',
                    ),
                ),
                width='100%',
            ),
        ),
        rx.cond(
            State.has_prompts_responses,
            rx.vstack(
                rx.foreach(
                    State.prompts_responses,
                    prompt_response_box,
                ),
                width='100%',
            ),
        ),
        rx.hstack(
            rx.text_area(
                border_color=rx.color('bronze', 8),
                border_style='solid',
                border_width='3px',
                disabled=State.cannot_enter_new_prompt_or_edit,
                on_blur=State.cancel_control,
                on_change=State.set_new_prompt,
                on_key_down=State.handle_key_down,
                on_key_up=State.handle_key_up,
                placeholder='何か質問はありますか？',
                value=State.new_prompt,
                width='100%',
            ),
            rx.button(
                rx.icon(
                    tag='eraser',
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme='red',
                disabled=State.cannot_chatgpt_with_new_prompt,
                margin_top='0.5em',
                on_click=lambda: State.clear_new_prompt,
            ),
            rx.button(
                rx.icon(
                    tag='send-horizontal',
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme='jade',
                disabled=State.cannot_chatgpt_with_new_prompt,
                is_loading=State.processing,
                margin_top='0.5em',
                on_click=State.chatgpt,
            ),
            width='100%',
        ),
        width='100%',
    )
