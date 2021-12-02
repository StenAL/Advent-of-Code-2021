from util import *
from collections import *
import copy

day = 2


def task1():
    data = get_input_for_day(day)
    commands = [command.split(" ") for command in data]
    commands = [[d, int(amount)] for d, amount in commands]
    horizontal = 0
    vertical = 0
    for command in commands:
        if command[0] == "forward":
            horizontal += command[1]
        if command[0] == "down":
            vertical += command[1]
        if command[0] == "up":
            vertical -= command[1]

    ans = horizontal * vertical
    print(ans)


def task2():
    data = get_input_for_day(day)
    commands = [command.split(" ") for command in data]
    commands = [[d, int(amount)] for d, amount in commands]
    horizontal = 0
    vertical = 0
    aim = 0
    for command in commands:
        if command[0] == "forward":
            horizontal += command[1]
            vertical += aim * command[1]
        if command[0] == "down":
            aim += command[1]
        if command[0] == "up":
            aim -= command[1]

    ans = horizontal * vertical
    print(ans)

task1()
task2()