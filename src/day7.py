from util import *
from collections import *
import copy

day = 7


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [int(el) for el in data[0].split(",")]
    minimum = min(data)
    maximum = max(data)

    min_fuel = -1
    optimal_position = -1
    for i in range(minimum, maximum + 1):
        fuel = 0
        for position in data:
            fuel += abs(position - i)
        if fuel < min_fuel or min_fuel == -1:
            min_fuel = fuel
            optimal_position = i
    print(min_fuel)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [int(el) for el in data[0].split(",")]
    minimum = min(data)
    maximum = max(data)

    min_fuel = -1
    optimal_position = -1
    for i in range(minimum, maximum + 1):
        fuel = 0
        for position in data:
            d = abs(position - i)
            fuel += (d * (1 + d) // 2)  # Sum of arithmetic sequence increasing in steps of 1 consisting of 1, 2, 3 ... d
        if fuel < min_fuel or min_fuel == -1:
            min_fuel = fuel
            optimal_position = i
    print(min_fuel)


# task1()
task2()
