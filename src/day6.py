from util import *
from collections import *
import copy

day = 6


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    fish = defaultdict(int) # days -> count
    for el in data[0].split(","):
        fish[int(el)] += 1

    steps = 80
    for _ in range(steps):
        new_fish = defaultdict(int)
        for days, count in fish.items():
            # print(days, count)
            days -= 1
            if days == -1:
                days = 6
                new_fish[8] = count
            new_fish[days] += count
        fish = new_fish

    ans = sum(v for v in fish.values())
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    fish = defaultdict(int)  # days -> count
    for el in data[0].split(","):
        fish[int(el)] += 1

    steps = 256
    for _ in range(steps):
        new_fish = defaultdict(int)
        for days, count in fish.items():
            # print(days, count)
            days -= 1
            if days == -1:
                days = 6
                new_fish[8] = count
            new_fish[days] += count
        fish = new_fish

    ans = sum(v for v in fish.values())
    print(ans)

# task1()
task2()
