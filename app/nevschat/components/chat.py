import reflex as rx

from nevschat.state import PromptResponse, State


def prompt_response_box(prompt_response: PromptResponse) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.markdown(
                    prompt_response.prompt,
                ),
                background_color="#fafafa",
                border_radius="10px",
                display="",
                padding="0.5em 1em 0.5em 1em",
                width="100%",
            ),
            rx.input(
                display="none",
            ),
            rx.button(
                "Edit",
                bg="green",
                color="white",
                display="none",
            ),
            rx.button(
                "Cancel",
                bg="red",
                color="white",
                display="none",
            ),
        ),
        rx.box(
            rx.markdown(
                prompt_response.response,
            ),
            padding="1em",
            padding_left="2em",
        ),
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(
            rx.foreach(
                State.prompts_responses,
                prompt_response_box,
            ),
            width="100%",
        ),
        rx.hstack(
            rx.debounce_input(
                rx.text_area(
                    is_disabled=State.processing,
                    placeholder = "Ask something.",
                    on_change=State.set_next_prompt,
                    on_key_down=State.handle_key_down,
                    on_key_up=State.handle_key_up,
                ),
                value=State.next_prompt,
                debounce_timeout=150,
            ),
            rx.button(
                "Send",
                bg="green",
                color="white",
                is_disabled=State.invalid_next_prompt,
                is_loading=State.processing,
                on_click=State.process_next_prompt,
            ),
            width="100%",
        ),
        rx.spacer(
            min_height="2em",
        ),
        width="100%",
    )
