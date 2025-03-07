import re
import unicodedata


def is_japanese_char(
    ch: str, *, include_digits_and_brackets: bool = True, log: bool = False
) -> bool:
    """
    Return True if the character is a Japanese character, optionally counting digits and
    brackets as Japanese characters.
    """
    assert len(ch) == 1, 'is_japanese_char, len(ch) == 1'
    included_blocks = [
        'CJK',
        'FULLWIDTH',
        'HIRAGANA',
        'IDEOGRAPHIC',
        'KATAKANA',
        'KATAKANA-HIRAGANA',
    ]
    if include_digits_and_brackets:
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


def is_kana_or_kanji_or_digit_or_char(
    ch: str, *, other: str = '', log: bool = False
) -> bool:
    """
    Return True if the character is a Japanese character or digit, excluding
    punctation.
    """
    assert len(ch) == 1, 'is_kana_or_kanji_or_digit, len(ch) == 1'
    included_blocks = [
        'CJK',
        'DIGIT',
        'HIRAGANA',
        'KATAKANA',
        'KATAKANA-HIRAGANA',
    ]
    try:
        if ch in other:
            return True
        block = unicodedata.name(ch).split()[0]
        is_kana_or_kanji = block in included_blocks
        if log:
            print(ch, block, 'J' if is_kana_or_kanji else '')
        return is_kana_or_kanji
    except ValueError:
        return False


# Built-in test.
for ch, other, expected_is in [
    ('か', '', True),
    ('カ', '', True),
    ('今', '', True),
    ('！', '！？', True),
    ('？', '！？', True),
    ('。', '', False),
    ('、', '', False),
    ('1', '', True),
    ('１', '', False),
    ('　', '', False),
    ('a', '', False),
    (',', '', False),
    ('.', '', False),
    (':', '', False),
    (' ', '', False),
]:
    is_ = is_kana_or_kanji_or_digit_or_char(ch, other=other)
    assert is_ == expected_is, f'{ch}: {is_} != {expected_is}'


# Built-in test.
for ch, expected_is in [
    ('か', True),
    ('カ', True),
    ('今', True),
    ('。', True),
    ('、', True),
    ('1', True),
    ('１', True),
    ('　', True),
    ('a', False),
    (',', False),
    ('.', False),
    (':', False),
    (' ', False),
]:
    is_ = is_japanese_char(ch)
    assert is_ == expected_is, f'{ch}: {is_} != {expected_is}'


def is_kanji(ch: str, *, log: bool = False) -> bool:
    """
    Return True if the character is a kanji.
    """
    assert len(ch) == 1, 'is_kanji, len(ch) == 1'
    try:
        block = unicodedata.name(ch).split()[0]
        is_kanji = block == 'CJK'
        if log:
            print(ch, block, 'K' if is_kanji else '')
        return is_kanji
    except ValueError:
        return False


def contains_japanese(text: str, *, log: bool = False) -> bool:
    """
    Return True if the text contains any Japanese at all.
    """
    return any(
        is_japanese_char(ch, include_digits_and_brackets=False, log=log) for ch in text
    )


def contains_kanji(text: str, *, log: bool = False) -> bool:
    """
    Return True if the text contains any kanji.
    """
    return any(is_kanji(ch, log=log) for ch in text)


