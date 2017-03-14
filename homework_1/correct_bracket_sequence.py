#!/usr/bin/python

opening_brackets = {'(', '{', '['}
opening_bracket = {')': '(', ']': '[', '}': '{'}

n = int(input())
answers = []
for i in range(n):
    string = input()
    stack = []
    for character in string:
        if character in opening_brackets:
            stack.append(character)
        else:
            if (len(stack) == 0) or (stack[-1] != opening_bracket[character]):
                print("no")
                break
            else:
                stack.pop()
    else:
        print("no" if stack else "yes")
