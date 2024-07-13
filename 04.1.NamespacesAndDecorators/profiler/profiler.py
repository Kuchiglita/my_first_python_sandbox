from datetime import datetime
import functools


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    profiler.calls = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        initial_calls = profiler.calls
        profiler.calls += 1
        start = datetime.now()
        rtrn = func(*args, **kwargs)
        wrapper.last_time_taken = (datetime.now() - start).total_seconds()
        wrapper.calls = profiler.calls - initial_calls
        return rtrn
    wrapper.calls = 0
    wrapper.last_time_taken = 0
    return wrapper
