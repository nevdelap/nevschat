# mypy: disable-error-code="attr-defined,name-defined"

import reflex as rx
from nevschat.components.my_audio import my_audio
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
                        debounce_timeout=1000,
                        on_blur=State.cancel_control,
                        on_change=State.update_edited_prompt,
                        on_key_down=State.handle_key_down,
                        on_key_up=State.handle_key_up,
                        value=State.edited_prompt,
                        width='100%',
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.button(
                                rx.icon(
                                    tag='eraser',
                                    size=20,
                                    stroke_width=1.5,
                                ),
                                color_scheme='red',
                                disabled=(
                                    State.cannot_clear_or_chatgpt_with_edited_prompt
                                ),
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
                                disabled=(
                                    State.cannot_clear_or_chatgpt_with_edited_prompt
                                ),
                                margin_top='0.5em',
                                on_click=lambda: State.chatgpt_with_edited_prompt(  # pylint: disable=no-value-for-parameter
                                    index  # type: ignore
                                ),
                            ),
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
                    ),
                    width='100%',
                ),
                rx.hstack(
                    rx.vstack(
                        rx.flex(
                            rx.box(
                                rx.markdown(
                                    prompt_response.prompt.text,
                                    margin='-0.5em 0em -0.5em 0em',
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
                                rx.spinner(
                                    color=rx.color('gray', 8),
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
                        is_loading=State.chat_processing,
                        margin_top='0.5em',
                        on_click=lambda: State.edit_prompt(index),  # type: ignore  # pylint: disable=no-value-for-parameter
                    ),
                    rx.cond(
                        ~State.chat_processing
                        & prompt_response.prompt.contains_japanese,
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
                rx.hstack(
                    my_audio(
                        id=f'audio_prompt_{index}',
                        class_name='audio',
                        height='32px',
                        # playing=True makes it play when it appears on the page
                        # for the first time, the on_pause makes it not autoplay
                        # in future, particularly on page refreshes.
                        on_pause=State.disable_autoplay(f'audio_prompt_{index}'),  # pylint: disable=no-value-for-parameter
                        playing=True,
                        url=prompt_response.prompt.tts_wav_url,
                        width='100%',
                    ),
                    rx.button(
                        rx.icon(
                            tag='list-video',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='blue',
                        on_click=lambda: State.play_from_here(f'audio_prompt_{index}'),  # pylint: disable=no-value-for-parameter
                    ),
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
                                State.profile.male,
                                rx.box(
                                    rx.markdown(
                                        prompt_response.response.text,
                                        margin='-0.5em 0em -0.5em 0em',
                                        width='100%',
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
                                        margin='-0.5em 0em -0.5em 0em',
                                        width='100%',
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
                            padding_bottom='0.55em',
                            padding_right='1.5em',
                            position='absolute',
                            bottom='0',
                            right='0',
                            user_select='none',
                        ),
                        position='relative',
                        width='100%',
                    ),
                    rx.cond(
                        prompt_response.response.tts_in_progress,
                        rx.center(
                            rx.spinner(
                                color=rx.color('gray', 8),
                            ),
                            width='100%',
                        ),
                    ),
                    width='100%',
                ),
                rx.cond(
                    State.chat_processing,
                    rx.button(
                        rx.icon(
                            tag='x',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='tomato',
                        margin_top='0.5em',
                        on_click=State.cancel_chat_processing,
                    ),
                ),
                rx.hstack(
                    rx.cond(
                        ~State.chat_processing
                        & prompt_response.response.contains_japanese,
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
                rx.hstack(
                    my_audio(
                        id=f'audio_response_{index}',
                        class_name='audio',
                        height='32px',
                        # playing=True makes it play when it appears on the page
                        # for the first time, the on_pause makes it not autoplay
                        # in future, particularly on page refreshes.
                        on_pause=State.disable_autoplay(f'audio_response_{index}'),  # pylint: disable=no-value-for-parameter
                        playing=True,
                        url=prompt_response.response.tts_wav_url,
                        width='100%',
                    ),
                    rx.button(
                        rx.icon(
                            tag='list-video',
                            size=20,
                            stroke_width=1.5,
                        ),
                        color_scheme='blue',
                        on_click=lambda: State.play_from_here(  # pylint: disable=no-value-for-parameter
                            f'audio_response_{index}'
                        ),
                    ),
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
                'Best Model',
                checked=State.gpt_best,
                on_change=State.set_gpt_best,
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
            State.using_profile_in_prompts,
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.box(
                            rx.cond(
                                State.profile.male,
                                rx.box(
                                    rx.markdown(
                                        State.profile.text,
                                        margin='-0.5em 0em -0.5em 0em',
                                        width='100%',
                                    ),
                                    background_color=rx.color('sky', 3),
                                    border_color=rx.color('sky', 8),
                                    border_style='solid',
                                    border_width='3px',
                                    min_width='10em',
                                    padding='0em 1em 0 1em',
                                    width='100%',
                                ),
                                rx.box(
                                    rx.markdown(
                                        State.profile.text,
                                        margin='-0.5em 0em -0.5em 0em',
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
                                    padding_bottom='0.55em',
                                    padding_right='1.5em',
                                    position='absolute',
                                    bottom='0',
                                    right='0',
                                    user_select='none',
                                ),
                            ),
                            position='relative',
                        ),
                        rx.cond(
                            State.profile.tts_in_progress,
                            rx.center(
                                rx.spinner(
                                    color=rx.color('gray', 8),
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
                    rx.hstack(
                        my_audio(
                            id='audio_profile',
                            class_name='audio',
                            height='32px',
                            # playing=True makes it play when it appears on the page
                            # for the first time, the on_pause makes it not autoplay
                            # in future, particularly on page refreshes.
                            on_pause=State.disable_autoplay('audio_profile'),  # pylint: disable=no-value-for-parameter
                            playing=True,
                            url=State.profile.tts_wav_url,
                            width='100%',
                        ),
                        rx.button(
                            rx.icon(
                                tag='list-video',
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme='blue',
                            on_click=State.play_from_profile(),  # pylint: disable=no-value-for-parameter
                        ),
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
                debounce_timeout=1000,
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
                is_loading=State.chat_processing,
                margin_top='0.5em',
                on_click=State.chatgpt,
            ),
            width='100%',
        ),
        rx.button(
            rx.icon(
                tag='x',
                size=20,
                stroke_width=1.5,
            ),
            color_scheme='tomato',
            disabled=State.cannot_clear_chat,
            on_click=State.clear_chat,
        ),
        rx.divider(),
        rx.flex(
            rx.button(
                '辞書',
                color_scheme='jade',
                height='2.25em',
                id='lookup_definition',
                on_click=State.lookup_definition,
            ),
            rx.button(
                '漢字',
                color_scheme='jade',
                height='2.25em',
                id='lookup_kanji',
                on_click=State.lookup_kanji,
            ),
            rx.button(
                '翻訳',
                color_scheme='jade',
                height='2.25em',
                id='translate',
                on_click=State.translate,
            ),
            rx.button(
                'フランス語へ',
                color_scheme='jade',
                height='2.25em',
                id='translate_to_french',
                on_click=State.translate_to_french,
            ),
            rx.button(
                '文法説明',
                color_scheme='jade',
                height='2.25em',
                id='explain_grammar',
                on_click=State.explain_grammar,
            ),
            rx.button(
                '文法チェック',
                color_scheme='jade',
                height='2.25em',
                id='check_grammar',
                on_click=State.check_grammar,
            ),
            rx.button(
                '使い方',
                color_scheme='jade',
                height='2.25em',
                id='explain_usage',
                on_click=State.explain_usage,
            ),
            rx.button(
                '例文',
                color_scheme='jade',
                height='2.25em',
                id='give_example_sentences',
                on_click=State.give_example_sentences,
            ),
            rx.button(
                '同じ意味',
                color_scheme='jade',
                height='2.25em',
                id='give_examples_of_same_meaning',
                on_click=State.give_examples_of_same_meaning,
            ),
            rx.button(
                '反対の意味',
                color_scheme='jade',
                height='2.25em',
                id='give_examples_of_opposite_meaning',
                on_click=State.give_examples_of_opposite_meaning,
            ),
            spacing='2',
            width='100%',
            wrap='wrap',
        ),
        rx.cond(
            State.learning_aide.text != '',
            rx.flex(
                rx.spacer(
                    width='100%',
                ),
                rx.vstack(
                    rx.box(
                        rx.box(
                            rx.markdown(
                                State.learning_aide.text,
                                margin='-0.5em 0em -0.5em 0em',
                                width='100%',
                            ),
                            background_color=rx.color('jade', 3),
                            border_color=rx.color('jade', 8),
                            border_style='solid',
                            border_width='3px',
                            min_width='10em',
                            padding='0 1em 0 1em',
                        ),
                        rx.box(
                            rx.text(
                                State.learning_aide.model,
                            ),
                            color=rx.color('gray', 8),
                            font_size='0.4em',
                            padding_bottom='0.55em',
                            padding_right='1.5em',
                            position='absolute',
                            bottom='0',
                            right='0',
                            user_select='none',
                        ),
                        position='relative',
                        width='100%',
                    ),
                    rx.cond(
                        State.learning_aide.tts_in_progress,
                        rx.center(
                            rx.spinner(
                                color=rx.color('gray', 8),
                            ),
                            width='100%',
                        ),
                    ),
                ),
                rx.vstack(
                    rx.hstack(
                        rx.cond(
                            State.learning_aide_processing,
                            rx.button(
                                rx.icon(
                                    tag='x',
                                    size=20,
                                    stroke_width=1.5,
                                ),
                                color_scheme='tomato',
                                margin_top='0.5em',
                                on_click=State.cancel_learning_aide_processing,
                            ),
                            rx.hstack(
                                rx.cond(
                                    State.learning_aide.contains_japanese,
                                    rx.button(
                                        rx.icon(
                                            tag='volume-2',
                                            size=20,
                                            stroke_width=1.5,
                                        ),
                                        color_scheme='blue',
                                        disabled=(
                                            State.learning_aide.tts_in_progress
                                            | (State.learning_aide.tts_wav_url != '')
                                        ),
                                        margin_top='0.5em',
                                        on_click=State.speak_learning_aide,  # pylint: disable=no-value-for-parameter
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
                                    on_click=rx.set_clipboard(State.learning_aide.text),
                                ),
                            ),
                        ),
                    ),
                    rx.cond(
                        ~State.learning_aide_processing,
                        rx.button(
                            rx.icon(
                                tag='x',
                                size=20,
                                stroke_width=1.5,
                            ),
                            color_scheme='tomato',
                            margin_top='0.5em',
                            on_click=State.clear_learning_aide_response,
                        ),
                    ),
                ),
                spacing='2',
                width='100%',
            ),
        ),
        rx.cond(
            (
                (State.learning_aide.text != '')
                & (State.learning_aide.tts_wav_url != '')
            ),
            my_audio(
                id='audio_learning_aide',
                height='32px',
                # playing=True makes it play when it appears on the page
                # for the first time, the on_pause makes it not autoplay
                # in future, particularly on page refreshes.
                on_pause=State.disable_autoplay('audio_learning_aide'),  # pylint: disable=no-value-for-parameter
                playing=True,
                url=State.learning_aide.tts_wav_url,
                width='100%',
            ),
        ),
        width='100%',
    )
