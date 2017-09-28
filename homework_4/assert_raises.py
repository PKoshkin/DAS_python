#!/usr/local/bin/python3

import sys


class AssertionError(Exception):
    pass


class AssertRaises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if isinstance(exception_value, self.exception):
            return True
        else:
            raise AssertionError()

exec(sys.stdin.read())
