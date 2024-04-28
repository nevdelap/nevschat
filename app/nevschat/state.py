# mypy: disable-error-code="attr-defined,name-defined"

import os
import re
import time
import unicodedata
from collections import OrderedDict
from collections.abc import AsyncGenerator
from typing import Any
from urllib.parse import urljoin

import requests
from nevschat.helpers import delete_old_wav_assets
from nevschat.helpers import get_random_voice
from nevschat.helpers import text_to_wav
from openai import OpenAI
from rxconfig import config
from rxconfig import site_runtime_assets_url

import reflex as rx

SYSTEM_INSTRUCTIONS = OrderedDict()
SYSTEM_INSTRUCTIONS["Normal English"] = ("Respond in English.", False)
SYSTEM_INSTRUCTIONS["私の三才の日本人の子供"] = (
    """
私の三才の日本人の子供であるかのように日本語で応答すること。
- プロンプトに漢字が含まれている場合、それは日本語であり、決して中国語ではない。
- 回答には日本語以外の言語を含んではならない。
- 回答はひらがなやカタカナやふりがなやローマ字の発音を含んではならない。
- 回答にリストが含まれている場合は、番号付きリストではなく、箇条書きのリストを
使用してください。
    """,
    False,
)
SYSTEM_INSTRUCTIONS["日本語チャットボット"] = (
    """
友達になったつもりで日本語で答えてください。
- プロンプトに漢字が含まれている場合、それは日本語であり、決して中国語ではない。
- 回答には日本語以外の言語を含んではならない。
- 回答はひらがなやカタカナやふりがなやローマ字の発音を含んではならない。
- 回答にリストが含まれている場合は、番号付きリストではなく、箇条書きのリストを
使用してください。
    """,
    False,
)
SYSTEM_INSTRUCTIONS["Check Grammar"] = (
    """
DO NOT translate, check the grammar of the given text and explain any problems
in English. DO NOT explain the simple or basic vocabulary or grammatical points.
NEVER give pronunciation for any language. NEVER give romaji for Japanese. If
prompts contain kanji assume it is Japanese, NEVER Chinese.
    """,
    False,
)
SYSTEM_INSTRUCTIONS["Explain Grammar"] = (
    """
DO NOT translate, rather explain in English the grammar of the given text. DO
NOT explain the simple or basic vocabulary or grammatical points. NEVER give
pronunciation for any language. NEVER give romaji for Japanese. If prompts
contain kanji assume it is Japanese, NEVER Chinese.
    """,
    False,
)
SYSTEM_INSTRUCTIONS["Explain Usage"] = (
    """
DO NOT translate, rather explain in English the usage of the given text. Give
examples, especially where words have different meanings in different contexts.
NEVER give pronunciation for any language. NEVER give romaji for Japanese. If
prompts contain kanji assume it is Japanese, NEVER Chinese.
    """,
    False,
)
SYSTEM_INSTRUCTIONS["Give example sentences using the given words."] = (
    """
Give a dot point list of 5 varied example sentences in Japanese using the given
word, with their translation in brackets. Use simple vocabulary.
 - The response MUST NOT CONTAIN pronunciation of the example sentences.
 - The response MUST NOT CONTAIN romaji for the Japanese of the example
sentences.
 - Give definitions of unusual or uncommon words.
    """,
    False,
)
SYSTEM_INSTRUCTIONS["Give varied ways of expressing the given meaning."] = (
    """
Give a dot point list of up to 5 varied ways of expressing the same meaning as
the given text, in Japanese, with their translations in brackets.
 - The response MUST NOT CONTAIN pronunciation of the example sentences.
 - The response MUST NOT CONTAIN romaji for the Japanese of the example
sentences.
 - Give definitions of unusual or uncommon words.
    """,
    False,
)
SYSTEM_INSTRUCTIONS[
    "Give varied ways of expressing the opposite of the given meaning."
] = (
    """
Give a dot point list of up to 5 varied ways of expressing the meaning opposite
to that of the given text, in Japanese, with their translations in brackets.
 - The response MUST NOT CONTAIN pronunciation of the example sentences.
 - The response MUST NOT CONTAIN romaji for the Japanese of the example
sentences.
 - Give definitions of unusual or uncommon words.
    """,
    False,
)
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

DEFAULT_SYSTEM_INSTRUCTION = "私の三才の日本人の子供"
assert DEFAULT_SYSTEM_INSTRUCTION in SYSTEM_INSTRUCTIONS

