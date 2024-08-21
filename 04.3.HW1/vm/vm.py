"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp


class Frame:

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals if frame_locals is not None else {}
        self.data_stack: tp.Any = []
        self.return_value = None
        self.current_instruction_index = 0

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        with open("debug_output", "w") as f:
            f.write("Frame: starting run\n")
            f.write("Frame: instructions list:\n")
        for instruction in dis.get_instructions(self.code):
            with open("debug_output", "a") as f:
                f.write(f"Frame: instr{instruction}\n")
        instructions = list(dis.get_instructions(self.code))
        while self.current_instruction_index < len(instructions):
            instruction = instructions[self.current_instruction_index]
            with open("debug_output", "a") as f:
                f.write(
                    f"Frame: Entering func_op named {instruction.opname.lower() + '_op'}\n")
            self.current_instruction_index += 1
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)  # self.opname_op(arg)
        return self.return_value

    def call_function_op(self, arg: int) -> None:
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def load_fast_op(self, arg: tp.Any) -> None:
        """arg is a variable from co_varnames"""
        with open("debug_output", "a") as f:
            f.write(f"Frame: locals are: {self.locals}; co_varnames are: {self.code.co_varnames}\n")
        self.push(self.locals[arg])

    def store_fast_op(self, arg: tp.Any) -> None:
        self.locals[arg] = self.pop()

    def delete_fast_op(self, arg: tp.Any) -> None:
        del self.locals[arg]

    def load_name_op(self, arg: str) -> None:
        if arg in self.builtins:
            self.push(self.builtins[arg])
        elif arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])

    def load_global_op(self, arg: str) -> None:
        if arg in self.builtins:
            self.push(self.builtins[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])

    def load_const_op(self, arg: tp.Any) -> None:
        self.push(arg)

    def load_method_op(self, arg: str) -> None:
        obj = self.pop()
        if hasattr(obj, arg):
            method = getattr(obj, arg)
            if callable(method):
                self.push(method)
                self.push(obj)
            else:
                self.push(None)
                self.push(method)
        else:
            self.push(None)
            self.push(getattr(obj, arg))

    def call_method_op(self, arg: int) -> None:
        args = self.popn(arg)
        method = self.pop()
        obj = self.pop()
        self.push(method(obj, *args))

    def return_value_op(self, arg: tp.Any) -> None:
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3571

        Parse stack:
            https://github.com/python/cpython/blob/3.9/Objects/call.c#L671

        Call function in cpython:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L4950
        """
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: dict[str, tp.Any] = {}
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: str) -> None:
        const = self.pop()
        self.globals[arg] = const

    def call_method_op(self, arg: int) -> None:
        args = self.popn(arg)
        method = self.pop()
        obj = self.pop()


    def unpack_sequence_op(self, arg: int) -> None:
        unpacking = self.pop()
        for item in reversed(unpacking):
            self.push(item)

    def extended_arg_op(self, arg: int) -> None:
        pass

    # BUILDS AND CONTAINERS
    def build_tuple_op(self, arg: int) -> None:
        self.push(tuple(self.popn(arg)))

    def build_list_op(self, arg: int) -> None:
        self.push(list(self.popn(arg)))

    def build_set_op(self, arg: int) -> None:
        self.push(set(self.popn(arg)))

    def build_map_op(self, arg: int) -> None:
        my_dict = {}
        for _ in range(arg):
            value = self.pop()
            key = self.pop()
            my_dict[key] = value
        self.push(my_dict)

    def build_const_key_map_op(self, arg: int) -> None:  # is it right?
        keys = self.pop()
        values = self.popn(arg)
        my_dict = {}
        for i in range(len(keys)):
            my_dict[keys[i]] = values[i]
        self.push(my_dict)

    def build_string_op(self, arg: int) -> None:
        self.push("".join(self.popn(arg)))

    def build_slice_op(self, arg: int) -> None:
        if arg == 2:
            a = self.pop()
            b = self.pop()
            self.push(slice(b, a))
        elif arg == 3:
            a = self.pop()
            b = self.pop()
            c = self.pop()
            self.push(slice(c, b, a))

    def list_to_tuple_op(self, arg: tp.Any) -> None:
        self.push(tuple(self.pop()))

    def list_extend_op(self, arg: int) -> None:
        a = self.pop()
        b = self.pop()
        b.extend(a)
        self.push(b)

    def set_update_op(self, arg: int) -> None:
        a = self.pop()
        b = self.pop()
        b.update(a)
        self.push(b)

    def dict_update_op(self) -> None:
        a = self.pop()
        b = self.pop()
        b.update(a)
        self.push(b)

    def dict_merge_op(self) -> None:
        a = self.pop()
        b = self.pop()
        b |= a
        self.push(b)

    def store_subscr_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        c = self.pop()
        b[a] = c

    def delete_subscr_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        del b[a]

    def compare_op_op(self, arg: str) -> None:
        if arg == "==":
            a = self.pop()
            b = self.pop()
            self.push(b == a)
        elif arg == "!=":
            a = self.pop()
            b = self.pop()
            self.push(b != a)
        elif arg == "<":
            a = self.pop()
            b = self.pop()
            self.push(b < a)
        elif arg == "<=":
            a = self.pop()
            b = self.pop()
            self.push(b <= a)
        elif arg == ">":
            a = self.pop()
            b = self.pop()
            self.push(b > a)
        elif arg == ">=":
            a = self.pop()
            b = self.pop()
            self.push(b >= a)

    # ARITHMETIC OPERATIONS
    def binary_power_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b ** a)

    def binary_multiply_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b * a)

    def binary_floor_divide_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b // a)

    def binary_true_divide_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b / a)

    def binary_modulo_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b % a)

    def binary_add_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b + a)

    def binary_subtract_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b - a)

    def binary_subscr_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b[a])

    def binary_lshift_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b << a)

    def binary_rshift_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b >> a)

    def binary_or_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b | a)

    def binary_xor_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b ^ a)

    def binary_and_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b & a)

    def inplace_power_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b ** a)

    def inplace_multiply_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b * a)

    def inplace_floor_divide_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b // a)

    def inplace_true_divide_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b / a)

    def inplace_modulo_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b % a)

    def inplace_add_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b + a)

    def inplace_subtract_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b - a)

    def inplace_lshift_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b << a)

    def inplace_rshift_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b >> a)

    def inplace_and_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b & a)

    def inplace_xor_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b ^ a)

    def inplace_or_op(self, arg: tp.Any) -> None:
        a = self.pop()
        b = self.pop()
        self.push(b | a)

    # ITERATOR OPERATIONS
    def get_iter_op(self, arg: tp.Any) -> None:
        self.push(iter(self.pop()))

    def for_iter_op(self, arg: int) -> None:
        try:
            self.push(next(self.top()))
        except StopIteration:
            self.pop()
            self.jump_absolute_op(arg)

    def jump_absolute_op(self, arg: int) -> None:
        self.current_instruction_index = arg // 2

    def jump_forward_op(self, arg: int) -> None:
        self.current_instruction_index += arg // 2 - 1

    def pop_jump_if_true_op(self, arg: int) -> None:
        if self.pop():
            self.jump_absolute_op(arg)

    def pop_jump_if_false_op(self, arg: int) -> None:
        if not self.pop():
            self.jump_absolute_op(arg)

    def jump_if_true_or_pop_op(self, arg: int) -> None:
        if self.top():
            self.jump_absolute_op(arg)
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, arg: int) -> None:
        if not self.top():
            self.jump_absolute_op(arg)
        else:
            self.pop()

    def is_op_op(self, arg: bool) -> None:
        a = self.pop()
        b = self.pop()
        if arg == 0:
            self.push(b is a)
        else:
            self.push(b is not a)

    def contains_op_op(self, arg: bool) -> None:
        a = self.pop()
        b = self.pop()
        if arg == 0:
            self.push(a in b)
        else:
            self.push(a not in b)


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)

        # Debug print to verify initialization
        with open("debug_output", "a") as f:
            f.write("VirtualMachine: Initialized Frame\n")

        return frame.run()
