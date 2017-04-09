#!/usr/bin/python

import sys

languages = {}

lines = sys.stdin
for line in lines:
    if line == '\n':
        break
    else:
        alphabet = line.split(' ')[1][:-1].lower()
        languages[alphabet] = line.split(' ')[0]

for line in sys.stdin:
    line_languages = set()
    for word in line[:-1].split(' '):
        counters = {languages[language]: 0 for language in languages}
        lower_word = word.lower()
        for character in lower_word:
            for language in languages:
                if character in language:
                    counters[languages[language]] += 1
        counters_list = [
            (languages[language], counters[languages[language]])
            for language in languages
        ]
        counters_list.sort(key=lambda x: (-x[1], x[0]))
        if counters_list[0][1] != 0:
            line_languages.add(counters_list[0][0])
    line_languages_list = [language for language in line_languages]
    line_languages_list.sort()
    print(' '.join(line_languages_list))
