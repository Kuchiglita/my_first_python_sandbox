import collections
import typing as tp


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    if len(seq) == 0:
        return 0
    count = collections.Counter(seq)
    return len(seq) - max(count.values())

