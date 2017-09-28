#!/usr/local/bin/python3

import sys
import functools


def takes(*types):
    def decorator(function):
        @functools.wraps(function)
        def new_function(*parametrs):
            if not all([isinstance(parametr, parametr_type)
                       for parametr, parametr_type
                       in zip(parametrs, types)]):
                raise TypeError
            return function(*parametrs)
        return new_function
    return decorator


exec(sys.stdin.read())
