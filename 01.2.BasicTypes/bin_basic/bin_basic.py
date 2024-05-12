import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    if len(nums) == 0:
        return False
    beg: int = 0
    end: int = len(nums) - 1
    while beg < end - 1:
        mid: int = (beg + end) // 2
        if nums[mid] < value:
            beg = mid
        else:
            end = mid
    if nums[beg] == value:
        return True
    if nums[end] == value:
        return True
    return False
