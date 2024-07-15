# flake8: noqa
from typing import Any


def f0(x) -> Any:
    pass


def f1(a) -> Any:
    a = 0
    return a


def f2(a) -> Any:
    a = 0
    print(a)
    return


def f3() -> Any:
    a = 0
    a += 1
    print(a)
    return


def f4() -> Any:
    return range(10)


def f5() -> Any:
    for i in range(10):
        print(i)
    return


def f6(a) -> Any:
    a = 0
    for i in range(10):
        a += 1
    print(a)
    return


def f8() -> Any:
    x, y = (1, 2)
    return


def f9() -> Any:
    if 1 == 1:
        return 1
    return 2


def f10() -> Any:
    for i in range(10):
        if i == 3:
            break
    return


def f11() -> Any:
    list_ = [1, 2, 3]
    dict_ = {'a': 1, 'b': 2}
    return list_, dict_


def f12() -> Any:
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    return a + (b * c) / (d**e)

