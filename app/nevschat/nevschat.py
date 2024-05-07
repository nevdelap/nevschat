# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = "0.0.97"
TITLE = f"ネヴの素晴らしいチャットジーピーティー v{VERSION}"


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(TITLE),
            rx.text(
                f"リフレックス v{rx.constants.Reflex.VERSION}",
                color="rgba(0, 0, 0, 0.4)",
            ),
            chat(),
            rx.button(
                rx.icon(
                    tag="x",
                    size=20,
                    stroke_width=1.5,
                ),
                color_scheme="tomato",
                disabled=State.cannot_clear_chat,
                on_click=State.clear_chat,
            ),
            rx.cond(
                State.using_profile,
                rx.vstack(
                    rx.divider(
                        margin="1em 0 1em 0",
                    ),
                    rx.flex(
                        rx.button(
                            "辞書",
                            color_scheme="jade",
                            height="2.25em",
                            id="lookup_definition",
                            on_click=State.lookup_definition,
                        ),
                        rx.button(
                            "文法",
                            color_scheme="jade",
                            height="2.25em",
                            id="explain_grammar",
                            on_click=State.explain_grammer,
                        ),
                        rx.button(
                            "使い方",
                            color_scheme="jade",
                            height="2.25em",
                            id="explain_usage",
                            on_click=State.explain_usage,
                        ),
                        rx.button(
                            "同じ意味",
                            color_scheme="jade",
                            height="2.25em",
                            id="give_examples_of_same_meaning",
                            on_click=State.give_examples_of_same_meaning,
                        ),
                        rx.button(
                            "反対の意味",
                            color_scheme="jade",
                            height="2.25em",
                            id="give_examples_of_opposite_meaning",
                            on_click=State.give_examples_of_opposite_meaning,
                        ),
                        rx.button(
                            "訳す",
                            color_scheme="jade",
                            height="2.25em",
                            id="translate",
                            on_click=State.translate,
                        ),
                        spacing="2",
                        width="100%",
                        wrap="wrap",
                    ),
                    rx.cond(
                        State.has_learning_aide_response,
                        rx.hstack(
                            rx.vstack(
                                rx.flex(
                                    rx.box(
                                        rx.markdown(
                                            State.learning_aide_response,
                                        ),
                                        rx.box(
                                            rx.text(State.learning_aide_model),
                                            color="rgba(0, 0, 0, 0.4)",
                                            font_size="0.4em",
                                            padding_bottom="1em",
                                            padding_right="1.5em",
                                            position="absolute",
                                            bottom="0",
                                            right="0",
                                        ),
                                        background_color="#e6f7ed",
                                        border_color="#56ba9f",
                                        border_style="solid",
                                        border_width="3px",
                                        min_width="10em",
                                        padding="0 1em 0 1em",
                                        position="relative",
                                    ),
                                    rx.spacer(
                                        width="100%",
                                    ),
                                    spacing="2",
                                    width="100%",
                                    wrap="wrap",
                                ),
                                rx.cond(
                                    State.learning_aide_tts_in_progress,
                                    rx.center(
                                        rx.chakra.spinner(
                                            color="#888",
                                            size="md",
                                        ),
                                        width="100%",
                                    ),
                                ),
                                spacing="2",
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
                                    margin_top="0.5em",
                                    on_click=State.cancel_chatgpt,
                                ),
                                rx.hstack(
                                    rx.cond(
                                        State.learning_aide_response_contains_japanese,
                                        rx.button(
                                            rx.icon(
                                                tag="volume-2",
                                                size=20,
                                                stroke_width=1.5,
                                            ),
                                            color_scheme="blue",
                                            disabled=(
                                                State.learning_aide_tts_in_progress
                                                | State.learning_aide_has_tts
                                            ),
                                            margin_top="0.5em",
                                            on_click=lambda: State.speak(  # pylint: disable=no-value-for-parameter
                                                -2,
                                                State.learning_aide_response,
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
                                        margin_top="0.5em",
                                        on_click=rx.set_clipboard(
                                            State.learning_aide_response
                                        ),
                                    ),
                                    rx.button(
                                        rx.icon(
                                            tag="x",
                                            size=20,
                                            stroke_width=1.5,
                                        ),
                                        color_scheme="tomato",
                                        margin_top="0.5em",
                                        on_click=State.clear_learning_aide_response,
                                    ),
                                ),
                            ),
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        State.has_learning_aide_response & State.learning_aide_has_tts,
                        rx.audio(
                            height="32px",
                            playing=True,
                            url=State.learning_aide_tts_wav_url,
                            width="100%",
                        ),
                    ),
                    spacing="2",
                    width="100%",
                ),
            ),
            rx.cond(
                State.warning,
                rx.callout(
                    State.warning,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
                None,
            ),
            rx.script(
                """
                    var update_selection_state = function() {
                        const has_selection = window.getSelection().toString() != '';
                        var ids = [
                            'lookup_definition',
                            'explain_grammar',
                            'explain_usage',
                            'give_examples_of_same_meaning',
                            'give_examples_of_opposite_meaning',
                            'translate'
                        ];
                        ids.forEach(function(id) {
                            var element = document.getElementById(id);
                            if (element) {
                                if (has_selection) {
                                    element.removeAttribute('data-disabled');
                                } else {
                                    element.setAttribute('data-disabled', 'true');
                                }
                            }
                        });
                    }

                    var get_selected_text_and_clear = function() {
                        const selection = window.getSelection();
                        const select_text = selection.toString();
                        selection.removeAllRanges()
                        console.log('Cleared selection.')
                        update_selection_state();
                        return select_text;
                    }

                    document.addEventListener('selectionchange', function() {
                        update_selection_state();
                    });

                    update_selection_state();
                """
            ),
            spacing="2",
            width="100%",
        ),
        align="center",
        direction="column",
        justify="start",
        max_width="800px",
        margin="2em 1em 5em 1em",
    )


app = rx.App(
    theme=rx.theme(
        accent_color="bronze",
        appearance="light",
        has_background=True,
        radius="medium",
        scaling="100%",
    )
)
app.add_page(
    index,
    title=TITLE,
)
