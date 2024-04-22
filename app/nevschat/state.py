# mypy: disable-error-code="attr-defined,name-defined"

import hashlib
import os
import unicodedata
from collections import OrderedDict
from typing import Any

from nevschat.helpers import delete_old_wav_assets
from nevschat.helpers import text_to_wav
from openai import OpenAI
from rxconfig import config

import reflex as rx

SYSTEM_INSTRUCTIONS = OrderedDict()
SYSTEM_INSTRUCTIONS["日本語チャットボット"] = (
    (
        "私の友人であるかのように日本語で応答すること。中級の学習者に適した日本"
        "語を使いましょう。専門用語や俗語は使わず、くだけた表現で。プロンプトに"
        "漢字が含まれている場合、それは日本語であり、決して中国語ではありません。"
        "日本語以外の言語で回答しないこと。"
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Define"] = (
    (
        "DO NOT translate, define in English the meaning of the given text.\n"
        "NEVER give pronunciation for any language.\n"
        "NEVER give romaji for Japanese.\n"
        "If prompts contain kanji assume it is Japanese, NEVER Chinese."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Définir"] = (
    (
        "NE JAMAIS traduire, définissez en français le sens du texte donné.\n"
        "DE donnez JAMAIS de prononciation pour n'importe quelle langue.\n"
        "DE donnez JAMAIS de romaji pour le japonais.\n"
        "Si les messages contiennent des kanji, "
        "il faut supposer qu'il s'agit de japonais, JAMAIS de chinois."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Definir"] = (
    "NO traduzca, defina en español el significado del texto dado.\n"
    "NO den NUNCA la pronunciación para cualquier idioma.\n"
    "NO den NUNCA los romaji para el japonés.\n"
    "Si las indicaciones contienen kanji, "
    "asume que es japonés, NUNCA chino.",
    False,
)
SYSTEM_INSTRUCTIONS["Explain"] = (
    (
        "DO NOT translate, explain in English the given text.\n"
        "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
        "NEVER give pronunciation for any language.\n"
        "NEVER give romaji for Japanese.\n"
        "If prompts contain kanji assume it is Japanese, NEVER Chinese."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Expliquer"] = (
    (
        "NE PAS traduire, expliquer en français le texte donné.\n"
        "N'expliquez PAS les points de vocabulaire ou de grammaire simples ou "
        "basiques.\nNE donnez JAMAIS de prononciation pour n'importe quelle langue.\n"
        "NE donnez JAMAIS de romaji pour le japonais.\n"
        "Si les messages contiennent des kanji, "
        "il faut supposer qu'il s'agit de japonais, JAMAIS de chinois."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Explicar"] = (
    (
        "NO traduzca, explica en español el texto dado.\n"
        "NO expliques el vocabulario sencillo o básico ni los puntos gramaticales "
        "sencillos o básicos.\n"
        "NO den NUNCA la pronunciación para cualquier idioma.\n"
        "NO den NUNCA los romaji para el japonés.\n"
        "Si las indicaciones contienen kanji, "
        "asume que es japonés, NUNCA chino."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Check Grammar"] = (
    (
        "DO NOT translate, check the grammar of the given text and explain any "
        "problems in English.\n"
        "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
        "NEVER give pronunciation for any language. NEVER give "
        "romaji for Japanese.\n"
        "If prompts contain kanji assume it is Japanese, NEVER Chinese."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Explain Grammar"] = (
    (
        "DO NOT translate, rather explain in English the grammar of the given text.\n"
        "DO NOT explain the simple or basic vocabulary or grammatical points.\n"
        "NEVER give pronunciation for any language. NEVER give romaji for Japanese.\n"
        "If prompts contain kanji assume it is Japanese, NEVER Chinese."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Explain Usage"] = (
    (
        "DO NOT translate, rather explain in English the usage of the given text.\n"
        "Give examples, especially where words have different meanings in different "
        "contexts.\n"
        "NEVER give pronunciation for any language.\n"
        "NEVER give romaji for Japanese.\n"
        "If prompts contain kanji assume it is Japanese, NEVER Chinese."
    ),
    False,
)
SYSTEM_INSTRUCTIONS["Give example sentences using the given words."] = (
    (
        "Give a dot point list of ten varied example sentences in Japanese using the "
        "given word. Use simple vocabulary.\n"
        " - The response MUST NOT CONTAIN pronunciation of the example sentences.\n"
        " - The response MUST NOT CONTAIN romaji for the Japanese of the example "
        "sentences.\n"
        " - The response MUST NOT CONTAIN translations of the example sentences.\n"
        " - ONLY give definitions of unusual or uncommon words."
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
SYSTEM_INSTRUCTIONS["Docker"] = (
    "The question is in the context of Docker containerisation technology.",
    True,
)
SYSTEM_INSTRUCTIONS["Git"] = (
    "The question is in the context of the Git version control tool.",
    True,
)
SYSTEM_INSTRUCTIONS["Linux"] = ("The question is in the context of Linux.", True)
SYSTEM_INSTRUCTIONS["Nginx"] = (
    "The question is in the context of Nginx configuration.",
    True,
)
SYSTEM_INSTRUCTIONS["Python"] = (
    "The question is in the context of the Python programming language.",
    True,
)
SYSTEM_INSTRUCTIONS["Snowflake SQL"] = (
    "The question is in the context of Snowflake SQL queries.",
    True,
)
SYSTEM_INSTRUCTIONS["SQL"] = (
    "The question is in the context of SQL queries. Prefer Snowflake SQL, "
    + "or PostgreSQL, or ANSI SQL.",
    True,
)

NORMAL_SYSTEM_INSTRUCTION = "Respond in English."

DEFAULT_SYSTEM_INSTRUCTION = "日本語チャットボット"
assert DEFAULT_SYSTEM_INSTRUCTION in SYSTEM_INSTRUCTIONS

GPT4_MODEL = "gpt-4-turbo"
GPT3_MODEL = "gpt-3.5-turbo"

USE_QUICK_PROMPT = False  # True to add a first prompt, for testing.
USE_CANNED_RESPONSE = False  # True to add a first response, for testing.


def is_japanese_char(ch: str) -> bool:
    """
    Return True if the character is a Japanese character.
    """
    assert len(ch) == 1
    try:
        block = unicodedata.name(ch).split()[0]
        is_japanese = block in [
            "CJK",
            "COMMA",
            "DIGIT",
            "FULLWIDTH",
            "FULL STOP",
            "HIRAGANA",
            "IDEOGRAPHIC",
            "KATAKANA",
            "KATAKANA-HIRAGANA",
            "LEFT",
            "RIGHT",
            "SPACE",
        ]
        # print(ch, block, "J" if is_japanese else "")
        return is_japanese
    except ValueError:
        return False


def is_japanese_text(text: str) -> bool:
    """
    Return True if at least X percent of characters in the
    text are Japanese characters.
    """
    if len(text) == 0:
        return False
    percent_required = 60
    japanese_characters = sum(1 for ch in text if is_japanese_char(ch))
    percent = 100 * japanese_characters / len(text)
    # print(f"{int(percent)}% Japanese.")
    return percent >= percent_required


class PromptResponse(rx.Base):  # type: ignore
    prompt: str
    response: str
    is_editing: bool
    is_japanese: bool
    model: str


class State(rx.State):  # type: ignore
    prompts_responses: list[PromptResponse] = (
        [
            PromptResponse(
                prompt="そうですか？",
                response="はい、そうです。",
                is_editing=False,
                is_japanese=True,
                model="gpt-canned",
            ),
        ]
        if USE_CANNED_RESPONSE
        else []
    )
    control_down: bool = False
    edited_prompt: str
    gpt_4: bool = False
    is_processing: bool = False
    mode: str = "Normal"
    new_prompt: str = "可愛いウサギがいる?" if USE_QUICK_PROMPT else ""
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION
    terse: bool = False
    warning: str = ""

    @rx.var  # type: ignore
    def is_not_system_instruction(self) -> bool:
        return self.mode != "Instruction:"

    @rx.var  # type: ignore
    def cannot_clear_chat(self) -> bool:
        return len(self.prompts_responses) == 0

    @rx.var  # type: ignore
    def cannot_clear_or_chatgpt_with_edited_prompt(self) -> bool:
        return len(self.edited_prompt.strip()) == 0

    @rx.var  # type: ignore
    def cannot_enter_new_prompt_or_edit(self) -> bool:
        return self.is_editing or self.is_processing

    @rx.var  # type: ignore
    def cannot_chatgpt_with_new_prompt(self) -> bool:
        return self.is_editing or len(self.new_prompt.strip()) == 0

    @rx.var  # type: ignore
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
        # self.issue1675()

    def update_edited_prompt(self, prompt: str) -> None:
        self.edited_prompt = prompt

    def clear_edited_prompt(self) -> None:
        self.edited_prompt = ""

    def clear_new_prompt(self) -> None:
        self.new_prompt = ""

    def chatgpt_with_edited_prompt(self, index: int) -> Any:
        assert len(self.edited_prompt.strip()) > 0
        self.new_prompt = self.edited_prompt
        self.prompts_responses = self.prompts_responses[:index]
        self.is_editing = False
        return State.chatgpt

    def cancel_edit_prompt(self, index: int) -> None:
        self.edited_prompt = ""
        self.prompts_responses[index].is_editing = False
        self.is_editing = False

    def handle_key_down(self, key: str) -> Any:
        if key == "Control":
            self.control_down = True
        elif key == "Enter" and self.control_down:
            if self.is_editing:
                index = self.editing_index()
                if index is None:
                    raise RuntimeError(
                        "If is_editing, the editing_index cannot be None."
                    )
                return self.chatgpt_with_edited_prompt(index)
            return State.chatgpt
        return None

    def handle_key_up(self, key: str) -> None:
        if key == "Control":
            self.control_down = False

    def cancel_control(self, _text: str = "") -> None:
        self.control_down = False

    @rx.background  # type: ignore
    async def chatgpt(self) -> None:
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

                if self.mode == "Normal":
                    system_instruction, code_related = NORMAL_SYSTEM_INSTRUCTION, False
                else:
                    system_instruction, code_related = SYSTEM_INSTRUCTIONS[
                        self.system_instruction
                    ]

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

                for prompt_response in self.prompts_responses:
                    messages.append({"role": "user", "content": prompt_response.prompt})
                    messages.append(
                        {"role": "assistant", "content": prompt_response.response}
                    )
                messages.append({"role": "user", "content": self.new_prompt})

                prompt_response = PromptResponse(
                    prompt=self.new_prompt,
                    response="",
                    is_editing=False,
                    is_japanese=False,
                    model=model,
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
                messages=messages,  # type: ignore
                stream=True,  # Enable streaming
            )

            # pylint error: https://github.com/openai/openai-python/issues/870
            for item in session:  # pylint: disable=not-an-iterable
                async with self:
                    response = item.choices[0].delta.content  # type: ignore
                    if response:
                        self.prompts_responses[-1].response += response
                        self.prompts_responses[-1].is_japanese = is_japanese_text(
                            self.prompts_responses[-1].response
                        )
                    if not self.is_processing:
                        # It's been cancelled.
                        self.prompts_responses[-1].response += " (cancelled)"
                        break

        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(f"Error: {ex}")
        finally:
            async with self:
                self.is_processing = False

    def cancel_chatgpt(self) -> None:
        self.is_processing = False

    def clear_chat(self) -> None:
        self.prompts_responses = []
        # self.invariant()

    @rx.background  # type: ignore
    async def speak(self, text: str) -> Any:
        try:
            text_to_wav(text)
            delete_old_wav_assets()
            hash_ = hashlib.md5(text.encode(encoding="utf-8")).hexdigest()  # nosec
            tts_wave_filename = f"tts_{hash_}.wav"
            tts_wave_url = os.path.join(
                config.frontend_path, f"wav/{tts_wave_filename}"
            )
            print(f"Playing url {tts_wave_url}.")
            return rx.call_script(f"play('{tts_wave_url}');")
        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(f"Error: {ex}")

    def invariant(self) -> None:
        number_of_prompts_being_edited = sum(
            int(prompt_response.is_editing)
            for prompt_response in self.prompts_responses
        )
        assert number_of_prompts_being_edited in [0, 1]
        assert self.is_editing == (number_of_prompts_being_edited == 1)
        assert not (
            self.cannot_chatgpt_with_new_prompt and self.cannot_enter_new_prompt_or_edit
        )
        assert not (
            self.cannot_clear_or_chatgpt_with_edited_prompt
            and self.is_editing
            and len(str(self.edited_prompt).strip()) > 0
        )
