import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range], lst_b: tp.Union[list[int], range]) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    if len(lst_b) == 0:
        return lst_a

    j: int = 0
    lst_out: list[int] = []
    j_reached_lst_b_end: bool = False

    for value in lst_a:
        if j_reached_lst_b_end:
            lst_out.append(value)
            continue

        while value > lst_b[j]:
            j += 1
            if j == len(lst_b):
                j_reached_lst_b_end = True
                j -= 1
                break

        if value != lst_b[j]:
            lst_out.append(value)

    return lst_out
