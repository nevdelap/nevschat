import os
from collections.abc import AsyncGenerator

import openai
import reflex as rx

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.getenv("OPENAI_API_BASE","https://api.openai.com/v1")


class PromptResponse(rx.Base):
    prompt: str
    response: str
    is_editing: bool


class State(rx.State):

    prompts_responses: list[PromptResponse] = []
    next_prompt: str = ""
    new_prompt: str | None = None
    is_processing: bool = False
    control_down: bool = False

    def __init__(self) -> None:
        super().__init__()
        # self.invariant()

    @rx.var
    def is_editing(self) -> bool:
        return any(
            prompt_response.is_editing for prompt_response in self.prompts_responses
        )

    @rx.var
    def cannot_enter_new_prompt(self) -> bool:
        # self.invariant()
        return self.is_editing or self.is_processing

    @rx.var
    def cannot_send(self) -> bool:
        # self.invariant()
        return self.is_editing or len(self.next_prompt.strip()) == 0

    def edit_prompt(self, index: int) -> None:
        self.new_prompt = self.prompts_responses[index].prompt
        self.prompts_responses[index].is_editing = True
        self.is_editing = True
        self.issue1675()

    def update_new_prompt(self, prompt: str) -> None:
        self.new_prompt = prompt

    def send_edited_prompt(  # type: ignore
        self, index: int
    ) -> AsyncGenerator[None, None]:
        assert self.new_prompt is not None
        self.next_prompt = str(self.new_prompt)
        self.prompts_responses = self.prompts_responses[:index]
        self.is_editing = False
        self.issue1675()
        yield from self.send()  # type: ignore

    def cancel_edit_prompt(self, index: int) -> None:
        self.new_prompt = None
        self.prompts_responses[index].is_editing = False
        self.is_editing = False
        self.issue1675()

    def issue1675(self) -> None:
        for i, _ in enumerate(self.prompts_responses):
            self.prompts_responses[i] = self.prompts_responses[i]

    def send_new_prompt(self) -> AsyncGenerator[None, None]:  # type: ignore
        yield from self.send()  # type: ignore

    def handle_key_down(self, key) -> AsyncGenerator[None, None]:  # type: ignore
        if key == "Control":
            self.control_down = True
        if key == "Enter" and self.control_down:
            yield from self.send()  # type: ignore

    def handle_key_up(self, key) -> AsyncGenerator[None, None]:  # type: ignore
        if key == "Control":
            self.control_down = False

    def send(self) -> AsyncGenerator[None, None]:  # type: ignore
        assert self.next_prompt != ""

        self.is_processing = True
        yield

        messages = []
        for prompt_response in self.prompts_responses:
            messages.append({"role": "user", "content": prompt_response.prompt})
            messages.append({"role": "assistant", "content": prompt_response.response})
        messages.append({"role": "user", "content": self.next_prompt})

        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL","gpt-3.5-turbo"),
            messages=messages,
            stop=None,
            temperature=0.7,
            stream=True,  # Enable streaming
        )
        prompt_response = PromptResponse(
            prompt=self.next_prompt, response="", is_editing=False
        )
        self.prompts_responses.append(prompt_response)

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                response = item.choices[0].delta.content
                self.prompts_responses[-1].response += response
                self.prompts_responses = self.prompts_responses
                yield

        self.next_prompt = ""
        self.is_processing = False

    def clear_chat(self) -> None:
        self.prompts_responses = []
        # self.invariant()

    # def invariant(self):
    #     number_of_prompts_being_edited = sum(
    #         int(prompt_response.is_editing)
    #         for prompt_response
    #         in self.prompts_responses
    #     )
    #     all_good = (
    #         number_of_prompts_being_edited in [0, 1]
    #         and (not self.cannot_send and self.cannot_enter_new_prompt)
    #     )
    #     if not all_good:
    #         print("poop")
    #     return True
    #     # assert all_good
