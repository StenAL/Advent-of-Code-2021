from util import *
from collections import *
import copy

day = 3


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    word_len = len(data[0])
    data_len = len(data)
    data = "".join(data)
    counts = defaultdict(int)

    for i in range(len(data)):
        counts[i % word_len] += int(data[i])

    gamma = "".join(["1" if counts[k] > data_len / 2 else "0" for k in counts])
    gamma = int(gamma, 2)
    epsilon = gamma ^ int("1" * word_len, 2)  # invert bits in gamma
    ans = gamma * epsilon
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")

    word_len = len(data[0])

    def filter_data(old_data: list, i: int, mode: str):
        data_len = len(old_data)
        if data_len == 1:
            return old_data
        s = sum(int(el[i]) for el in old_data)
        if mode == "o2":
            if s >= data_len / 2:
                return [el for el in old_data if el[i] == "1"]
            else:
                return [el for el in old_data if el[i] == "0"]
        else:
            if s < data_len / 2:
                return [el for el in old_data if el[i] == "1"]
            else:
                return [el for el in old_data if el[i] == "0"]

    oxygen_data = data
    for i in range(word_len):
        oxygen_data = filter_data(oxygen_data, i, "o2")

    co_data = data
    for i in range(word_len):
        co_data = filter_data(co_data, i, "co2")

    oxygen_rating = int(oxygen_data[0], 2)
    co_rating = int(co_data[0], 2)
    ans = oxygen_rating * co_rating
    print(ans)


task1()
task2()
