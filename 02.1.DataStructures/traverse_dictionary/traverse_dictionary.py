import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    lst_out: list = []
    for s in dct:
        if type(dct[s]) == int:
            lst_out.append((prefix + s, dct[s]))
        else:
            lst_out += traverse_dictionary_immutable(dct[s], prefix + s + '.')
    return lst_out


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for s in dct:
        if type(dct[s]) == int:
            result.append((prefix + s, dct[s]))
        else:
            traverse_dictionary_mutable(dct[s], result, prefix + s + ".")


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    lst_out = []
    stack = []
    root = [dct, '']
    while True:
        s: str
        for s in root[0]:
            if type(root[0][s]) is not int:
                stack.append([root[0][s], root[1] + s + '.'])
            else:
                lst_out.append((root[1] + s, root[0][s]))
        if len(stack) == 0:
            return lst_out
        root = stack.pop()


print(traverse_dictionary_iterative({'a': 1, 'b': 2}))
