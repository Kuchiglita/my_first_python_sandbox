import typing as tp
from collections import defaultdict


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """

    def count_chars(text: str) -> int:
        return len(text)

    def count_lines(text: str) -> int:
        return sum(1 for _ in text if _ == '\n')

    def count_longest_line(text: str) -> int:
        return max(len(line) for line in text.splitlines()) if text else 0

    def count_words(text: str) -> int:
        return len(text.split())

    result: dict[str, int] = defaultdict(int)
    flags_ = flags or '-mlLw'
    for flag in flags_:
        if flag == 'm':
            result['chars'] = count_chars(text)
        elif flag == 'l':
            result['lines'] = count_lines(text)
        elif flag == 'L':
            result['longest_line'] = count_longest_line(text)
        elif flag == 'w':
            result['words'] = count_words(text)
    return result
