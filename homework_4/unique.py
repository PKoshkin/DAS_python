#!/usr/local/bin/python3

import sys


def unique(iterable):
    current_element = None
    for new_element in iterable:
        if new_element != current_element:
            current_element = new_element
            yield new_element


exec(sys.stdin.read())