def contains_non_japanese(text: str, log: bool = False) -> bool:
    """
    Return True if the text contains any Latin characters at all.
    """
    return any(not is_japanese_char(ch, log=log) for ch in text)


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
for original, expected_stripped in [
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
    stripped = strip_spaces_in_japanese(original)
    assert stripped == expected_stripped, (
        f'{original}: {stripped} != {expected_stripped}'
    )


def strip_non_japanese_and_split_sentences(
    text: str, include_digits_and_brackets: bool = True
) -> str:
    """
    If the text contains non-Japanese characters from the text, insert 。
    between pieces of Japanese that were separated by non-Japanese to make the
    tts insert a pause rather then running them all together, and remove
    consecutive duplicate sentences.
    """
    if contains_non_japanese(text):
        # Android puts spaces in voice input where it shouldn't. Make sure they
        # don't count as separate sentences.
        text = strip_spaces_in_japanese(text)
        # Replace non-japanese chars with 。.
        text = (
            ''.join(
                ch
                if is_japanese_char(
                    ch,
                    include_digits_and_brackets=include_digits_and_brackets,
                )
                else '。'
                for ch in text
            )
            + '。'
        )
        # Then replace all strings of 。 with a single one.
        text = re.sub(
            r'。+',
            '。',
            text,
        ).lstrip('。')
    return text


# Built-in test.
for original, expected_stripped in [
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
    ('おんな、おんな、is Japanese.', 'おんな、おんな、。'),
    # If mixed Japanese and Latin, strip Latin characters and duplication.
    ('違う。違う。違う。hello.違う。違う。', '違う。違う。違う。違う。違う。'),
    # If mixed Japanese and Latin, add 。 between pieces of Japanese.
    ('日本語あるハー「」。、ab, ()1', '日本語あるハー「」。、。()1。'),
    # Strip spaces too.
    ('おんな、 おんな、', 'おんな、おんな、。'),
]:
    stripped = strip_non_japanese_and_split_sentences(original)
    assert stripped == expected_stripped, (
        f'{original}: {stripped} != {expected_stripped}'
    )


def replace_punctuation_with_commas(text: str) -> str:
    """
    Replace non-kana/kanji/digits with Japanese commas, for tts.
    """
    text = ''.join(
        ch
        if is_kana_or_kanji_or_digit_or_char(ch, other='！？') or ch == '。'
        else '、'
        for ch in text
    )
    # Clean up duplication.
    text = re.sub(
        r'、、+',
        '、',
        text,
    )
    text = re.sub(
        r'、*。、*',
        '。',
        text,
    )
    text = re.sub(
        r'^[、。]+',
        '',
        text,
    )
    return text


# Built-in test.
for original, expected_replaced in [
    (
        '、',
        '',
    ),
    (
        '、か',
        'か',
    ),
    (
        '、 か',
        'か',
    ),
    (
        '、　か',
        'か',
    ),
    (
        '、か、。',
        'か。',
    ),
    (
        '、か、、。、',
        'か。',
    ),
    (
        '、1. か',
        '1、か',
    ),
    (
        '1. こんにちは、（おい！）。2. げんき？',
        '1、こんにちは、おい！。2、げんき？',
    ),
]:
    replaced = replace_punctuation_with_commas(original)
    assert replaced == expected_replaced, (
        f'{original}: {replaced} != {expected_replaced}'
    )


def strip_sentences_without_kanji(text: str) -> str:
    """
    Strip hiragana only sentences out of text returned from
    strip_non_japanese_and_split_sentences, that is, sentences and fragments
    stripped out of mixed text and delimited by '。' characters for tts.
    """
    assert all(is_japanese_char(ch) for ch in text), (
        'strip_sentences_without_kanji, all(is_japanese_char)'
    )
    result = ''
    maybe_keep_sentence = ''
    for ch in text:
        if ch != '。':
            maybe_keep_sentence += ch
            continue
        if any(is_kanji(ch) for ch in maybe_keep_sentence):
            result += maybe_keep_sentence + ch
        maybe_keep_sentence = ''
    if any(is_kanji(ch) for ch in maybe_keep_sentence):
        result += maybe_keep_sentence
    return result


# Built-in test.
for original, expected_stripped in [
    ('おはよう！。か。や。いぬ。今。どうした？', '今。'),
    ('おはよう！。か。や。いぬ。今。どうした？。', '今。'),
    ('い。', ''),
    (')。い。', ''),
]:
    stripped = strip_sentences_without_kanji(original)
    assert stripped == expected_stripped, (
        f'{original}: {stripped} != {expected_stripped}'
    )


def strip_duplicate_sentences(text: str) -> str:
    """
    Strip duplicate sentences out of text returned from
    strip_non_japanese_and_split_sentences, that is, sentences and fragments
    stripped out of mixed text and delimited by '。' characters for tts.
    """
    assert all(is_japanese_char(ch) for ch in text), (
        'strip_duplicate_sentences, all(is_japanese_char)'
    )
    original = [
        sentence + '。' for sentence in text.split('。') if sentence.strip() != ''
    ]
    without_duplicates = [x for i, x in enumerate(original) if x not in original[:i]]
    return ''.join(without_duplicates)


# Built-in test.
for original, expected_stripped in [
    (
        'おはよう！。おはよう！。か。や。や。いぬ。や。今。か。どうした？',
        'おはよう！。か。や。いぬ。今。どうした？。',
    ),
    (
        'おはよう！。おはよう！。か。や。や。いぬ。や。今。か。どうした？。',
        'おはよう！。か。や。いぬ。今。どうした？。',
    ),
    ('違う。違う。違う。違う。違う。', '違う。'),
    ('違う。や。や。違う。', '違う。や。'),
    (
        (
            '大切。大事。1。大切(たいせつ)。大切。家族は私にとって大切です。(。)'
            '2。大事(だいじ)。大事。病気を治すことが一番大事です。(。)。大切。大事。'
        ),
        '大切。大事。1。大切、たいせつ。家族は私にとって大切です。2。大事、だいじ。病気を治すことが一番大事です。',
    ),
]:
    stripped = strip_non_japanese_and_split_sentences(original)
    stripped = replace_punctuation_with_commas(stripped)
    stripped = strip_duplicate_sentences(stripped)
    assert stripped == expected_stripped, (
        f'{original}: {stripped} != {expected_stripped}'
    )


# Built-in test.
for original, expected_stripped in [
    (
        # pylint: disable=line-too-long
        """Certainly! Both 上手い and 上手な are used to describe someone's skill or talent, but they are used in different grammatical contexts and can have slightly different nuances.
上手い (うまい)
上手い is an adjective (in the い-adjective form) that means "skillful" or "good at" something. It is frequently used in casual conversation to appreciate someone's skill.
Examples:
彼は料理が上手い。 (He is good at cooking.)
君のギターの演奏は本当に上手いね。 (Your guitar playing is really skillful.)
上手な (じょうずな)
上手な is a な-adjective and it carries a more formal tone, often used in written Japanese or formal speech. It also means "skillful" or "good at something," but it usually implies a more learned or cultivated skill.
Examples:
彼は上手なスピーチをしました。 (He gave a skillful speech.)
彼女は上手な絵を描きます。 (She draws skillful pictures.)
Comparison:
カジュアルな会話で:
彼はスキーが上手いよ。 (He is good at skiing.)
フォーマルな状況で:
彼は上手なスキー選手です。 (He is a skillful skier.)
In summary:
Use 上手い in more informal, conversational contexts.
Use 上手な when you need a more formal tone, such as in speeches, writing, or formal situations.""",
        # pylint: enable=line-too-long
        (
            '上手い。上手な。上手い(うまい)上手い。彼は料理が上手い。'
            ')君のギターの演奏は本当に上手いね。)上手な(じょうずな)上手な。'
            '彼は上手なスピーチをしました。)彼女は上手な絵を描きます。'
            'カジュアルな会話で。彼はスキーが上手いよ。)フォーマルな状況で。'
            '彼は上手なスキー選手です。'
        ),
    ),
]:
    stripped = strip_non_japanese_and_split_sentences(original)
    stripped = strip_sentences_without_kanji(stripped)
    stripped = strip_duplicate_sentences(stripped)
    assert stripped == expected_stripped, (
        f'{original}: {stripped} != {expected_stripped}'
    )


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


for age, expected_kanji in [
    (0, '零'),
    (1, '一'),
    (7, '七'),
    (10, '十'),
    (16, '十六'),
    (40, '四十'),
    (44, '四十四'),
    (50, '五十'),
]:
    kanji = age_to_kanji(age)
    assert kanji == expected_kanji, f'{age}: {kanji} != {expected_kanji}'