GPT4_MODEL = "gpt-4-turbo"
GPT3_MODEL = "gpt-3.5-turbo"

USE_QUICK_PROMPT = False  # True to add a first prompt, for testing.
USE_CANNED_RESPONSE = False  # True to add a first response, for testing.


def is_japanese_char(ch: str, log: bool = False) -> bool:
    """
    Return True if the character is a Japanese character.
    """
    assert len(ch) == 1
    try:
        block = unicodedata.name(ch).split()[0]
        is_japanese = block in [
            "CJK",
            "DIGIT",
            "FULLWIDTH",
            "HIRAGANA",
            "IDEOGRAPHIC",
            "KATAKANA",
            "KATAKANA-HIRAGANA",
            "LEFT",
            "RIGHT",
        ]
        if log:
            print(ch, block, "J" if is_japanese else "")
        return is_japanese
    except ValueError:
        return False


def is_latin_char(ch: str, log: bool = False) -> bool:
    """
    Return True if the character is a Japanese character.
    """
    assert len(ch) == 1
    try:
        block = unicodedata.name(ch).split()[0]
        is_latin = block in [
            "LATIN",
        ]
        if log:
            print(ch, block, "L" if is_latin else "")
        return is_latin
    except ValueError:
        return False


def contains_japanese(text: str, log: bool = False) -> bool:
    """
    Return True if the text contains any Japanese at all.
    """
    if len(text) == 0:
        return False
    return any(is_japanese_char(ch, log) for ch in text)


def contains_latin(text: str, log: bool = False) -> bool:
    """
    Return True if the text contains any latin characters at all.
    """
    if len(text) == 0:
        return False
    return any(is_latin_char(ch, log) for ch in text)


def strip_non_japanese_split_sentences(text: str) -> str:
    """
    If the text contains non-Japanese characters from the text, insert 。
    between pieces of Japanese that were separated by non-Japanese to make the
    tts insert a pause rather then running them all together, and remove
    consecutive duplicate sentences.
    """
    if contains_latin(text):
        text = re.sub(
            r"。+",
            "。",
            "".join(ch if is_japanese_char(ch, True) else "。" for ch in text) + "。",
        ).lstrip("。")
        while True:
            old_len = len(text)
            text = re.sub(r"([^、。]*[、。])\1", r"\1", text)
            if len(text) == old_len:
                break
    return text


# Built-in test.
def test_strip_non_japanese_split_sentence(original: str, expected: str) -> None:
    stripped = strip_non_japanese_split_sentences(original)
    assert stripped == expected, f"{original}: {stripped} != {expected}"


# If mixed Japanese and latin, strip latin characters.
test_strip_non_japanese_split_sentence(
    "Both '異る' and '違う' are verbs in Japanese that can be translated as "
    "'to differ' or 'to be different'. '異る' carries a stronger connotation "
    "of being unusual, rare, or significant in its difference compared to "
    "something else.",
    "異る。違う。異る。",
)

# If only Japanese leave as is.
test_strip_non_japanese_split_sentence(
    "おんな、おんな、",
    "おんな、おんな、",
)

# If mixed Japanese and latin, strip latin characters and duplication.
test_strip_non_japanese_split_sentence(
    "おんな、おんな、is Japanese.",
    "おんな、。",
)

# If mixed Japanese and latin, strip latin characters and duplication.
test_strip_non_japanese_split_sentence(
    "違う。違う。違う。hello.違う。違う。",
    "違う。",
)

# If mixed Japanese and latin, add 。 between pieces of Japanese.
test_strip_non_japanese_split_sentence(
    "日本語あるハー「」。、ab, ()1",
    "日本語あるハー「」。、。()1。",
)


class PromptResponse(rx.Base):  # type: ignore
    prompt: str
    response: str
    is_editing: bool
    contains_japanese: bool
    tts_in_progress: bool
    has_tts: bool
    tts_wav_url: str
    model: str
    voice: str


