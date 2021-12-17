import math

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 17


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = data[0].strip("target area: ").split(", ")
    x_range = [int(el) for el in data[0].split("=")[1].split("..")]
    y_range = [int(el) for el in data[1].split("=")[1].split("..")]
    dy = y_range[1] - y_range[0]
    initial_y_speed = -1
    ans = -1
    while True:
        initial_y_speed += 1
        y_speed = initial_y_speed
        y = 0
        t = 0
        peak = 0
        while y >= y_range[0]:
            y += y_speed
            t += 1
            peak = max(peak, y)
            y_speed -= 1
            if y_range[0] <= y <= y_range[1]:
                ans = max(peak, ans)
        print(ans)



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = data[0].strip("target area: ").split(", ")
    x_range = [int(el) for el in data[0].split("=")[1].split("..")]
    y_range = [int(el) for el in data[1].split("=")[1].split("..")]
    valid_x = []
    for initial_x_speed in range(x_range[1] + 1):
        x = 0
        x_speed = initial_x_speed
        while x_speed >= 0:
            x += x_speed
            if x_range[0] <= x <= x_range[1]:
                valid_x.append(initial_x_speed)
                break
            x_speed -= 1
    min_y_speed = y_range[0]  # if lower than y_range[0], zone will be instantly overshot
    max_y_speed = abs(y_range[0])  # y forms a parabola where speed at 0,0 will be -1 * starting speed. If it's > y_range[0], zone will be overshot
    valid_y = []
    for initial_y_speed in range(min_y_speed, max_y_speed):
        y_speed = initial_y_speed
        y = 0
        while y >= y_range[0]:
            y += y_speed
            y_speed -= 1
            if y_range[0] <= y <= y_range[1]:
                valid_y.append(initial_y_speed)
                break
    valid_combos = []
    for initial_x_speed in valid_x:
        for initial_y_speed in valid_y:
            x_speed = initial_x_speed
            y_speed = initial_y_speed
            x = 0
            y = 0
            while y >= y_range[0]:
                x += x_speed
                y += y_speed
                if x_speed > 0:
                    x_speed -= 1
                y_speed -= 1
                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    valid_combos.append((initial_x_speed, initial_y_speed))
                    break
    ans = len(valid_combos)
    print(ans)


# task1()
task2()
