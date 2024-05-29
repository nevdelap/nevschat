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


def strip_non_japanese_and_split_sentences(
    text: str, include_digits_and_punctuation: bool = True
) -> str:
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
                if is_japanese_char(
                    ch,
                    include_digits_and_punctuation=include_digits_and_punctuation,
                )
                else '。'
                for ch in text
            )
            + '。',
        ).lstrip('。')
    return text


# Built-in test.
def test_strip_non_japanese_split_sentences(original: str, expected: str) -> None:
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
    ('おんな、おんな、is Japanese.', 'おんな、おんな、。'),
    # If mixed Japanese and Latin, strip Latin characters and duplication.
    ('違う。違う。違う。hello.違う。違う。', '違う。違う。違う。違う。違う。'),
    # If mixed Japanese and Latin, add 。 between pieces of Japanese.
    ('日本語あるハー「」。、ab, ()1', '日本語あるハー「」。、。()1。'),
]:
    test_strip_non_japanese_split_sentences(original, expected)


def strip_short_hiragana_sentences(text: str, up_to_characters: int) -> str:
    """
    Strip short sentences out of text returned from
    strip_non_japanese_and_split_sentences, that is, sentences and fragments
    stripped out of mixed text and delimited by '。' characters for tts.
    """
    assert all(is_japanese_char(ch) for ch in text)
    result = ''
    maybe_keep_sentence = ''
    for ch in text:
        if ch != '。':
            maybe_keep_sentence += ch
            continue
        if len(maybe_keep_sentence) > up_to_characters or any(
            is_kanji(ch) for ch in maybe_keep_sentence
        ):
            result += maybe_keep_sentence + ch
        maybe_keep_sentence = ''
    result += maybe_keep_sentence
    return result


# Built-in test.
def test_strip_short_hiragana_sentences(
    original: str, expected: str, up_to_characters: int
) -> None:
    stripped = strip_short_hiragana_sentences(original, up_to_characters)
    assert stripped == expected, f'{original}: {stripped} != {expected}'


for original, expected, up_to_characters in [
    (
        'おはよう！。か。や。いぬ。今。どうした？',
        'おはよう！。か。や。いぬ。今。どうした？',
        0,
    ),
    ('おはよう！。か。や。いぬ。今。どうした？', 'おはよう！。いぬ。今。どうした？', 1),
    ('おはよう！。か。や。いぬ。今。どうした？', 'おはよう！。今。どうした？', 2),
    ('おはよう！。か。や。いぬ。今。どうした？', 'おはよう！。今。どうした？', 3),
    ('おはよう！。か。や。いぬ。今。どうした？', 'おはよう！。今。どうした？', 4),
    ('おはよう！。か。や。いぬ。今。どうした？', '今。どうした？', 5),
    ('おはよう！。か。や。いぬ。今。どうした？。', '今。', 5),
]:
    test_strip_short_hiragana_sentences(original, expected, up_to_characters)


def strip_duplicate_sentences(text: str) -> str:
    """
    Strip duplicate sentences out of text returned from
    strip_non_japanese_and_split_sentences, that is, sentences and fragments
    stripped out of mixed text and delimited by '。' characters for tts.
    """
    assert all(is_japanese_char(ch) for ch in text)
    while True:
        old_len = len(text)
        text = re.sub(r'([^。]*。)\1', r'\1', text)
        if len(text) == old_len:
            break
    return text


# Built-in test.
def test_strip_duplicate_sentences(original: str, expected: str) -> None:
    original = strip_short_hiragana_sentences(
        strip_non_japanese_and_split_sentences(
            original,
            include_digits_and_punctuation=False,
        ),
        up_to_characters=3,
    )
    stripped = strip_duplicate_sentences(original)
    assert stripped == expected, f'{original}: {stripped} != {expected}'


for original, expected in [
    ('違う。違う。違う。違う。違う。', '違う。'),
    ('違う。や。や。違う。', '違う。'),
    (
        # pylint: disable=line-too-long
        """Certainly, let's break down the more advanced aspects of the provided text:

1. **うどんやワッフルや紅茶が好きです**:
   - The particle "や" is used here to list multiple items in a non-exhaustive manner. This implies that there are potentially other items the speaker likes, but these three are mentioned as examples. This is subtly different from the exhaustive list implied by the particle "と".
   - The sentence structure is a basic subject-predicate form, where "が" marks the subject "うどんやワッフルや紅茶" for the predicate "好きです".

2. **私は想像力が豊かです**:
   - This sentence uses "私は", with "は" as the topic marker, to introduce the topic of the sentence, "私".
   - The particle "が" is used again here to mark the subject within the context of the topic. "想像力" (imagination) is being described as "豊かです" (abundant/rich). Essentially, the structure indicates that the imagination is abundant, attached to the topic "私".
   - The adjective "豊か" is in its formal ending "です", indicating a polite form. "豊か" is a na-adjective, and the verb "です" is used to link this adjective to the subject.
z
3. **今、刺激されています**:
   - "今" sets the time frame for the following statement, meaning "now".
   - The verb "刺激する" means "to stimulate". Here, it is in the passive form "刺激される", which means "to be stimulated".
   - "刺激されています" uses the passive form in the polite present continuous tense, implying that the subject (understood to be "私", from context) is currently being stimulated. The "-ています" form indicates an ongoing action or state.""",
        # pylint: enable=line-too-long
        (
            'うどんやワッフルや紅茶が好きです。うどんやワッフルや紅茶。好きです。'
            '私は想像力が豊かです。私は。私。想像力。豊かです。私。豊か。'
            '今、刺激されています。今。刺激する。刺激される。刺激されています。'
            '私。ています。'
        ),
    ),
    (
        # pylint: disable=line-too-long
        """The sentence "おにぎりやお茶漬けや烏龍茶が好きです。" uses several advanced grammatical features that are worth noting.

や (particle): The particle "や" is used to list multiple items in a non-exhaustive manner. It implies that there are other items that are liked besides the ones mentioned. In the sentence, "や" connects "おにぎり," "お茶漬け," and "烏龍茶," indicating that the speaker likes onigiri, ochazuke, and oolong tea, among other things.

が (particle): The particle "が" is used to mark the subject of the sentence. In this context, "が" marks the subject "おにぎりやお茶漬けや烏龍茶" for the verb "好きです," indicating what the speaker likes.

好きです (expression): This phrase is a polite form of "好きだ," which is an adjectival noun meaning "to like" or "to be fond of." The nominal nature of "好き" often needs the preceding subject marked typically by "が" to indicate the object of liking. It's worth noting that in casual speech, "好き" can be used as "好きだ" instead of "好きです."

These components work together to convey that the speaker has a fondness for the listed items among potentially others not mentioned.""",
        # pylint: enable=line-too-long
        (
            'おにぎりやお茶漬けや烏龍茶が好きです。おにぎり。お茶漬け。烏龍茶。'
            'おにぎりやお茶漬けや烏龍茶。好きです。好きだ。好き。好きだ。好きです。'
        ),
    ),
]:
    test_strip_duplicate_sentences(original, expected)


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
