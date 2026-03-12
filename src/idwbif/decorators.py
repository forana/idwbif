import logging
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from typing import ParamSpec, TypeVar

TIME_LIMIT = timedelta(milliseconds=10)
"""The default time limit at which a function will be called "not fast"."""
_FAST_ATTR = "__is_fast"

P = ParamSpec("P")
R = TypeVar("R")

_logger = logging.getLogger("idwbif")


def make_it_faster(func: Callable[P, R]) -> Callable[P, R | None]:
    """
    Make a slow function faster. If it ever takes longer than the time limit (10ms),
    this decorator will make the function much faster for every subsequent call - up to
    1000x faster, or maybe even more.

    Don't worry about how it works.
    """
    @wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R | None:
        # if the wrapped function isn't for sure fast yet, let's measure it. if it's not
        # fast enough, we'll make it faster the next time.
        if getattr(func, _FAST_ATTR, False) is False:
            start = datetime.now()
            return_value = func(*args, **kwargs)

            # did it take too long?
            if start + TIME_LIMIT < datetime.now():
                # then make it fast forever after
                setattr(func, _FAST_ATTR, True)
                _logger.info(f"Function '{func.__qualname__}' has been improved.")

            return return_value
        else:
            # fast mode
            return None
    
    return wrapped
