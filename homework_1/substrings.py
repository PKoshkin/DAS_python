#!/usr/bin/python

n = int(input())
for i in range(n):
    string = input()
    substrings = []
    for size in range(1, len(string) + 1):
        index = 0
        while index + size <= len(string):
            substrings.append(string[index: index + size])
            index += 1
    print(" ".join(substrings))
