# mypy: disable-error-code="attr-defined,name-defined"

import reflex as rx
from nevschat.components import chat
from nevschat.state import State
from reflex.style import color_mode  # type: ignore
from reflex.style import toggle_color_mode

VERSION = '0.0.124.alpha.2'
TITLE = f'ネヴのすごいチャットジーピーティー v{VERSION}'


def index() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.heading(TITLE),
            rx.spacer(
                width='100%',
            ),
            rx.button(
                rx.cond(
                    color_mode == 'light',
                    rx.icon(
                        tag='moon',
                    ),
                    rx.icon(
                        tag='sun',
                    ),
                ),
                color=rx.color('gray', 12),
                background_color='rgba(0, 0, 0, 0)',
                on_click=toggle_color_mode,
            ),
            spacing='2',
            width='100%',
        ),
        rx.text(
            f'リフレックス v{rx.constants.Reflex.VERSION}',
            color=rx.color('gray', 8),
        ),
        chat(),
        rx.cond(
            State.warning,
            rx.callout(
                State.warning,
                icon='triangle_alert',
                color_scheme='red',
                role='alert',
            ),
            None,
        ),
        rx.script(
            """
                ///// Play From Here Buttons ///////////////////////////////////////////

                const play_from_here = function(audio_id) {
                    console.log('Play from here - ' + audio_id);
                    if (audio_id) {
                        const audio_div = document.querySelector('div#' + audio_id);
                        if (audio_div) {
                            const audio = audio_div.querySelector('audio');
                            audio.addEventListener('ended', function onAudioEnd() {
                                audio.removeEventListener('ended', onAudioEnd);
                                const audio_divs = document.querySelectorAll('.audio');
                                const index = Array.prototype.indexOf.call(
                                    audio_divs,
                                    audio_div
                                );
                                if (index >= 0 && index < audio_divs.length - 1) {
                                    const next_audio_div = audio_divs[index + 1];
                                    play_from_here(next_audio_div.id);
                                }
                            })
                            audio.play();
                        }
                    }
                }

                ///// Learning Aide Buttons ////////////////////////////////////////////

                const update_selection_state = function() {
                    const has_selection = window.getSelection().toString() != '';
                    const ids = [
                        'check_grammar',
                        'explain_grammar',
                        'explain_usage',
                        'give_example_sentences',
                        'give_examples_of_opposite_meaning',
                        'give_examples_of_same_meaning',
                        'lookup_definition',
                        'translate',
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

                const get_selected_text_and_clear = function() {
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
        margin='2em 1em 5em 1em',
        max_width='800px',
        spacing='2',
    )


app = rx.App(
    theme=rx.theme(
        accent_color='bronze',
        appearance='light',
        has_background=True,
        radius='medium',
        scaling='100%',
    )
)
app.add_page(
    index,
    title=TITLE,
)
