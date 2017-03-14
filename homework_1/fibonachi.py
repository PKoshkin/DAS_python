#!/usr/bin/python

def fibonachi(n):
    if (n == 0) or (n == 1):
        return n
    previos = current = 1
    for i in range(n - 2):
        temp = previos + current
        previos = current
        current = temp
    return current

n = int(input())
print(fibonachi(n))
