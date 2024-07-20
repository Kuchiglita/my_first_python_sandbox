import types
import dis
from collections import Counter


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    opnames = Counter([])
    it = dis.get_instructions(source_code)
    for i in it:
        if type(i.argval) == types.CodeType:
            opnames += count_operations(i.argval)
        opnames[i.opname] += 1
    return opnames

