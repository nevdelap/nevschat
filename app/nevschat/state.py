# mypy: disable-error-code="attr-defined,name-defined"

import asyncio
import logging
import re
import time
from typing import Any

from openai import OpenAI

import reflex as rx
from nevschat.canned_chat import get_canned_chat
from nevschat.helpers import ENGLISH
from nevschat.helpers import FRENCH
from nevschat.helpers import contains_japanese
from nevschat.helpers import contains_kanji
from nevschat.helpers import contains_non_japanese
from nevschat.helpers import get_default_voice
from nevschat.helpers import get_definition
from nevschat.helpers import get_kanji
from nevschat.helpers import get_translation
from nevschat.helpers import strip_spaces_in_japanese
from nevschat.learning_aide import LearningAide
from nevschat.profile import Profile
from nevschat.prompt import Prompt
from nevschat.prompt_response import PromptResponse
from nevschat.response import Response
from nevschat.speakable import Speakable
from nevschat.system_instructions import CHECK_GRAMMAR
from nevschat.system_instructions import EXPLAIN_GRAMMAR
from nevschat.system_instructions import EXPLAIN_USAGE
from nevschat.system_instructions import EXPRESS_OPPOSITE_MEANING
from nevschat.system_instructions import EXPRESS_SAME_MEANING
from nevschat.system_instructions import GIVE_EXAMPLE_SENTENCES
from nevschat.system_instructions import get_system_instructions

SYSTEM_INSTRUCTIONS = get_system_instructions()
DEFAULT_SYSTEM_INSTRUCTION = 'English'

GPT_BEST_MODEL = 'gpt-4.1'
GTP_CHEAP_MODEL = 'gpt-4.1-nano'

# Requires a restart when changing.
USE_CANNED_PROFILE_AND_CHAT = False  # For testing.
USE_QUICK_PROMPT = False  # For testing.


def log(msg: str = '') -> None:
    """
    Log basic info.
    """
    logging.info(msg=msg)


