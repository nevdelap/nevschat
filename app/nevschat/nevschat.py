# mypy: disable-error-code="attr-defined,name-defined"

from nevschat.components import chat
from nevschat.state import State

import reflex as rx

VERSION = "0.0.42"
TITLE = f"Nev's Awesome ChatGPT v{VERSION}"


def index() -> rx.Component:
    return rx.center(
        rx.script(
            """
                function play(tts_wav_url) {
                    fetch(tts_wav_url)
                        .then(response => {
                            if (!response.ok) {
                                console.log(
                                    'Checking url ' + tts_wav_url +
                                    ' got status ' + response.status +
                                    '. Retrying after a moment...'
                                );
                                setTimeout(() => {
                                    play(tts_wav_url);
                                }, 250);
                            } else {
                                console.log('Playing url ' + tts_wav_url + '.');
                                var audio = new Audio(tts_wav_url);
                                audio.load();
                                audio.play();
                            }
                        })
                        .catch(error => {
                            console.log(
                                    'Checking url ' + tts_wav_url +
                                    ' got error ' + error +
                                    '. Retrying after a moment...'
                                );
                            setTimeout(() => {
                                play(tts_wav_url);
                            }, 250);
                        });
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
