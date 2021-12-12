from util import *
from collections import *
import copy
from functools import reduce

day = 12

def get_paths(node, neighbors, seen, paths):
    if node == "end":
        paths.append(seen)
        return
    valid_neighbors = set()
    for n in neighbors[node]:
        if n != "start" and (n.isupper() or n not in seen):
            valid_neighbors.add(n)

    for neighbor in valid_neighbors:
        get_paths(neighbor, neighbors, seen.union({neighbor}), paths)
    return paths


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test2")
    data = [line.split("-") for line in data]
    neighbors = defaultdict(set)
    for s, d in data:
        neighbors[s].add(d)
        neighbors[d].add(s)
    ans = len(get_paths("start", neighbors, set(), []))
    print(ans)


def get_paths2(node, neighbors, seen: dict[str, int], path, paths, double_visit):
    if node == "end":
        s = "-".join(path)
        if s not in paths:
            paths.add(s)
        return
    valid_neighbors = set()
    for n in neighbors[node]:
        if n == "start":
            continue
        if n.isupper():
            valid_neighbors.add(n)
        if n == double_visit and seen[n] <= 1:
            valid_neighbors.add(n)
        if seen[n] == 0:
            valid_neighbors.add(n)
    for neighbor in valid_neighbors:
        seen_copy = seen.copy()
        seen_copy[neighbor] += 1
        path_copy = path.copy()
        path_copy.append(neighbor)
        get_paths2(neighbor, neighbors, seen_copy, path_copy, paths, double_visit)
    return paths

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [line.split("-") for line in data]
    neighbors = defaultdict(set)
    for s, d in data:
        neighbors[s].add(d)
        neighbors[d].add(s)
    paths = set()
    for s in neighbors:
        if s != "start" and s != "end" and s.islower():
            paths = (get_paths2("start", neighbors, defaultdict(int), ["start"], paths, s))

    ans = len(paths)
    print(ans)


# task1()
task2()