class State(rx.State):  # type: ignore
    prompts_responses: list[PromptResponse] = (
        [
            PromptResponse(
                prompt="そうですか？",
                response="はい、そうです。",
                is_editing=False,
                contains_japanese=True,
                tts_in_progress=False,
                has_tts=False,
                tts_wav_url="",
                model="gpt-canned",
                voice="",
            ),
        ]
        if USE_CANNED_RESPONSE
        else []
    )
    auto_speak: bool = False
    control_down: bool = False
    edited_prompt: str
    gpt_4: bool = False
    is_processing: bool = False
    new_prompt: str = "可愛いウサギが好きですか?" if USE_QUICK_PROMPT else ""
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION
    terse: bool = False
    voice: str = get_random_voice()
    warning: str = ""

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
        assert index < len(self.prompts_responses)
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
        assert index < len(self.prompts_responses)
        assert len(self.edited_prompt.strip()) > 0
        self.new_prompt = self.edited_prompt
        self.prompts_responses = self.prompts_responses[:index]
        self.is_editing = False
        return State.chatgpt

    def cancel_edit_prompt(self, index: int) -> None:
        assert index < len(self.prompts_responses)
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
    async def chatgpt(self) -> AsyncGenerator[None, None]:
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

                if len(self.prompts_responses) == 0:
                    self.voice = get_random_voice()

                prompt_response = PromptResponse(
                    prompt=self.new_prompt,
                    response="",
                    is_editing=False,
                    contains_japanese=False,
                    tts_in_progress=False,
                    has_tts=False,
                    tts_wav_url="",
                    model=model,
                    voice="",
                )
                self.prompts_responses.append(prompt_response)
                self.new_prompt = ""

                print(
                    f"GPT4? {self.gpt_4}\n"
                    f"Terse? {self.terse}\n"
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
                        self.prompts_responses[-1].contains_japanese = (
                            contains_japanese(self.prompts_responses[-1].response)
                        )
                    if not self.is_processing:
                        # It's been cancelled.
                        self.prompts_responses[-1].response += " (cancelled)"
                        break

        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.is_processing = False

        async with self:
            if self.prompts_responses[-1].contains_japanese and self.auto_speak:
                self.prompts_responses[-1].tts_in_progress = True
            yield
            async with self:
                if self.prompts_responses[-1].contains_japanese and self.auto_speak:
                    try:
                        index = len(self.prompts_responses) - 1
                        self.do_speak(
                            index,
                            strip_non_japanese_split_sentences(
                                self.prompts_responses[index].response
                            ),
                        )
                    finally:
                        async with self:
                            self.prompts_responses[-1].tts_in_progress = False

    def cancel_chatgpt(self) -> None:
        self.is_processing = False

    def clear_chat(self) -> None:
        self.prompts_responses = []
        # self.invariant()

    @rx.background  # type: ignore
    async def speak(self, index: int, text: str) -> AsyncGenerator[None, None]:
        async with self:
            self.prompts_responses[index].tts_in_progress = True
        yield
        async with self:
            try:
                self.do_speak(index, strip_non_japanese_split_sentences(text))
            finally:
                async with self:
                    self.prompts_responses[index].tts_in_progress = False

    def do_speak(self, index: int, text: str) -> None:
        """
        Non-async version to call from the async rx.background handlers.
        """
        assert self.voice != ""
        assert index < len(self.prompts_responses)
        try:
            print(f"Speaking: {text}")
            tts_wav_filename = text_to_wav(text, self.voice)
            # Take advantage of a moment for the Nginx to make the wav available
            # by doing some housekeeping.
            delete_old_wav_assets()
            tts_wav_url = os.path.join(
                config.frontend_path, f"{tts_wav_filename[len('assets/'):]}"
            )
            full_tts_wav_url = urljoin(site_runtime_assets_url, tts_wav_url)
            print(f"Checking that {full_tts_wav_url} is being served...", end="")
            for _ in range(0, 10):
                try:
                    response = requests.head(full_tts_wav_url, timeout=10.0)
                    if response.status_code >= 200 and response.status_code < 400:
                        print("OK")
                        self.prompts_responses[index].tts_wav_url = tts_wav_url
                        self.prompts_responses[index].voice = self.voice
                        # This causes the rx.audio to be rendered, at which
                        # point we know for sure it has a working url.
                        self.prompts_responses[index].has_tts = True
                        return
                except Exception as ex:  # pylint: disable=broad-exception-caught
                    self.warning = str(ex)
                    print(self.warning)
                else:
                    self.warning = ""
                time.sleep(0.25)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            self.warning = str(ex)
            print(self.warning)
        else:
            print("NOT OK")
            self.warning = (
                "Some problem prevented the audio from being available to play."
            )
            print(self.warning)

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
