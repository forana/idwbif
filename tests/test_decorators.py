import time
import unittest
from collections.abc import Callable
from datetime import datetime, timedelta

from idwbif.decorators import make_it_faster


def _time_func(f: Callable) -> timedelta:
    start = datetime.now()
    f()
    return datetime.now() - start


class TestDecorator(unittest.TestCase):
    def test_it(self):
        # this is a VERY slow function. WOW
        @make_it_faster
        def super_slow_func():
            time.sleep(1)

        # the first run is always still slow
        first_run = _time_func(super_slow_func)

        # but after that, it should be FAST
        for more_runs in range(100):
            new_run = _time_func(super_slow_func)
            # it should be, like, at least 100 times faster
            assert new_run * 100 < first_run
