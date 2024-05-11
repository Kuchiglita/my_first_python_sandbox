import typing as tp


def get_fizz_buzz(n: int) -> list[tp.Union[int, str]]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    lst_out: tp.List[tp.Union[int, str]] = []
    for i in range(1, n + 1):
        adder: tp.Union[int, str]
        if not(i % 3 == 0 or i % 5 == 0):
            adder = i
        else:
            adder = ''
            if i % 3 == 0:
                adder += 'Fizz'
            if i % 5 == 0:
                adder += 'Buzz'
        lst_out.append(adder)

    return lst_out
