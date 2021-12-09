from util import *
from collections import *
from functools import reduce
import copy

day = 9

def get_neighbors(point, height, width):
    (x, y) = point
    neighbors = set()
    if x > 0:
        neighbors.add((x-1, y))
    if y > 0:
        neighbors.add((x, y-1))
    if x < width - 1:
        neighbors.add((x + 1, y))
    if y < height - 1:
        neighbors.add((x, y + 1))
    return neighbors

def task1():
    data = get_input_for_day(day)
    data = get_input_for_file("test")
    data = [[int(n) for n in list(row)] for row in data]
    height = len(data)
    width = len(data[0])
    ans = 0
    for y in range(height):
        for x in range(width):
            depth = data[y][x]
            neighbors = get_neighbors((x, y), height, width)
            neighbor_depths = [data[n[1]][n[0]] for n in neighbors]
            if len([d for d in neighbor_depths if d <= depth]) == 0:
                print(x, y, depth)
                ans += depth + 1
    print(ans)


def dfs(data, point, acc, height, width):
    (x, y) = point
    if point in acc:
        return
    acc.add(point)
    neighbors = get_neighbors((x, y), height, width)
    neighbors = [n for n in neighbors if data[n[1]][n[0]] != 9]
    for n in neighbors:
        dfs(data, n, acc, height, width)

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [[int(n) for n in list(row)] for row in data]
    seen = set()
    basins = []
    height = len(data)
    width = len(data[0])
    ans = 0
    for y in range(height):
        for x in range(width):
            if (x, y) in seen or data[y][x] == 9:
                continue
            basin = set()
            dfs(data, (x, y), basin, height, width)
            seen = seen.union(basin)
            basins.append(basin)
    basins.sort(key=lambda b: len(b), reverse=True)
    sizes = [len(b) for b in basins]
    ans = reduce(lambda acc, x: acc * x, sizes[:3], 1)
    print(ans)


# task1()
task2()
