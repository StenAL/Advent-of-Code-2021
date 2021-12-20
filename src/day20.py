from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 20

def get_neighbors(p):
    (x, y) = p
    neighbors = []
    for d1 in range(-1, 2):
        for d2 in range(-1, 2):
            neighbors.append((x + d2, y + d1))
    # print(p, neighbors)
    return neighbors


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    mode = "algorithm"
    algorithm = ""
    y = -1
    points = dict()
    for line in data:
        if mode == "algorithm":
            algorithm = line
            mode = "image"
            continue
        if mode == "image":
            for x in range(len(line)):
                if line[x] == "#":
                    points[(x, y)] = 1
                else:
                    points[(x, y)] = 0

            y += 1

    iterations = 2
    for i in range(iterations):
        new_points = points.copy()
        seen = set()
        for point in points:
            neighbors = get_neighbors(point)
            for p in neighbors:
                if p in seen:
                    continue

                neighbors2 = get_neighbors(p)
                index = []
                for n in neighbors2:
                    if n in points and points[n] == 1:
                        index.append("1")
                        continue
                    if n in points and points[n] == 0:
                        index.append("0")
                        continue
                    if i % 2 == 1:
                        index.append("1")
                        continue
                    index.append("0")
                index_int = int("".join(index), 2)
                value = algorithm[index_int]
                new_points[p] = 1 if value == "#" else 0
                seen.add(p)
        points = new_points
    lit = [k for k, v in points.items() if v == 1]
    ans = len(lit)
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    mode = "algorithm"
    algorithm = ""
    y = -1
    points = dict()
    for line in data:
        if mode == "algorithm":
            algorithm = line
            mode = "image"
            continue
        if mode == "image":
            for x in range(len(line)):
                if line[x] == "#":
                    points[(x, y)] = 1
                else:
                    points[(x, y)] = 0

            y += 1

    iterations = 50
    for i in range(iterations):
        new_points = points.copy()
        seen = set()
        for point in points:
            neighbors = get_neighbors(point)
            for p in neighbors:
                if p in seen:
                    continue

                neighbors2 = get_neighbors(p)
                index = []
                for n in neighbors2:
                    if n in points and points[n] == 1:
                        index.append("1")
                        continue
                    if n in points and points[n] == 0:
                        index.append("0")
                        continue
                    if i % 2 == 1:
                        index.append("1")
                        continue
                    index.append("0")
                index_int = int("".join(index), 2)
                value = algorithm[index_int]
                new_points[p] = 1 if value == "#" else 0
                seen.add(p)
        points = new_points
        print(i)
    lit = [k for k, v in points.items() if v == 1]
    ans = len(lit)
    print(ans)


# task1()
task2()
