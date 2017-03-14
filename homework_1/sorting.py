#!/usr/bin/python

import no_standard_sort
import sys

def merge_sort(array, begin, end):
    if end - begin == 1:
        return

    middle = int((end + begin) / 2)
    merge_sort(array, begin, middle)
    merge_sort(array, middle, end)

    left_begin = begin
    left_end = middle
    right_begin = middle
    right_end = end

    index = 0
    merged = [0 for i in range(end - begin)]
    while (right_end - right_begin > 0) and (left_end - left_begin > 0):
        if (array[left_begin] > array[right_begin]):    
            merged[index] = array[right_begin]
            index += 1
            right_begin += 1
        else:
            merged[index] = array[left_begin]
            index += 1
            left_begin += 1
    
    while right_end - right_begin > 0:
        merged[index] = array[right_begin]
        index += 1
        right_begin += 1

    while left_end - left_begin > 0:
        merged[index] = array[left_begin]
        index += 1
        left_begin += 1

    for i in range(begin, end):
        array[i] = merged[i - begin]

stdin = sys.stdin.read()
if len(stdin) == 0:
    print(' ')
    exit()
array = [int(value) for value in stdin.split()]

merge_sort(array, 0, len(array))
print(' '.join([str(value) for value in array]))
