# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = "0.0.40"
TITLE = f"Nev's Awesome ChatGPT v{VERSION}"


def index() -> rx.Component:
    return rx.center(
        rx.script(
            """
                function check_url_and_play(url) {
                    fetch(url)
                        .then(response => {
                            if (!response.ok) {
                                console.log(
                                    'Checking url ' + url +
                                    ' got status ' + response.status +
                                    '. Retrying after a moment...'
                                );
                                setTimeout(() => {
                                    check_url_and_play(url);
                                }, 250);
                            } else {
                                console.log('Playing url ' + url + '.');
                                var audio = new Audio(tts_wav_url);
                                audio.load();
                                audio.play();
                            }
                        })
                        .catch(error => {
                            console.log(
                                    'Checking url ' + url +
                                    ' got error ' + error +
                                    '. Retrying after a moment...'
                                );
                            setTimeout(() => {
                                check_url_and_play(url);
                            }, 250);
                        });
                }
                function play(response) {
                    tts_wav_url = '/tts_' + response + '.wav';
                    check_url_and_play(tts_wav_url);
                }
            """
        ),
        rx.vstack(
            rx.heading(TITLE),
            rx.text(
                f"Reflex v{rx.constants.Reflex.VERSION}.",
                color="#aaa",
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
                State.warning,
                rx.callout(
                    State.warning,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
                None,
            ),
            max_width="800px",
            padding="1em",
            width="100%",
        ),
        align="center",
        direction="column",
        justify="start",
    )


app = rx.App(
    theme=rx.theme(
        accent_color="teal",
        appearance="light",
        has_background=True,
        radius="large",
        scaling="100%",
    )
)
app.add_page(
    index,
    title=TITLE,
)
