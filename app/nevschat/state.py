# mypy: disable-error-code="attr-defined,name-defined"

import os
from collections import OrderedDict
from collections.abc import AsyncGenerator

from openai import OpenAI

import reflex as rx

SYSTEM_INSTRUCTIONS = OrderedDict()
SYSTEM_INSTRUCTIONS["Define"] = (
    "DO NOT translate, define in English the meaning of the given text.\n"
    + "NEVER give pronunciation for any language.\n"
    + "NEVER give romaji for Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Définir"] = (
    "NE JAMAIS traduire, définissez en français le sens du texte donné.\n"
    + "DE donnez JAMAIS de prononciation pour n'importe quelle langue.\n"
    + "DE donnez JAMAIS de romaji pour le japonais.",
    False,
)
SYSTEM_INSTRUCTIONS["Definir"] = (
    "NO traduzca, defina en español el significado del texto dado.\n"
    + "NO den NUNCA la pronunciación para cualquier idioma.\n"
    + "NO den NUNCA los romaji para el japonés.",
    False,
)
SYSTEM_INSTRUCTIONS["Explain"] = (
    "DO NOT translate, explain in English the given text.\n"
    + "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
    + "NEVER give pronunciation for any language.\n"
    + "NEVER give romaji for Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Expliquer"] = (
    "NE PAS traduire, expliquer en français le texte donné.\n"
    + "N'expliquez PAS les points de vocabulaire ou de grammaire simples ou basiques.\n"
    + "NE donnez JAMAIS de prononciation pour n'importe quelle langue.\n"
    + "NE donnez JAMAIS de romaji pour le japonais.",
    False,
)
SYSTEM_INSTRUCTIONS["Explicar"] = (
    "NO traduzca, explica en español el texto dado.\n"
    + "NO expliques el vocabulario sencillo o básico ni los puntos gramaticales "
    + "sencillos o básicos.\n"
    + "NO den NUNCA la pronunciación para cualquier idioma.\n"
    + "NO den NUNCA los romaji para el japonés.",
    False,
)
SYSTEM_INSTRUCTIONS["Check Grammar"] = (
    "DO NOT translate, check the grammar of the given text and explain any "
    + "problems in English.\n"
    + "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
    + "NEVER give pronunciation for any language. NEVER give "
    + "romaji for Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Explain Grammar"] = (
    "DO NOT translate, rather explain in English the grammar of the given text.\n"
    + "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
    + "NEVER give pronunciation for any language. NEVER give romaji for Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Explain Usage"] = (
    "DO NOT translate, rather explain in English the usage of the given text.\n"
    + "Give examples, especially where words have different meanings in different "
    + "contexts.\n"
    + "NEVER give pronunciation for any language.\n"
    + "NEVER give romaji for Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Give example sentences using the given words."] = (
    (
        "Give a dot point list of ten varied example sentences in Japanese using the "
        + "given word. Use simple vocabulary.\n"
        + " - The response MUST NOT CONTAIN pronunciation of the example sentences.\n"
        + " - The response MUST NOT CONTAIN romaji for the Japanese of the example "
        + "sentences.\n"
        + " - The response MUST NOT CONTAIN translations of the example sentences.\n"
        + " - ONLY give definitions of unusual or uncommon words."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Translate To English"] = (
    "Translate the given text into English.",
    False,
)
SYSTEM_INSTRUCTIONS["Translate To French"] = (
    "Traduisez le texte donné en français.",
    False,
)
SYSTEM_INSTRUCTIONS["Translate To Japanese"] = (
    "Translate the given text into Japanese.",
    False,
)
SYSTEM_INSTRUCTIONS["Translate To Spanish"] = (
    "Traduce el texto dado al español.",
    False,
)
# SYSTEM_INSTRUCTIONS["Translate JSON"] = (
#     """Translate the given text into Spanish, French
# and Japanese. Respond in the format below delimited by three backticks and
# formatting with the keys in this order, in a three backticks code block. Do
# not translate these instructions, simply acknowledge that you understand.

#     ```
#     [
#         ("en", "The English"),
#         ("es", "Spanish translation"),
#         ("fr", "French translation"),
#         ("ja", "Japanese translation"),
#     ],
#     ```
# """,
#     False,
# )
SYSTEM_INSTRUCTIONS["Bash"] = (
    "The question is in the context of Bash shell scripting.",
    True,
)
SYSTEM_INSTRUCTIONS["Git"] = (
    "The question is in the context of the Git version control tool.",
    True,
)
SYSTEM_INSTRUCTIONS["Linux"] = ("The question is in the context of Linux.", True)
SYSTEM_INSTRUCTIONS["Python"] = (
    "The question is in the context of the Python programming language.",
    True,
)
SYSTEM_INSTRUCTIONS["Snowflake"] = (
    "The question is in the context of Snowflake SQL queries.",
    True,
)
SYSTEM_INSTRUCTIONS["SQL"] = (
    "The question is in the context of SQL queries. Prefer Snowflake SQL, "
    + "or PostgreSQL,",
    True,
)

NORMAL_SYSTEM_INSTRUCTION = "Respond in English."

DEFAULT_SYSTEM_INSTRUCTION = "Give example sentences using the given words."
assert DEFAULT_SYSTEM_INSTRUCTION in SYSTEM_INSTRUCTIONS

GPT4_MODEL = "gpt-4-1106-preview"
GPT3_MODEL = "gpt-3.5-turbo"

TEST_PROMPT = "Give 10 example sentences about nice jugs."
TESTING = False


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
    new_prompt: str = "" if not TESTING else TEST_PROMPT
    edited_prompt: str
    is_processing: bool = False
    control_down: bool = False
    gpt_4: bool = False
    terse: bool = False
    mode: str = "Normal"
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION
    warning: str = ""

    @rx.var
    def is_not_system_instruction(self) -> bool:
        return self.mode != "Instruction:"

    @rx.var
    def cannot_clear_chat(self) -> bool:
        return len(self.prompts_responses) == 0

    @rx.var
    def cannot_clear_or_send_edited_prompt(self) -> bool:
        return len(self.edited_prompt.strip()) == 0

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
        self.edited_prompt = ""

    def clear_new_prompt(self) -> None:
        self.new_prompt = ""

    def send_edited_prompt(self, index: int):  # type: ignore
        assert len(self.edited_prompt.strip()) > 0
        self.new_prompt = self.edited_prompt
        self.prompts_responses = self.prompts_responses[:index]
        self.is_editing = False
        self.issue1675()
        return State.send

    def cancel_edit_prompt(self, index: int) -> None:
        self.edited_prompt = ""
        self.prompts_responses[index].is_editing = False
        self.is_editing = False
        self.issue1675()

    def issue1675(self) -> None:
        for i, _ in enumerate(self.prompts_responses):
            self.prompts_responses[i] = self.prompts_responses[i]

    # TODO: Figure out why Ctrl+Enter is not working.
    def handle_key_down(self, key):  # type: ignore
        if key == "Control":
            self.control_down = True
        if key == "Enter" and self.control_down:
            if self.is_editing:
                index = self.editing_index()
                if index is None:
                    raise RuntimeError(
                        "If is_editing, the editing_index cannot be None."
                    )
                return self.send_edited_prompt(index)  # type: ignore
            else:
                return State.send  # type: ignore

    def handle_key_up(self, key) -> AsyncGenerator[None, None]:  # type: ignore
        if key == "Control":
            self.control_down = False

    def cancel_control(self, _text: str = "") -> None:
        self.control_down = False

    @rx.background
    async def send(self):
        try:
            async with self:
                assert self.new_prompt != ""

                self.cancel_control()
                self.is_processing = True
                self.warning = ""

                model = GPT4_MODEL if self.gpt_4 else GPT3_MODEL
                messages = []

                if self.terse:
                    messages.append(
                        {
                            "role": "system",
                            "content": (
                                "Give terse responses without extra explanation."
                            ),
                        }
                    )

                if self.mode in SYSTEM_INSTRUCTIONS:
                    system_instruction, code_related = SYSTEM_INSTRUCTIONS[
                        self.system_instruction
                    ]
                else:
                    system_instruction, code_related = NORMAL_SYSTEM_INSTRUCTION, False

                messages.append({"role": "system", "content": system_instruction})
                if code_related:
                    messages.append(
                        {
                            "role": "system",
                            "content": (
                                "All responses with code examples MUST "
                                + "wrap the code examples in triple backticks."
                            ),
                        }
                    )

                messages.append(
                    {
                        "role": "system",
                        "content": (
                            "If prompts contain kanji assume it is Japanese, "
                            + "NEVER Chinese."
                        ),
                    }
                )

                for prompt_response in self.prompts_responses:
                    messages.append({"role": "user", "content": prompt_response.prompt})
                    messages.append(
                        {"role": "assistant", "content": prompt_response.response}
                    )
                messages.append({"role": "user", "content": self.new_prompt})

                prompt_response = PromptResponse(
                    prompt=self.new_prompt, response="", is_editing=False, model=model
                )
                self.prompts_responses.append(prompt_response)
                self.new_prompt = ""

                print(
                    f"GPT4? {self.gpt_4}\n"
                    f"Terse? {self.terse}\n"
                    f"Mode? {self.mode}\n"
                    f"Messages: {messages}"
                )

            session = OpenAI(
                timeout=10.0,
            ).chat.completions.create(
                model=os.getenv("OPENAI_MODEL", model),
                messages=messages,
                stream=True,  # Enable streaming
            )

            # pylint error: https://github.com/openai/openai-python/issues/870
            for item in session:  # pylint: disable=not-an-iterable
                async with self:
                    response = item.choices[0].delta.content
                    if response:
                        self.prompts_responses[-1].response += response
                        self.prompts_responses = self.prompts_responses
                    if not self.is_processing:
                        # It's been cancelled.
                        self.prompts_responses[-1].response += " (cancelled)"
                        self.prompts_responses = self.prompts_responses
                        break

        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(f"Error: {ex}")
        finally:
            async with self:
                self.is_processing = False

    def cancel_send(self) -> None:
        self.is_processing = False

    def clear_chat(self) -> None:
        self.prompts_responses = []
        # self.invariant()

    def invariant(self) -> None:
        number_of_prompts_being_edited = sum(
            int(prompt_response.is_editing)
            for prompt_response in self.prompts_responses
        )
        assert number_of_prompts_being_edited in [0, 1]
        assert self.is_editing == (number_of_prompts_being_edited == 1)
        assert not (
            self.cannot_send_new_prompt and self.cannot_enter_new_prompt_or_edit
        )
        assert not (
            self.cannot_clear_or_send_edited_prompt
            and self.is_editing
            and len(str(self.edited_prompt).strip()) > 0
        )
