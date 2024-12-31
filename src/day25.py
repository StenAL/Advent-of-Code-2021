from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 25


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    cucumbers = defaultdict(set)
    x_size = -1
    y_size = -1
    for y, line in enumerate(data):
        y_size = max(y_size, y + 1)
        for x, c in enumerate(line):
            x_size = max(x_size, x + 1)
            if c in ["v", ">"]:
                cucumbers[c].add((x, y))
    moved = True
    steps = 0
    while moved:
        moved = False
        down = cucumbers["v"]
        right = cucumbers[">"]
        all = down.union(right)
        new_right = set()
        for c in right:
            x, y = c
            p = ((x + 1) % x_size, y)
            if p not in all:
                new_right.add(p)
                moved = True
            else:
                new_right.add((x, y))

        all = down.union(new_right)
        new_down = set()
        for c in cucumbers["v"]:
            x, y = c
            p = (x, (y + 1) % y_size)
            if p not in all:
                new_down.add(p)
                moved = True
            else:
                new_down.add((x, y))
        cucumbers[">"] = new_right
        cucumbers["v"] = new_down
        steps += 1
    print(steps)


task1()
