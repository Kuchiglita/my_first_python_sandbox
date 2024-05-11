import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    return [value ** 2 for value in elements]


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    return [id + 1 for id in range(len(elements))]


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    ans_index: tp.Optional[int] = None
    ans_value: tp.Optional[int] = None
    for index, value in enumerate(elements):
        if ans_value is None or value > ans_value:  #возможно нужно добавить ans != None
            ans_value = value
            ans_index = index
    return ans_index


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    return elements[1::2]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    ans_index: tp.Optional[int] = None
    for index, value in enumerate(elements):
        if value == 3:
            ans_index = index
            break
    return ans_index


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    ans_index: tp.Optional[int] = None
    for index, value in enumerate(reversed(elements)):
        if value == 3:
            ans_index = len(elements) - index - 1
            break
    return ans_index


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int]) -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    ans: tuple[tp.Optional[int], tp.Optional[int]] = (default, default)
    if len(elements) != 0:
        ans = (min(elements), max(elements))
    return ans


# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater than boundary and None otherwise
    """
    ans: tp.Optional[int]
    return ans if boundary < (ans := elements[i]) else None
