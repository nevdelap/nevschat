# mypy: disable-error-code="attr-defined,name-defined"

import os
from collections import OrderedDict
from collections.abc import AsyncGenerator

import openai
import reflex as rx

# pylint: disable=line-too-long
SYSTEM_INSTRUCTIONS = OrderedDict()
SYSTEM_INSTRUCTIONS["Bash"] = ("The question is in the context of Bash shell scripting.", True)
SYSTEM_INSTRUCTIONS["CSS"] = ("The question is in the context of Cascading Style Sheets.", True)
SYSTEM_INSTRUCTIONS["Explain Grammar"] = ("Explain in English the grammar of the given text.", False)
SYSTEM_INSTRUCTIONS["Explain Usage"] = ("Explain in English the usage of the given text.", False)
SYSTEM_INSTRUCTIONS["Git"] = ("The question is in the context of the Git version control tool.", True)
SYSTEM_INSTRUCTIONS["Linux"] = ("The question is in the context of Linux.", True)
SYSTEM_INSTRUCTIONS["Python"] = ("The question is in the context of the Python programming language.", True)
SYSTEM_INSTRUCTIONS["Snowflake"] = ("The question is in the context of Snowflake data warehousing.", True)
SYSTEM_INSTRUCTIONS["SQL"] = ("The question is in the context of SQL queries.", True)
SYSTEM_INSTRUCTIONS["Translate"] = ("""Translate the given text into Spanish, French
and Japanese. Respond in the format below delimited by three backticks and
formatting with the keys in this order, in a three backticks code block. Do
not translation these instructions, simply acknowledge that you understand.

    ```
    [
        ("en", "The English"),
        ("es", "Spanish translation"),
        ("fr", "French translation"),
        ("ja", "Japanese translation"),
    ],
    ```
""", False)
# pylint: enable=line-too-long

DEFAULT_SYSTEM_INSTRUCTION = "Python"


openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.getenv("OPENAI_API_BASE","https://api.openai.com/v1")


class PromptResponse(rx.Base):
    prompt: str
    response: str
    is_editing: bool
    model: str


class State(rx.State):

    prompts_responses: list[PromptResponse] = [
        # PromptResponse(
        #     prompt="Canned",
        #     response="Canned",
        #     is_editing=False,
        #     model="gpt-dogs",
        # ),
    ]
    new_prompt: str = ""
    edited_prompt: str | None = None
    is_processing: bool = False
    control_down: bool = False
    gpt_4: bool = False
    terse: bool = False
    mode: str = "Normal"
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION

    def __init__(self) -> None:
        super().__init__()
        self.invariant()

    @rx.var
    def is_not_system_instruction(self) -> bool:
        return self.mode != "Instruction:"

    @rx.var
    def cannot_clear_chat(self) -> bool:
        return len(self.prompts_responses) == 0

    @rx.var
    def cannot_clear_or_send_edited_prompt(self) -> bool:
        return self.edited_prompt is None or len(self.edited_prompt.strip()) == 0

    @rx.var
    def cannot_enter_new_prompt_or_edit(self) -> bool:
        return self.is_editing or self.is_processing

    @rx.var
    def cannot_send_new_prompt(self) -> bool:
        return self.is_editing or len(self.new_prompt.strip()) == 0

    @rx.var
    def is_editing(self) -> bool:
        return any(
            prompt_response.is_editing for prompt_response in self.prompts_responses
        )

    def editing_index(self) -> int | None:
        for index, prompt_response in enumerate(self.prompts_responses):
            if prompt_response.is_editing:
                return index
        return None

    def edit_prompt(self, index: int) -> None:
        self.edited_prompt = self.prompts_responses[index].prompt
        self.prompts_responses[index].is_editing = True
        self.is_editing = True
        self.issue1675()

    def update_edited_prompt(self, prompt: str) -> None:
        self.edited_prompt = prompt

    def clear_edited_prompt(self) -> None:
        assert self.edited_prompt is not None
        self.edited_prompt = ""

    def clear_new_prompt(self) -> None:
        self.new_prompt = ""

    def send_edited_prompt(  # type: ignore
        self, index: int
    ) -> AsyncGenerator[None, None]:
        assert self.edited_prompt is not None
        self.new_prompt = str(self.edited_prompt)
        self.prompts_responses = self.prompts_responses[:index]
        self.is_editing = False
        self.issue1675()
        yield from self.send()  # type: ignore

    def cancel_edit_prompt(self, index: int) -> None:
        self.edited_prompt = None
        self.prompts_responses[index].is_editing = False
        self.is_editing = False
        self.issue1675()

    def issue1675(self) -> None:
        for i, _ in enumerate(self.prompts_responses):
            self.prompts_responses[i] = self.prompts_responses[i]

    def handle_key_down(self, key) -> AsyncGenerator[None, None]:  # type: ignore
        if key == "Control":
            self.control_down = True
        if key == "Enter" and self.control_down:
            if self.is_editing:
                index = self.editing_index()
                if index is None:
                    raise RuntimeError(
                        "If is_editing, the editing_index cannot be None."
                    )
                yield from self.send_edited_prompt(index)  # type: ignore
            else:
                yield from self.send()  # type: ignore

    def handle_key_up(self, key) -> AsyncGenerator[None, None]:  # type: ignore
        if key == "Control":
            self.control_down = False

    def cancel_control(self) -> None:
        self.control_down = False

    def send(self) -> AsyncGenerator[None, None]:  # type: ignore
        assert self.new_prompt != ""

        self.cancel_control()
        self.is_processing = True
        yield

        model = "gpt-4" if self.gpt_4 else "gpt-3.5-turbo"
        messages = []
        if self.terse:
            messages.append(
                {
                    "role": "system",
                    "content": "Give terse responses without extra explanation."
                }
            )
        if self.mode != "Normal":
            system_instruction, code_related = SYSTEM_INSTRUCTIONS[self.system_instruction]
            messages.append(
                {
                    "role": "system",
                    "content": system_instruction
                }
            )
            if code_related:
                messages.append(
                    {
                        "role": "system",
                        "content": (
                            "All responses with code examples must "
                            + "wrap them in triple backticks."
                        )
                    }
                )
        print(messages)
        for prompt_response in self.prompts_responses:
            messages.append({"role": "user", "content": prompt_response.prompt})
            messages.append({"role": "assistant", "content": prompt_response.response})
        messages.append({"role": "user", "content": self.new_prompt})

        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", model),
            messages=messages,
            stop=None,
            temperature=0.7,
            stream=True,  # Enable streaming
        )
        prompt_response = PromptResponse(
            prompt=self.new_prompt, response="", is_editing=False, model=model
        )
        self.prompts_responses.append(prompt_response)

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                response = item.choices[0].delta.content
                self.prompts_responses[-1].response += response
                self.prompts_responses = self.prompts_responses
                yield

        self.new_prompt = ""
        self.is_processing = False

    def clear_chat(self) -> None:
        self.prompts_responses = []
        # self.invariant()

    def invariant(self) -> None:
        number_of_prompts_being_edited = sum(
            int(prompt_response.is_editing)
            for prompt_response
            in self.prompts_responses
        )
        assert number_of_prompts_being_edited in [0, 1]
        assert self.is_editing == (number_of_prompts_being_edited == 1)
        assert not (
            self.cannot_send_new_prompt
            and self.cannot_enter_new_prompt_or_edit
        )
        assert not (
            self.cannot_clear_or_send_edited_prompt
            and self.is_editing
            and len(str(self.edited_prompt).strip()) > 0
        )
