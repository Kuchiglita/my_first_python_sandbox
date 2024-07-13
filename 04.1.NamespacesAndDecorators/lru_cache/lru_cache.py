from typing import Callable, Any, TypeVar
import functools
import collections

Function = TypeVar('Function', bound=Callable[..., Any])

global_count = 0
global_count_ = 0


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """

    # decorator is such that it makes func -> func, so we return it.

    def decorator(func):
        cache_dict = {}

        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache_dict:
                if len(cache_dict) >= max_size:
                    cache_dict.pop(next(iter(cache_dict)))#pop first element, lol!!! this works somehow)))
                cache_dict[args] = func(*args)
            else:
                x = cache_dict.pop(args)
                cache_dict[args] = x
            return cache_dict[args]

        return wrapper

    return decorator
