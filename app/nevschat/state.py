import os
from collections.abc import AsyncGenerator

import openai
import reflex as rx

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.getenv("OPENAI_API_BASE","https://api.openai.com/v1")


class PromptResponse(rx.Base):
    prompt: str
    response: str


class State(rx.State):

    prompts_responses: list[PromptResponse] = []
    next_prompt: str
    processing: bool = False
    control_down: bool = False

    @rx.var
    def invalid_next_prompt(self) -> bool:
        return len(self.next_prompt.strip()) == 0

    def clear_chat(self) -> None:
        self.prompts_responses = []


    def handle_key_down(self, key) -> AsyncGenerator[None, None]:
        if key == "Control":
            self.control_down = True
        if key == "Enter" and self.control_down:
            yield from self.process_next_prompt()

    def handle_key_up(self, key) -> AsyncGenerator[None, None]:
        if key == "Control":
            self.control_down = False

    def process_next_prompt(self) -> AsyncGenerator[None, None]:
        assert self.next_prompt != ""

        self.processing = True
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
        prompt_response = PromptResponse(prompt=self.next_prompt, response="")
        self.prompts_responses.append(prompt_response)

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                response = item.choices[0].delta.content
                self.prompts_responses[-1].response += response
                self.prompts_responses = self.prompts_responses
                yield

        self.next_prompt = ""
        self.processing = False
