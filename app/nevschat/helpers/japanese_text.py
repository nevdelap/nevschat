import re
import unicodedata


def is_japanese_char(
    ch: str, *, include_digits_and_punctuation: bool = True, log: bool = False
) -> bool:
    """
    Return True if the character is a Japanese character.
    """
    assert len(ch) == 1
    included_blocks = [
        'CJK',
        'FULLWIDTH',
        'HIRAGANA',
        'IDEOGRAPHIC',
        'KATAKANA',
        'KATAKANA-HIRAGANA',
    ]
    if include_digits_and_punctuation:
        included_blocks.extend(
            [
                'DIGIT',
                'LEFT',
                'RIGHT',
            ]
        )
    try:
        block = unicodedata.name(ch).split()[0]
        is_japanese = block in included_blocks
        if log:
            print(ch, block, 'J' if is_japanese else '')
        return is_japanese
    except ValueError:
        return False


def is_kanji(ch: str, *, log: bool = False) -> bool:
    """
    Return True if the character is a kanji.
    """
    assert len(ch) == 1
    try:
        block = unicodedata.name(ch).split()[0]
        is_kanji = block == 'CJK'
        if log:
            print(ch, block, 'K' if is_kanji else '')
        return is_kanji
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
            'LATIN',
        ]
        if log:
            print(ch, block, 'L' if is_latin else '')
        return is_latin
    except ValueError:
        return False


def contains_japanese(text: str, *, log: bool = False) -> bool:
    """
    Return True if the text contains any Japanese at all.
    """
    return any(
        is_japanese_char(ch, include_digits_and_punctuation=False, log=log)
        for ch in text
    )


def contains_kanji(text: str, *, log: bool = False) -> bool:
    """
    Return True if the text contains any kanji.
    """
    return any(is_kanji(ch, log=log) for ch in text)


def contains_latin(text: str, log: bool = False) -> bool:
    """
    Return True if the text contains any Latin characters at all.
    """
    return any(is_latin_char(ch, log) for ch in text)


def strip_non_japanese_and_split_sentences(text: str) -> str:
    """
    If the text contains non-Japanese characters from the text, insert 。
    between pieces of Japanese that were separated by non-Japanese to make the
    tts insert a pause rather then running them all together, and remove
    consecutive duplicate sentences.
    """
    if contains_latin(text):
        text = re.sub(
            r'。+',
            '。',
            ''.join(
                ch
                if is_japanese_char(ch, include_digits_and_punctuation=True)
                else '。'
                for ch in text
            )
            + '。',
        ).lstrip('。')
        while True:
            old_len = len(text)
            text = re.sub(r'([^、。]*[、。])\1', r'\1', text)
            if len(text) == old_len:
                break
    return text


# Built-in test.
def test_strip_non_japanese_split_sentence(original: str, expected: str) -> None:
    stripped = strip_non_japanese_and_split_sentences(original)
    assert stripped == expected, f'{original}: {stripped} != {expected}'


for original, expected in [
    # If mixed Japanese and Latin, strip Latin characters.
    (
        "Both '異る' and '違う' are verbs in Japanese that can be translated as "
        "'to differ' or 'to be different'. '異る' carries a stronger connotation "
        'of being unusual, rare, or significant in its difference compared to '
        'something else.',
        '異る。違う。異る。',
    ),
    # If only Japanese leave as is.
    ('おんな、おんな、', 'おんな、おんな、'),
    # If mixed Japanese and Latin, strip Latin characters and duplication.
    ('おんな、おんな、is Japanese.', 'おんな、。'),
    # If mixed Japanese and Latin, strip Latin characters and duplication.
    ('違う。違う。違う。hello.違う。違う。', '違う。'),
    # If mixed Japanese and Latin, add 。 between pieces of Japanese.
    ('日本語あるハー「」。、ab, ()1', '日本語あるハー「」。、。()1。'),
]:
    test_strip_non_japanese_split_sentence(original, expected)


def strip_spaces_in_japanese(text: str) -> str:
    """
    Voice input on Android insists on putting spaces in spoken Japanese, and
    then ChatGPT complains about it when checking grammar, even when told to
    ignore it. So strip it out. Rather than trying to make a regex that does it
    reliably, use the unicodedata functionality that we already have. It is
    stripping spaces only between Japanese characters so that it can be used on
    mixed texts.
    """
    result = ''
    previous_is_japanese = False
    maybe_keep_spaces = ''
    for ch in text:
        if ch.isspace() and previous_is_japanese:
            maybe_keep_spaces += ch
            continue
        if is_japanese_char(ch):
            previous_is_japanese = True
        else:
            previous_is_japanese = False
            result += maybe_keep_spaces
        maybe_keep_spaces = ''
        result += ch
    return result


# Built-in test.
def test_strip_spaces_in_japanese(original: str, expected: str) -> None:
    stripped = strip_spaces_in_japanese(original)
    assert stripped == expected, f'{original}: {stripped} != {expected}'


for original, expected in [
    ('猫は怖いいです。 鶏は臭いです。', '猫は怖いいです。鶏は臭いです。'),
    ('猫は怖いいです。  鶏は臭いです。', '猫は怖いいです。鶏は臭いです。'),
    (
        'hello猫は怖いいです。  鶏は臭いです。there',
        'hello猫は怖いいです。鶏は臭いです。there',
    ),
    (
        'hello 猫は怖いいです。  鶏は臭いです。there',
        'hello 猫は怖いいです。鶏は臭いです。there',
    ),
    (
        'hello 猫は怖いいです。  鶏は臭いです。there ',
        'hello 猫は怖いいです。鶏は臭いです。there ',
    ),
    (
        'hello 猫は怖いいです。 waa! 鶏は臭いです。there ',
        'hello 猫は怖いいです。 waa! 鶏は臭いです。there ',
    ),
    (
        'h  ell o  猫は怖   いいです。 wa a!   鶏は臭 いです。 there   ',
        'h  ell o  猫は怖いいです。 wa a!   鶏は臭いです。 there   ',
    ),
]:
    test_strip_spaces_in_japanese(original, expected)


def age_to_kanji(age: int) -> str:
    kanji_numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    if age == 0:
        return kanji_numbers[age]
    tens = age // 10
    ones = age % 10
    return (
        (kanji_numbers[tens] if age >= 20 else '')
        + (kanji_numbers[10] if age >= 10 else '')
        + (kanji_numbers[ones] if ones > 0 else '')
    )


def test_age_to_kanji(age: int, expected: str) -> None:
    kanji = age_to_kanji(age)
    assert kanji == expected, f'{age}: {kanji} != {expected}'


test_age_to_kanji(0, '零')
test_age_to_kanji(1, '一')
test_age_to_kanji(7, '七')
test_age_to_kanji(10, '十')
test_age_to_kanji(16, '十六')
test_age_to_kanji(40, '四十')
test_age_to_kanji(44, '四十四')
test_age_to_kanji(50, '五十')
