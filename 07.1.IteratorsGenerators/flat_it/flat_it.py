from typing import Iterable, Generator, Any


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    try:
        for item in sequence:
            if item != sequence:
                yield from flat_it(item)
            else:
                yield item
    except TypeError:
        yield sequence
