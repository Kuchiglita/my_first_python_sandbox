def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    if (a - b) * (a - c) <= 0:
        return a
    if (b - a) * (b - c) <= 0:
        return b
    if (c - a) * (c - b) <= 0:
        return c
    return sorted([a, b, c])[1]
