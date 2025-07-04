# mypy: disable-error-code="attr-defined,name-defined"

import logging

import reflex as rx
from nevschat.components import chat
from nevschat.state import State
from reflex.style import color_mode
from reflex.style import toggle_color_mode

VERSION = '0.0.196'
TITLE = f'ネヴの凄いチャット v{VERSION}'


def index() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.tooltip(
                rx.heading(TITLE),
                content='ネヴのすごいチャット',
            ),
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
        chat(),
        rx.script(
            r"""
                ///// Play From Here Buttons ///////////////////////////////////////////

                function onAudioPause(event) {
                    console.log("Audio paused, ending play from here.");
                    audio = event.target;
                    if (!audio.ended) {
                        audio.removeEventListener('ended', onAudioEnd);
                        audio.removeEventListener('pause', onAudioPause);
                    }
                }

                function onAudioEnd(event) {
                    console.log("Audio ended, playing the next one.");
                    audio = event.target;
                    audio.removeEventListener('ended', onAudioEnd);
                    audio.removeEventListener('pause', onAudioPause);
                    const audio_div = audio.parentNode;
                    const audio_divs = document.querySelectorAll('.audio');
                    const index = Array.prototype.indexOf.call(
                        audio_divs,
                        audio_div
                    );
                    if (index >= 0 && index < audio_divs.length - 1) {
                        const next_audio_div = audio_divs[index + 1];
                        play_from_here(next_audio_div.id);
                    }
                }

                const play_from_here = function(audio_id) {
                    console.log('Play from here - ' + audio_id);
                    const audio_div = document.querySelector('div#' + audio_id);
                    // Stop everything that is already playing
                    // before starting play from here.
                    document.querySelectorAll("audio").forEach(
                        audio => {
                            audio.autoplay = false;
                            audio.pause()
                        }
                    );
                    const audio = audio_div.querySelector('audio');
                    audio.addEventListener('pause', onAudioPause);
                    audio.addEventListener('ended', onAudioEnd);
                    audio.currentTime = 0;
                    audio.play();
                }

                const disable_autoplay = function(audio_id) {
                    console.log('Disable autoplay - ' + audio_id);
                    const audio_div = document.querySelector('div#' + audio_id);
                    const audio = audio_div.querySelector('audio');
                    audio.autoplay = false;
                }

                ///// Learning Aide Buttons ////////////////////////////////////////////

                const update_selection_state = function() {
                    const selection = window.getSelection().toString();
                    const ids = [
                        'check_grammar',
                        'explain_grammar',
                        'explain_usage',
                        'give_example_sentences',
                        'give_examples_of_opposite_meaning',
                        'give_examples_of_same_meaning',
                        'lookup_definition',
                        'lookup_kanji',
                        'translate',
                        'translate_to_french',
                    ];
                    ids.forEach(id => {
                        var element = document.getElementById(id);
                        if (
                            !id.startsWith('translate') && selection.length > 0
                            // Deepl doesn't translate single characters.
                            || id.startsWith('translate') && selection.length > 1
                        ) {
                            element.removeAttribute('data-disabled');
                        } else {
                            element.setAttribute('data-disabled', 'true');
                        }
                    });
                }

                const get_selected_text_and_clear = function() {
                    const selection = window.getSelection();
                    const selected_text = selection.toString();
                    selection.removeAllRanges()
                    console.log('Cleared selection.')
                    update_selection_state();
                    // The model and voice are set in css to user-select=none, and that
                    // prevents them being visibly selected in Chrome, but for some
                    // reason they can selected (even if it is not visible) as far as
                    // window.getSelection() in JavaScript is concerned. So strip that
                    // out. (Hack.)
                    return selected_text.replace(
                        /gpt-\\S+(\\s+ja-JP-\\S+)?/g,
                        ''
                    ).trim();
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


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s - Line %(lineno)d %(message)s',
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
