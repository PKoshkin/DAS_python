#!/usr/bin/python

import sys
import re

regular_strings = [
    '(\d{2}\.){2}\d{4}',
    '(\d{2}\/){2}\d{4}',
    '(\d{2}-){2}\d{4}',
    '\d{4}(\.\d{2}){2}',
    '\d{4}(\/\d{2}){2}',
    '\d{4}(-\d{2}){2}',
    '\d{1,2}\s*([Ёёа-яА-Я]+)\s*\d{4}'
]

regular_string = '^(' + '|'.join(regular_strings) + ')$'

for line in sys.stdin:
    if re.match(regular_string, line) is not None:
        print("YES")
    else:
        print("NO")
