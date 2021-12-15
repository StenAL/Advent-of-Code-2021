import queue

from util import *
from collections import *
import copy
import heapq
from functools import reduce

day = 15

def get_neighbors(point, x_max, y_max):
    (x, y) = point
    neighbors = set()
    if x > 0:
        neighbors.add((x-1, y))
    if y > 0:
        neighbors.add((x, y-1))
    if x < x_max - 1:
        neighbors.add((x + 1, y))
    if y < y_max - 1:
        neighbors.add((x, y + 1))
    return neighbors


def dijkstra(memo: dict[(int, int), int], x_max, y_max, levels):
    q = queue.PriorityQueue()
    for k in levels:
        memo[k] = 1000000000
        q.put((99, k))
    memo[(0, 0)] = 0
    while not q.empty():
        priority, node = q.get()
        neighbors = get_neighbors(node, x_max, y_max)
        for n in neighbors:
            d = memo[node] + levels[n]
            if d < memo[n]:
                memo[n] = d
                q.put((d, n))


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    points = defaultdict(int)
    y_max = len(data)
    x_max = len(data[0])
    for y in range(y_max):
        for x in range(x_max):
            points[(x, y)] = int(data[y][x])
    memo = dict()
    dijkstra(memo, x_max, y_max, points)
    ans = memo[(x_max - 1, y_max - 1)]
    print(ans)



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    points = defaultdict(int)
    y_max = len(data)
    x_max = len(data[0])
    for y in range(y_max):
        for x in range(x_max):
            for i in range(25):
                dx = x_max * (i // 5)
                dy = y_max * (i % 5)
                value = (int(data[y][x]) + dx + dy)
                while value > 9:
                    value -= 9
                points[(x + dx, y + dy)] = value
    y_max *= 5
    x_max *= 5
    memo = dict()
    dijkstra(memo, x_max, y_max, points)
    ans = memo[(x_max - 1, y_max - 1)]
    print(ans)


# task1()
task2()
