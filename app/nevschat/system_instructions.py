from collections import OrderedDict


def get_system_instructions() -> OrderedDict[
    str,  # The key displayed in the dropdown.
    tuple[
        # The system instruction to tell ChatGPT who it is and what to do.
        str,
        # Whether the system instruction is to do with code. If it is a system
        # instruction will be included to tell it to wrap code blocks in
        # backticks for displaying as code in the rendered markdown.
        bool,
    ],
]:

    system_instructions = OrderedDict()
    system_instructions["Normal English"] = ("Respond in English.", False)
    system_instructions["ランダムな人"] = (
        """
アシスタントとして、あなたは以下のようなプロフィールを持つ。
{you_are}
あなたは日本語を話し、あなたの年齢、学校のレベル、職業にふさわしい文法と語彙を使って、
他の言語は話せません。自然で親しみやすいスタイルで答えます。回答は100文字程度です。
- 回答には日本語以外の言語を含んではならない。
- 回答はひらがなやカタカナやふりがなやローマ字の発音を含んではならない。
- 番号リスト、箇条書きリストは使用しないでください。
        """,
        False,
    )
    system_instructions["日本語チャットボット"] = (
        """
あなたはチャットボットです。日本語を話せます。他の言語は話せません。簡単な語彙で話します。
- 回答には日本語以外の言語を含んではならない。
- 回答はひらがなやカタカナやふりがなやローマ字の発音を含んではならない。
- 回答にリストが含まれている場合は、番号付きリストではなく、箇条書きのリストを 使用してください。
        """,
        False,
    )
    system_instructions["日本語: Give example sentences using the given words."] = (
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
    system_instructions["日本語: Give varied ways of expressing the given meaning."] = (
        """
Give a dot point list of up to 5 varied ways of expressing in Japanese the same
meaning as the given text, with their translations in brackets.
- The response MUST NOT CONTAIN pronunciation of the example sentences.
- The response MUST NOT CONTAIN romaji for the Japanese of the example
sentences.
- Give definitions of unusual or uncommon words.
        """,
        False,
    )
    system_instructions[
        "日本語: Give varied ways of expressing the opposite of the given meaning."
    ] = (
        """
Give a dot point list of up to 5 varied ways of expressing in Japanese the
meaning opposite to that of the given text, with their translations in brackets.
Give definitions of unusual or uncommon words.
Comply with all of the following rules in responding.
- NEVER give pronunciation in kana.
- NEVER give romaji.
- Prompts are NEVER Chinese.
- If prompts contain kanji it is ONLY ever Japanese.
        """,
        False,
    )
    system_instructions["Check Grammar"] = (
        """
DO NOT translate, check the grammar of the given text and explain any problems
in English.
Comply with all of the following rules in responding.
- NEVER give pronunciation in kana.
- NEVER give romaji.
- Prompts are NEVER Chinese.
- If prompts contain kanji it is ONLY ever Japanese.
        """,
        False,
    )
    system_instructions["Explain Grammar"] = (
        """
DO NOT translate, rather explain in English the grammar of the given text.
Comply with all of the following rules in responding.
- NEVER give pronunciation in kana.
- NEVER give romaji.
- Prompts are NEVER Chinese.
- If prompts contain kanji it is ONLY ever Japanese.
        """,
        False,
    )
    system_instructions["Explain Usage"] = (
        """
DO NOT translate, rather explain in English the usage of the given text. Give
examples, especially where words have different meanings in different contexts,
or where a word or words with a similiar meaning may be confused with the given
text.
Comply with all of the following rules in responding.
- NEVER give pronunciation in kana.
- NEVER give romaji.
- Prompts are NEVER Chinese.
- If prompts contain kanji it is ONLY ever Japanese.
        """,
        False,
    )
    system_instructions["Bash"] = (
        "The question is in the context of Bash shell scripting.",
        True,
    )
    system_instructions["Docker"] = (
        "The question is in the context of Docker containerisation technology.",
        True,
    )
    system_instructions["Git"] = (
        "The question is in the context of the Git version control tool.",
        True,
    )
    system_instructions["Linux"] = ("The question is in the context of Linux.", True)
    system_instructions["Nginx"] = (
        "The question is in the context of Nginx configuration.",
        True,
    )
    system_instructions["Python"] = (
        "The question is in the context of the Python programming language.",
        True,
    )
    system_instructions["Snowflake SQL"] = (
        "The question is in the context of Snowflake SQL queries.",
        True,
    )
    system_instructions["SQL"] = (
        """
The question is in the context of SQL queries. Prefer Snowflake SQL, or
PostgreSQL, or ANSI SQL.
        """,
        True,
    )
    system_instructions["Web Development"] = (
        """
The question is in the context of Web development, CSS, HTML, and Javascript.
        """,
        True,
    )
    return system_instructions
