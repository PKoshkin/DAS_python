#!/usr/bin/python


p = float(input())

print(pow(sum([pow(abs(float(value)), p) for value in input().split(' ')]), 1 / p))
