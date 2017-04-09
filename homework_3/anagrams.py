#!/usr/bin/python

import sys

lines_number = int(input())
sorted_strings = {}
for i in range(lines_number):
    string = input()
    string = string.lower()
    sorted_string = ''.join(sorted(string))
    if sorted_string in sorted_strings:
        sorted_strings[sorted_string].add(string)
    else:
        sorted_strings[sorted_string] = {string}

for key in sorted_strings:
    sorted_strings[key] = sorted(list(sorted_strings[key]))
sorted_keys = sorted(list(sorted_strings), key=lambda x: sorted_strings[x][0])

for key in sorted_keys:
    if len(sorted_strings[key]) > 1:
        print(' '.join(sorted_strings[key]))
