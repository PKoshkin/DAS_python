#!/usr/local/bin/python3

import sys


def inexhaustible(generator):
    class Decorated:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __iter__(self):
            self.generator = generator(*self.args, **self.kwargs)
            return self

        def __next__(self):
            return next(self.generator)

    Decorated.__name__ = generator.__name__
    Decorated.__doc__ = generator.__doc__

    return Decorated


exec(sys.stdin.read())
