import sys
import math
from typing import Any, Optional

PROMPT = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace"""
    if context is None:
        context = {}
    context["__builtins__"] = {}
    while True:
        try:
            l = input(PROMPT)
            print(eval(l, context))
        except EOFError:
            print()
            break
