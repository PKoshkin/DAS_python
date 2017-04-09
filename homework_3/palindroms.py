#!/usr/bin/python

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ'
lines_number = int(input())
for i in range(lines_number):
    line = input()
    line = line.upper()
    i = 0
    j = len(line) - 1
    while (i < len(line)) and (j >= 0):
        if i > j:
            print("yes")
            break
        if (line[i] in alphabet) and (line[j] in alphabet):
            if (line[i] == line[j]) or ((line[i] in 'ЕЁ') and (line[j] in 'ЕЁ')):
                i += 1
                j -= 1
            else:
                print("no")
                break
        if line[i] not in alphabet:
            i += 1
        if line[j] not in alphabet:
            j -= 1
