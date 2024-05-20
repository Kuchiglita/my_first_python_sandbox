from heapq import *
import typing as tp


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    lst_out = []
    indexes = [0 for _ in range(len(seq))]
    values_with_indexes = [(seq[i][0], i) for i in range(len(seq)) if len(seq[i]) != 0]
    heapify(values_with_indexes)
    count: int = sum(1 for _ in seq if len(_) > 0)
    while count > 0:
        val, ind = heappop(values_with_indexes)
        lst_out.append(val)
        indexes[ind] += 1
        if indexes[ind] == len(seq[ind]):
            count -= 1
        else:
            heappush(values_with_indexes, (seq[ind][indexes[ind]], ind))

    return lst_out
