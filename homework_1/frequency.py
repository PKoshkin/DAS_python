#!/usr/bin/python

import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'
dictionary = {character: 0 for character in alphabet}
for line in sys.stdin:
    for character in line:
        if character.lower() in dictionary:
            dictionary[character.lower()] += 1
items = [item for item in dictionary.items()]
items.sort(key=(lambda item: (item[1], -ord(item[0]))), reverse=True)

for character, frequency in items:
    if frequency != 0:
        print("{}: {}".format(character, frequency))
