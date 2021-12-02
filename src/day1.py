from util import *
from collections import *
import copy

day = 1


def task1():
    data = get_int_input_for_day(day)
    increases = [1 if data[i] > data[i-1] else 0 for i in range(1, len(data))]
    s = sum(increases)
    print(s)


def task2():
    data = get_int_input_for_day(day)

    triples = [[data[i-2], data[i-1], data[i]] for i in range(2, len(data))]
    triple_sums = [sum(triple) for triple in triples]
    increases = [1 if triple_sums[i] > triple_sums[i-1] else 0 for i in range(1, len(triple_sums))]
    s = sum(increases)
    print(s)

task1()
task2()