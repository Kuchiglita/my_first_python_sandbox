import typing as tp
from collections import defaultdict


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    helper: dict[str, list[str]] = defaultdict(list)
    for k in dct:
        helper[dct[k]].append(k)
    return helper
