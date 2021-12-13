from util import *
from collections import *
import copy
from functools import reduce

day = 13


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    dots = set()
    folds = []
    mode = "dots"
    for line in data:
        if line == "":
            mode = "folds"
            continue
        if mode == "dots":
            line = tuple([int(el) for el in line.split(",")])
            dots.add(line)
        if mode == "folds":
            line = line.strip("fold along ")
            line = line.split("=")
            folds.append((line[0], int(line[1])))

    iterations = 1
    for fold in folds[:iterations]:
        (direction, line) = fold
        new_dots = dots.copy()
        if direction == "y":
            for point in filter(lambda p: p[1] > line, dots):
                length = line * 2
                (x, y) = point
                new_dots.remove(point)
                new_dots.add((x, length - y))
        if direction == "x":
            for point in filter(lambda p: p[0] > line, dots):
                width = line * 2
                (x, y) = point
                new_dots.remove(point)
                new_dots.add((width - x, y))
        dots = new_dots
    ans = len(dots)
    print(ans)

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    dots = set()
    folds = []
    mode = "dots"
    for line in data:
        if line == "":
            mode = "folds"
            continue
        if mode == "dots":
            line = tuple([int(el) for el in line.split(",")])
            dots.add(line)
        if mode == "folds":
            line = line.strip("fold along ")
            line = line.split("=")
            folds.append((line[0], int(line[1])))

    for fold in folds:
        (direction, line) = fold
        new_dots = dots.copy()
        if direction == "y":
            for point in filter(lambda p: p[1] > line, dots):
                length = line * 2
                (x, y) = point
                new_dots.remove(point)
                new_dots.add((x, length - y))
        if direction == "x":
            for point in filter(lambda p: p[0] > line, dots):
                width = line * 2
                (x, y) = point
                new_dots.remove(point)
                new_dots.add((width - x, y))
        dots = new_dots
    max_x = max(dots, key=lambda d: d[0])[0]
    max_y = max(dots, key=lambda d: d[1])[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in dots:
                print("█", end="")
            else:
                print(" ", end="")
        print("")
    ans = "FPEKBEJL"
    print(ans)

# task1()
task2()