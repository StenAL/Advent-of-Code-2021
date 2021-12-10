from util import *
from collections import *
import copy
from functools import reduce

day = 10


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    matches = {"(": ")", "{": "}", "[": "]", "<": ">"}
    corrupted = []
    for line in data:
        stack = []
        for char in line:
            if char in ["(", "[", "<", "{"]:
                stack.append(char)
            else:
                c = stack.pop()
                if char != matches[c]:
                    corrupted.append(char)
                    break
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    ans = sum([points[c] for c in corrupted])
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    matches = {"(": ")", "{": "}", "[": "]", "<": ">"}
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    not_corrupted = []
    for line in data:
        stack = []
        corrupted = False
        for char in line:
            if char in ["(", "[", "<", "{"]:
                stack.append(char)
            else:
                c = stack.pop()
                if char != matches[c]:
                    corrupted = True
                    break
        if not corrupted:
            not_corrupted.append(line)

    scores = []
    for line in not_corrupted:
        stack = []
        score = 0
        for char in line:
            if char in ["(", "[", "<", "{"]:
                stack.append(char)
            else:
                stack.pop()
        for c in reversed(stack):
            score *= 5
            score += points[matches[c]]
        scores.append(score)

    scores.sort()
    ans = scores[len(scores) // 2]
    print(ans)


# task1()
task2()
