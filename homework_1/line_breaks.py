#!/usr/bin/python

import sys

max_length = int(input())

result = ''
line_length = 0
line_begins = True
for line in sys.stdin:
    for word in line.split(' '):
        if word == '':
            continue

        if len(result) == 0:
            line_begins = True
        elif result[-1] == '\n':
            line_begins = True
        else:
            line_begins = False
        
        if line_begins:
            line_length = len(word)
            line_begins = False
            result += word
        else:
            if line_length + len(word) + 1 <= max_length:
                line_length += len(word) + 1
                result += ' ' + word
            else:
                if result[-1] != '\n':
                    result += '\n'
                result += word
                line_length = len(word)

print(result)