class State(rx.State):
    ####################################################################################
    # State

    prompts_responses: list[PromptResponse] = (
        get_canned_chat() if USE_CANNED_PROFILE_AND_CHAT else []
    )
    auto_speak: bool = True
    chat_processing: bool = False
    control_down: bool = False
    edited_prompt: str
    gpt_best: bool = True
    learning_aide: LearningAide = LearningAide()
    learning_aide_processing: bool = False
    new_prompt: str = '可愛いウサギが好きですか?' if USE_QUICK_PROMPT else ''
    non_profile_voice: str = get_default_voice()
    profile: Profile = Profile(canned=USE_CANNED_PROFILE_AND_CHAT)
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION
    terse: bool = True
    tts_processing: bool = False
    warning: str

    # These @rx.vars that just call a method on a property or do an operation
    # with a property that is an rx.Base are because @rx.vars in those classes
    # do no propagate, at least as of Reflex v0.4.9 as far as I've been able to
    # discover. When I discover otherwise hopefully these can be moved into
    # methods in those classes marked @rx.var.

    @rx.var(cache=True)
    def cannot_chatgpt_with_new_prompt(self) -> bool:
        return self.editing or len(self.new_prompt.strip()) == 0

    @rx.var(cache=True)
    def cannot_clear_chat(self) -> bool:
        return len(self.prompts_responses) == 0

    @rx.var(cache=True)
    def cannot_clear_or_chatgpt_with_edited_prompt(self) -> bool:
        return len(self.edited_prompt.strip()) == 0

    @rx.var(cache=True)
    def cannot_enter_new_prompt_or_edit(self) -> bool:
        return self.editing or self.chat_processing

    @rx.var(cache=True)
    def editing(self) -> bool:
        return any(
            prompt_response.editing for prompt_response in self.prompts_responses
        )

    def editing_index(self) -> int | None:
        for index, prompt_response in enumerate(self.prompts_responses):
            if prompt_response.editing:
                return index
        return None

    @rx.var(cache=True)
    def has_prompts_responses(self) -> bool:
        return len(self.prompts_responses) > 0

    @rx.var(cache=True)
    def using_profile_in_prompts(self) -> bool:
        """
        'Using' the profile means the profile is shown to the user and is
        included in the chat prompts. If not 'using' it for that purpose the
        profile voice is still used for spoken responses.
        """
        return self.system_instruction == 'ランダムな人'

    @rx.var(cache=True)
    def you_are(self) -> str:
        return self.profile.text.replace('私', 'あなた')

    def cancel_chat_processing(self) -> None:
        self.chat_processing = False

    def cancel_learning_aide_processing(self) -> None:
        self.learning_aide_processing = False

    ####################################################################################
    # Profile

    def change_profile(self) -> None:
        self.profile.clear()
        # TODO: Investigate if this indicates a bug in Reflex or not. It used to
        # be that these assignments were necessary to trigger UI state changes
        # but I thought it wasn't the case anymore. It might be because it is
        # two levels deep.
        self.profile.text = self.profile.text
        for prompt_response in self.prompts_responses:
            prompt_response.response.tts_wav_url = ''
            prompt_response.response.pitch = self.profile.pitch
            prompt_response.response.speaking_rate = self.profile.speaking_rate
            prompt_response.response.voice = self.profile.voice

    ####################################################################################
    # System Instruction

    @rx.event(background=True)
    async def set_system_instruction(self, system_instruction: str) -> Any:
        async with self:
            self.system_instruction = system_instruction
            self.change_profile()
        # This needs to run in the background so that when this ultimately runs
        # it is after the UI has updated and shown the buttons that it will
        # disable.
        return State.trigger_clear_learning_aide_prompt

    ####################################################################################
    # Prompt Editing

    def edit_prompt(self, index: int) -> None:
        assert index < len(self.prompts_responses)
        self.edited_prompt = self.prompts_responses[index].prompt.text
        self.prompts_responses[index].editing = True
        self.editing = True
        # self.issue1675()

    def update_edited_prompt(self, prompt: str) -> None:
        self.edited_prompt = prompt

    def clear_chat(self) -> Any:
        self.prompts_responses = []
        self.change_profile()
        return self.trigger_clear_learning_aide_prompt()

    def clear_edited_prompt(self) -> None:
        self.edited_prompt = ''

    def clear_new_prompt(self) -> None:
        self.new_prompt = ''

    def chatgpt_with_edited_prompt(self, index: int) -> Any:
        assert index < len(self.prompts_responses)
        assert len(self.edited_prompt.strip()) > 0
        self.new_prompt = self.edited_prompt
        self.prompts_responses = self.prompts_responses[:index]
        self.editing = False
        return State.chatgpt

    def cancel_edit_prompt(self, index: int) -> None:
        assert index < len(self.prompts_responses)
        self.edited_prompt = ''
        self.prompts_responses[index].editing = False
        self.editing = False

    def handle_key_down(self, key: str) -> Any:
        if key == 'Control':
            self.control_down = True
        elif key == 'Enter' and self.control_down:
            if self.editing:
                index = self.editing_index()
                if index is None:
                    raise RuntimeError('If editing, the editing_index cannot be None.')
                return self.chatgpt_with_edited_prompt(index)
            return State.chatgpt
        return None

    def handle_key_up(self, key: str) -> None:
        if key == 'Control':
            self.control_down = False

    def cancel_control(self, _text: str = '') -> None:
        self.control_down = False

    ####################################################################################
    # ChatGPT

    @rx.event(background=True)
    async def chatgpt(self) -> Any:
        try:
            async with self:
                assert self.new_prompt != ''

                self.cancel_control()
                self.chat_processing = True
                self.warning = ''

                model = GPT_BEST_MODEL if self.gpt_best else GTP_CHEAP_MODEL
                messages = []

                if self.terse:
                    messages.append(
                        {
                            'role': 'system',
                            'content': (
                                'Give terse responses without extra explanation.'
                            ),
                        }
                    )

                system_instruction, code_related = SYSTEM_INSTRUCTIONS[
                    self.system_instruction
                ]

                if self.using_profile_in_prompts:  # pylint: disable=using-constant-test
                    system_instruction = system_instruction.format(you_are=self.you_are)

                system_instruction = re.sub(r'\s+', ' ', system_instruction).strip()

                messages.append({'role': 'system', 'content': system_instruction})
                if code_related:
                    messages.append(
                        {
                            'role': 'system',
                            'content': (
                                'All responses with code examples MUST '
                                + 'wrap the code examples in triple backticks.'
                            ),
                        }
                    )

                for prompt_response in self.prompts_responses:
                    messages.append(
                        {'role': 'user', 'content': prompt_response.prompt.text}
                    )
                    messages.append(
                        {'role': 'assistant', 'content': prompt_response.response.text}
                    )
                messages.append({'role': 'user', 'content': self.new_prompt})

                prompt_response = PromptResponse(
                    prompt=Prompt(
                        text=self.new_prompt,
                        contains_japanese=contains_japanese(self.new_prompt),
                        contains_non_japanese=contains_non_japanese(self.new_prompt),
                    ),
                    response=Response(
                        model=model,
                        pitch=self.profile.pitch,
                        speaking_rate=self.profile.speaking_rate,
                        voice=self.profile.voice,
                        text='\u00a0',  # Non-breaking space.
                    ),
                    editing=False,
                )
                self.prompts_responses.append(prompt_response)
                self.new_prompt = ''

                print(
                    f'GPT Best Model? {self.gpt_best}\n'
                    f'Terse? {self.terse}\nMessages: {messages}'
                )

            async with self:
                if (
                    # The user may have cleared the chat.
                    len(self.prompts_responses) > 0
                    and not self.prompts_responses[-1].prompt.contains_non_japanese
                    and self.auto_speak
                ):
                    self.learning_aide.model = GPT_BEST_MODEL
                    self.learning_aide.system_instruction = (
                        SYSTEM_INSTRUCTIONS[CHECK_GRAMMAR][0]
                        + " IF THE GRAMMAR IS CORRECT JUST REPLY '<OK>'"
                    )
                    self.learning_aide.prompt = self.prompts_responses[-1].prompt.text
                    yield State.chatgpt_learning_aide
                    yield State.speak_last_prompt

            session = OpenAI(
                timeout=10.0,
            ).chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
                stream=True,  # Enable streaming
            )

            # pylint error: https://github.com/openai/openai-python/issues/870
            for item in session:  # pylint: disable=not-an-iterable
                async with self:
                    response = item.choices[0].delta.content  # type: ignore
                    # The user may have cleared the chat.
                    if len(self.prompts_responses) == 0:
                        break
                    if response:
                        # The non-breaking space is used to make the markdown
                        # component render as if it had something in it, until
                        # it does, without being visible to the user.
                        if self.prompts_responses[-1].response.text == '\u00a0':
                            self.prompts_responses[-1].response.text = ''
                        self.prompts_responses[-1].response.text += response
                        self.prompts_responses[
                            -1
                        ].response.contains_japanese = contains_japanese(
                            self.prompts_responses[-1].response.text
                        )
                    if not self.chat_processing:
                        # It's been cancelled.
                        self.prompts_responses[-1].response.text += ' (キャンセル）'
                        break
                    yield

        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.chat_processing = False

        # Hacky temporary solution until I make it wait for the spoken prompt to
        # have completed playing before playing the response - properly. Assume
        # a characters per second speaking rate and adjust for the actual
        # speaking rate.
        characters_per_second = 6
        await asyncio.sleep(
            len(self.prompts_responses[-1].prompt.text)
            / characters_per_second
            / self.prompts_responses[-1].prompt.speaking_rate
        )
        async with self:
            if (
                len(self.prompts_responses) > 0  # The user may have cleared the chat.
                and self.prompts_responses[-1].response.contains_japanese
                and self.auto_speak
            ):
                yield State.speak_last_response

    ####################################################################################
    # Text To Speech

    @rx.event(background=True)
    async def speak_profile(self) -> Any:
        async with self:
            self.profile.tts_in_progress = True
            yield
        async with self:
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.profile, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def speak_prompt(self, index: int) -> Any:
        async with self:
            self.prompts_responses[index].prompt.tts_in_progress = True
            yield
        async with self:
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.prompts_responses[index].prompt, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def speak_response(self, index: int) -> Any:
        async with self:
            self.prompts_responses[index].response.tts_in_progress = True
            yield
        async with self:
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.prompts_responses[index].response, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def speak_last_prompt(self) -> Any:
        async with self:
            if len(self.prompts_responses) == 0:  # The user may have cleared the chat.
                return
            self.prompts_responses[-1].prompt.tts_in_progress = True
            yield
        async with self:
            if len(self.prompts_responses) == 0:  # The user may have cleared the chat.
                return
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.prompts_responses[-1].prompt, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def speak_last_response(self) -> Any:
        async with self:
            if len(self.prompts_responses) == 0:  # The user may have cleared the chat.
                return
            self.prompts_responses[-1].response.tts_in_progress = True
            yield
        async with self:
            if len(self.prompts_responses) == 0:  # The user may have cleared the chat.
                return
            # Wait for the prompt to finish tts'ing.
            while self.tts_processing:
                yield
                time.sleep(0.5)
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.prompts_responses[-1].response, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def speak_learning_aide(self) -> Any:
        async with self:
            self.learning_aide.tts_in_progress = True
            yield
        async with self:
            self.tts_processing = True
            try:
                Speakable.text_to_wav(self.learning_aide, self)
            finally:
                self.tts_processing = False

    @rx.event(background=True)
    async def play_from_profile(self) -> Any:
        print('Play from here - profile')
        return rx.call_script(
            'play_from_here("audio_profile")',
        )

    @rx.event(background=True)
    async def play_from_here(self, audio_id: str) -> Any:
        print(f'Play from here - {audio_id}')
        return rx.call_script(
            f'play_from_here("{audio_id}")',
        )

    @rx.event(background=True)
    async def disable_autoplay(self, audio_id: str) -> Any:
        print(f'Disable autoplay - {audio_id}')
        return rx.call_script(
            f'disable_autoplay("{audio_id}")',
        )

    ####################################################################################
    # Learning Aide

    def clear_learning_aide_prompt(self, _: Any = None) -> None:
        self.learning_aide.clear()

    def lookup_definition(self) -> Any:
        log()
        return self.do_dictionary_learning_aide()

    def lookup_kanji(self) -> Any:
        log()
        return self.do_kanji_learning_aide()

    def translate(self) -> Any:
        log()
        try:
            return self.do_deepl_learning_aide(ENGLISH)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            self.warning = str(ex)
            print(self.warning)
            return self.do_chatgpt_learning_aide(
                GTP_CHEAP_MODEL,
                (
                    'Translate the given Japanese text into English. '
                    + 'NEVER give pronunciation. NEVER give romaji.'
                ),
            )

    def translate_to_french(self) -> Any:
        log()
        try:
            return self.do_deepl_learning_aide(FRENCH)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            self.warning = str(ex)
            print(self.warning)
            return self.do_chatgpt_learning_aide(
                GTP_CHEAP_MODEL,
                (
                    'Traduisez le texte japonais donné en anglais.'
                    + 'Ne donnez JAMAIS la prononciation. NE JAMAIS donner le romaji.'
                ),
            )

    def check_grammar(self) -> Any:
        log()
        self.learning_aide.expects_japanese = True
        return self.do_chatgpt_learning_aide(
            GPT_BEST_MODEL,
            SYSTEM_INSTRUCTIONS[CHECK_GRAMMAR][0]
            + " IF THE GRAMMAR IS CORRECT JUST REPLY 'The grammar is correct.'",
        )

    def explain_grammar(self) -> Any:
        log()
        self.learning_aide.expects_japanese = True
        return self.do_chatgpt_learning_aide(
            GPT_BEST_MODEL, SYSTEM_INSTRUCTIONS[EXPLAIN_GRAMMAR][0]
        )

    def explain_usage(self) -> Any:
        log()
        self.learning_aide.expects_japanese = True
        return self.do_chatgpt_learning_aide(
            GTP_CHEAP_MODEL, SYSTEM_INSTRUCTIONS[EXPLAIN_USAGE][0]
        )

    def give_examples_of_same_meaning(self) -> Any:
        log()
        self.learning_aide.expects_japanese = False
        return self.do_chatgpt_learning_aide(
            GTP_CHEAP_MODEL,
            SYSTEM_INSTRUCTIONS[EXPRESS_SAME_MEANING][0],
        )

    def give_examples_of_opposite_meaning(self) -> Any:
        log()
        self.learning_aide.expects_japanese = False
        return self.do_chatgpt_learning_aide(
            GTP_CHEAP_MODEL,
            SYSTEM_INSTRUCTIONS[EXPRESS_OPPOSITE_MEANING][0],
        )

    def give_example_sentences(self) -> Any:
        log()
        self.learning_aide.expects_japanese = False
        return self.do_chatgpt_learning_aide(
            GTP_CHEAP_MODEL,
            SYSTEM_INSTRUCTIONS[GIVE_EXAMPLE_SENTENCES][0],
        )

    ####################################################################################
    # Dictionary Learning Aide

    def do_dictionary_learning_aide(self) -> Any:
        return self.trigger_set_dictionary_learning_aide_prompt()

    def trigger_set_dictionary_learning_aide_prompt(self) -> Any:
        return rx.call_script(
            'get_selected_text_and_clear()',
            callback=State.set_dictionary_learning_aide_prompt,
        )

    @rx.event(background=True)
    async def set_dictionary_learning_aide_prompt(self, text: str) -> Any:
        async with self:
            self.learning_aide.prompt = text
        return State.dictionary_learning_aide

    @rx.event(background=True)
    async def dictionary_learning_aide(self) -> Any:
        try:
            async with self:
                self.learning_aide_processing = True
                self.warning = ''
                self.learning_aide.model = ''
                self.learning_aide.text = '見つけ中…'
                self.learning_aide.has_tts = False
                self.learning_aide.tts_wav_url = ''
            yield
            async with self:
                definition, model = get_definition(self.learning_aide.prompt)
                yield
                self.learning_aide.model = model
                self.learning_aide.text = ''
                if definition is not None:
                    for ch in definition:
                        self.learning_aide.text += ch
                        self.learning_aide.contains_japanese = contains_japanese(
                            definition
                        )
                        yield
                        if not self.learning_aide_processing:
                            # It's been cancelled.
                            self.learning_aide.text += ' (キャンセル）'
                            break
        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.learning_aide_processing = False

    ####################################################################################
    # Kanji Learning Aide

    def do_kanji_learning_aide(self) -> Any:
        return self.trigger_set_kanji_learning_aide_prompt()

    def trigger_set_kanji_learning_aide_prompt(self) -> Any:
        return rx.call_script(
            'get_selected_text_and_clear()',
            callback=State.set_kanji_learning_aide_prompt,
        )

    @rx.event(background=True)
    async def set_kanji_learning_aide_prompt(self, text: str) -> Any:
        async with self:
            self.learning_aide.prompt = text
        return State.kanji_learning_aide

    @rx.event(background=True)
    async def kanji_learning_aide(self) -> Any:
        try:
            async with self:
                self.learning_aide_processing = True
                self.warning = ''
                self.learning_aide.model = ''
                self.learning_aide.text = '見つけ中…'
                self.learning_aide.has_tts = False
                self.learning_aide.tts_wav_url = ''
            yield
            async with self:
                if not contains_kanji(self.learning_aide.prompt):
                    self.learning_aide.text = 'テキストには漢字がない。'
                else:
                    kanji, model = get_kanji(self.learning_aide.prompt)
                    yield
                    self.learning_aide.model = model
                    self.learning_aide.text = ''
                    if kanji is not None:
                        for ch in kanji:
                            self.learning_aide.text += ch
                            self.learning_aide.contains_japanese = contains_japanese(
                                kanji
                            )
                            yield
                            if not self.learning_aide_processing:
                                # It's been cancelled.
                                self.learning_aide.text += ' (キャンセル）'
                                break
        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.learning_aide_processing = False

    ####################################################################################
    # DeepL Learning Aide

    def do_deepl_learning_aide(self, target_lang: str) -> Any:
        self.learning_aide.target_lang = target_lang
        return self.trigger_set_deepl_learning_aide_prompt()

    def trigger_set_deepl_learning_aide_prompt(self) -> Any:
        return rx.call_script(
            'get_selected_text_and_clear()',
            callback=State.set_deepl_learning_aide_prompt,
        )

    @rx.event(background=True)
    async def set_deepl_learning_aide_prompt(self, text: str) -> Any:
        async with self:
            self.learning_aide.prompt = text
        return State.deepl_learning_aide

    @rx.event(background=True)
    async def deepl_learning_aide(self) -> Any:
        try:
            async with self:
                self.learning_aide_processing = True
                self.warning = ''
                self.learning_aide.model = 'deepl'
                self.learning_aide.text = '翻訳中…'
                self.learning_aide.has_tts = False
                self.learning_aide.tts_wav_url = ''
            yield
            async with self:
                if self.learning_aide.prompt == '':
                    self.learning_aide.text = 'テキストはない。'
                else:
                    translation = get_translation(
                        self.learning_aide.prompt,
                        target_lang=self.learning_aide.target_lang,
                    )
                    yield
                    self.learning_aide.text = ''
                    if translation is not None:
                        for ch in translation:
                            self.learning_aide.text += ch
                            self.learning_aide.contains_japanese = contains_japanese(
                                translation
                            )
                            yield
                            if not self.learning_aide_processing:
                                # It's been cancelled.
                                self.learning_aide.text += ' (キャンセル）'
                                break
        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.learning_aide_processing = False

    ####################################################################################
    # ChatGPT Learning Aide

    def do_chatgpt_learning_aide(self, model: str, system_instruction: str) -> Any:
        self.learning_aide.model = model
        self.learning_aide.system_instruction = system_instruction
        return self.trigger_set_chatgpt_learning_aide_prompt()

    def trigger_set_chatgpt_learning_aide_prompt(self) -> Any:
        return rx.call_script(
            'get_selected_text_and_clear()',
            callback=State.set_chatgpt_learning_aide_prompt,
        )

    @rx.event(background=True)
    async def set_chatgpt_learning_aide_prompt(self, text: str) -> Any:
        async with self:
            self.learning_aide.prompt = text
        return State.chatgpt_learning_aide

    @rx.event(background=True)
    async def chatgpt_learning_aide(self) -> Any:
        try:
            async with self:
                learning_aide_system_instruction = self.learning_aide.system_instruction
                learning_aid_prompt = strip_spaces_in_japanese(
                    self.learning_aide.prompt
                )
                model = self.learning_aide.model
                learning_aide_system_instruction = re.sub(
                    r'\s+', ' ', learning_aide_system_instruction
                ).strip()
                if learning_aid_prompt != '':
                    self.learning_aide_processing = True
                    self.warning = ''
                    self.learning_aide.text = ''
                    self.learning_aide.contains_japanese = False
                    self.learning_aide.tts_wav_url = ''
            yield
            async with self:
                if self.learning_aide.expects_japanese and not contains_japanese(
                    self.learning_aide.prompt
                ):
                    self.learning_aide.text = 'テキストは日本語だけではない。'
                else:
                    messages = [
                        {
                            'role': 'system',
                            'content': learning_aide_system_instruction,
                        },
                        {'role': 'user', 'content': learning_aid_prompt},
                    ]
                    print(f'Model: {model}\nMessages: {messages}')
                    session = OpenAI(
                        timeout=10.0,
                    ).chat.completions.create(
                        model=model,
                        messages=messages,  # type: ignore
                        stream=True,  # Enable streaming
                    )
                    # pylint error: https://github.com/openai/openai-python/issues/870
                    for item in session:  # pylint: disable=not-an-iterable
                        response = item.choices[0].delta.content  # type: ignore
                        if response:
                            self.learning_aide.text += response
                            self.learning_aide.contains_japanese = contains_japanese(
                                self.learning_aide.text
                            )
                            if self.learning_aide.text == '<OK>':
                                # No need to show it.
                                self.learning_aide.text = ''
                        if not self.learning_aide_processing:
                            # It's been cancelled.
                            self.learning_aide.text += ' (キャンセル）'
                            break
                        yield
        except Exception as ex:  # pylint: disable=broad-exception-caught
            async with self:
                self.warning = str(ex)
                print(self.warning)
        finally:
            async with self:
                self.learning_aide_processing = False

    def clear_learning_aide_response(self) -> Any:
        return self.trigger_clear_learning_aide_prompt()

    def trigger_clear_learning_aide_prompt(self, _: Any = None) -> Any:
        return rx.call_script(
            'get_selected_text_and_clear()',
            callback=State.clear_learning_aide_prompt,
        )
