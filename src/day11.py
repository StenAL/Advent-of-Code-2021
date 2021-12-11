from util import *
from collections import *
import copy
from functools import reduce

day = 11

def get_neighbors(p, x_max, y_max):
    (x, y) = p
    neighbors = set()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            neighbors.add((x + dx, y + dy))
    neighbors.remove(p)
    neighbors = set(filter(lambda a: x_max >= a[0] >= 0 and y_max >= a[1] >= 0, neighbors))
    return neighbors

def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    levels = defaultdict(int)
    x_max = len(data) - 1
    y_max = len(data[0]) - 1
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            levels[(x, y)] = int(line[x])
    steps = 100
    ans = 0
    for i in range(steps):
        flash_happened = True
        flashed = set()
        for k in levels:
            levels[k] += 1
        while flash_happened:
            flash_happened = False
            for k, v in levels.items():
                if v > 9 and k not in flashed:
                    flashed.add(k)
                    flash_happened = True
                    ans += 1
                    for neighbor in get_neighbors(k, x_max, y_max):
                        levels[neighbor] += 1
        for k in flashed:
            levels[k] = 0
    print(ans)





def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    levels = defaultdict(int)
    x_max = len(data) - 1
    y_max = len(data[0]) - 1
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            levels[(x, y)] = int(line[x])
    ans = 0
    while True:
        ans += 1
        flash_happened = True
        flashed = set()
        for k in levels:
            levels[k] += 1
        while flash_happened:
            flash_happened = False
            for k, v in levels.items():
                if v > 9 and k not in flashed:
                    flashed.add(k)
                    flash_happened = True
                    for neighbor in get_neighbors(k, x_max, y_max):
                        levels[neighbor] += 1
        for k in flashed:
            levels[k] = 0
        if len(flashed) == len(levels):
            break
    print(ans)


# task1()
task2()
