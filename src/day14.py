from util import *
from collections import *
import copy
from functools import reduce

day = 14


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    input = list(data[0])
    formulas = defaultdict(str)
    for line in data[2:]:
        parts, result = line.split(" -> ")
        formulas[parts] = result
    queue = deque(input)
    iterations = 10
    for i in range(iterations):
        l = len(queue) - 1
        for _ in range(l):
            a = queue.popleft()
            b = queue[0]
            result = formulas[a + b]
            queue.append(a)
            queue.append(result)
        queue.rotate(-1)
    counts = Counter(queue)
    most_common = counts.most_common()[0]
    least_common = counts.most_common()[len(counts) - 1]
    ans = most_common[1] - least_common[1]
    print(ans)



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    formulas = defaultdict(str)
    for line in data[2:]:
        parts, result = line.split(" -> ")
        formulas[parts] = result
    iterations = 40
    pairs = defaultdict(int)
    for i in range(len(data[0]) - 1):
        pair = data[0][i:i+2]
        pairs[pair] += 1
    for i in range(iterations):
        new_pairs = pairs.copy()
        for k, v in pairs.items():
            a, b = k
            result = formulas[k]
            new_pairs[a + result] += v
            new_pairs[result + b] += v
            new_pairs[k] -= v
            if new_pairs[k] == 0:
                del new_pairs[k]
        pairs = new_pairs
    counts = defaultdict(int)
    for k, v in pairs.items():
        counts[k[0]] += v  # only count first character of each pair to avoid double counting
    counts[data[0][-1]] += 1  # last element always stays the same, add 1 to its count
    counts = Counter(counts)
    most_common = counts.most_common()[0]
    least_common = counts.most_common()[len(counts) - 1]
    ans = most_common[1] - least_common[1]
    print(ans)



# task1()
task2()
