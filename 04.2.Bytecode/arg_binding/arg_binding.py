from types import FunctionType
from typing import Any, Dict

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'  #
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'  #
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'  #
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    pos_only_cnt = func.__code__.co_posonlyargcount
    arg_cnt = func.__code__.co_argcount
    kwonly_cnt = func.__code__.co_kwonlyargcount
    args_starr = bool(func.__code__.co_flags & CO_VARARGS)
    kwargs_starr = bool(func.__code__.co_flags & CO_VARKEYWORDS)
    all_args_names = []
    if func.__code__.co_varnames:
        all_args_names = func.__code__.co_varnames[:arg_cnt + kwonly_cnt]
    binding: dict = {}
    args_name: str = "args"
    kwargs_name: str = "kwargs"
    if func.__code__.co_varnames:
        args_name = func.__code__.co_varnames[min(arg_cnt + kwonly_cnt - 1 + int(args_starr), len(func.__code__.co_varnames))]
        kwargs_name = func.__code__.co_varnames[min(arg_cnt + kwonly_cnt - 1 + int(args_starr) + int(kwargs_starr), len(func.__code__.co_varnames))]
    if kwargs_starr:  # initializing "*kwargs" if needed
        binding[kwargs_name] = {}
    # non-error lengths founder
    len_args = 0
    if args is not None:
        len_args = len(args)
    len_defaults = 0
    if func.__defaults__:
        len_defaults = len(func.__defaults__)
    len_kw_defaults = 0
    if func.__kwdefaults__:
        len_kw_defaults = len(func.__kwdefaults__)

    if len_args > arg_cnt and not args_starr:  # args_starr = False, len(args) > pos_only + usual + defaults
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if args_starr:
        if len_args > arg_cnt:
            binding[args_name] = tuple(args[arg_cnt:])  # len(args) > arg_cnt => len(args) >= 1; we took what's left
        else:
            binding[args_name] = tuple([])

    # this section is for binding args
    for i in range(len_defaults):  # initializing defaults in
        binding[all_args_names[arg_cnt - len_defaults + i]] = func.__defaults__[i]
    for i, arg in enumerate(args):  # args binding
        if i < arg_cnt:
            binding[all_args_names[i]] = arg

    used_arg_names = all_args_names[:min(len_args, arg_cnt)]

    # this section is for binding kwargs or what is left with args
    if func.__kwdefaults__:  # no check-ups, kw_defaults are always correct
        for key, value in func.__kwdefaults__.items():
            binding[key] = value

    for key, value in kwargs.items():
        if key in all_args_names[arg_cnt:arg_cnt + kwonly_cnt]:  # safe option, if it is in def func(...)
            binding[key] = value
        elif key in all_args_names[:pos_only_cnt]:  # right handling
            if not kwargs_starr:
                raise TypeError(ERR_POSONLY_PASSED_AS_KW)
            binding[kwargs_name][key] = value
        elif key in all_args_names[pos_only_cnt:arg_cnt]:  # right handling
            if key in used_arg_names:
                raise TypeError(ERR_MULT_VALUES_FOR_ARG)
            else:
                binding[key] = value
        else:  # if it must be in *kwargs
            if not kwargs_starr:
                raise TypeError(ERR_TOO_MANY_KW_ARGS)
            binding[kwargs_name][key] = value

    for arg_name in all_args_names[:max(arg_cnt - len_defaults, pos_only_cnt)]:  # usual args only
        if arg_name not in binding:  # if args not enough to cover usuals and kwargs don't cover either
            raise TypeError(ERR_MISSING_POS_ARGS)
    for arg_name in all_args_names[arg_cnt: arg_cnt + kwonly_cnt - len_kw_defaults]:  # check if all the non-default kwargs were set
        if arg_name not in binding:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)

    return binding
