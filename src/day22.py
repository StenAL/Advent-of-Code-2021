from typing import Optional

from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 22


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    on = set()
    for line in data:
        command, raw_ranges = line.split(" ")
        raw_ranges = [r.split("..") for r in raw_ranges.split(",")]
        ranges = []
        for r in raw_ranges:
            beginning = int(r[0].split("=")[1])
            end = int(r[1])
            if end < -50:
                continue
            if beginning > 50:
                continue
            if beginning < -50:
                beginning = -50
            if end > 50:
                end = 50
            ranges.append((beginning, end))
        if len(ranges) < 3:
            continue
        for x in range(ranges[0][0], ranges[0][1] + 1):
            for y in range(ranges[1][0], ranges[1][1] + 1):
                for z in range(ranges[2][0], ranges[2][1] + 1):
                    p = (x, y, z)
                    if command == "on":
                        on.add(p)
                    if command == "off" and p in on:
                        on.remove(p)
    ans = len(on)
    print(ans)


class Cube:
    def __init__(self, coords: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        self.coords = tuple(coords)

    def volume(self):
        dx = abs(self.coords[0][0] - self.coords[0][1]) + 1
        dy = abs(self.coords[1][0] - self.coords[1][1]) + 1
        dz = abs(self.coords[2][0] - self.coords[2][1]) + 1
        return dx * dy * dz

    def __str__(self):
        return f"{self.coords}"

    def __repr__(self):
        return self.__str__()



def intersection(a: Cube, b: Cube) -> Optional[Cube]:
    (a_min_x, a_max_x), (a_min_y, a_max_y), (a_min_z, a_max_z) = a.coords
    (b_min_x, b_max_x), (b_min_y, b_max_y), (b_min_z, b_max_z) = b.coords
    x_overlap = a_max_x >= b_min_x and a_min_x <= b_max_x
    y_overlap = a_max_y >= b_min_y and a_min_y <= b_max_y
    z_overlap = a_max_z >= b_min_z and a_min_z <= b_max_z
    if not (x_overlap and y_overlap and z_overlap):
        return None
    x = sorted([a_min_x, a_max_x, b_min_x, b_max_x])
    x_from = x[1]
    x_to = x[2]
    y = sorted([a_min_y, a_max_y, b_min_y, b_max_y])
    y_from = y[1]
    y_to = y[2]
    z = sorted([a_min_z, a_max_z, b_min_z, b_max_z])
    z_from = z[1]
    z_to = z[2]
    r = Cube(((x_from, x_to), (y_from, y_to), (z_from, z_to)))
    return r


def subtract(a: Cube, b: Cube) -> list[Cube]:
    i = intersection(a, b)
    if not i:
        return [a]
    (a_min_x, a_max_x), (a_min_y, a_max_y), (a_min_z, a_max_z) = a.coords
    (b_min_x, b_max_x), (b_min_y, b_max_y), (b_min_z, b_max_z) = b.coords
    result = []
    if b_max_z < a_max_z:
        above = Cube(((a_min_x, a_max_x), (a_min_y, a_max_y), (b_max_z + 1, a_max_z)))
        result.append(above)
        a_max_z = b_max_z
    if b_max_x < a_max_x:
        right = Cube(((b_max_x + 1, a_max_x), (a_min_y, a_max_y), (a_min_z, a_max_z)))
        result.append(right)
        a_max_x = b_max_x
    if b_min_x > a_min_x:
        left = Cube(((a_min_x, b_min_x - 1), (a_min_y, a_max_y), (a_min_z, a_max_z)))
        result.append(left)
        a_min_x = b_min_x
    if b_max_y < a_max_y:
        up = Cube(((a_min_x, a_max_x), (b_max_y + 1, a_max_y), (a_min_z, a_max_z)))
        result.append(up)
        a_max_y = b_max_y
    if b_min_y > a_min_y:
        down = Cube(((a_min_x, a_max_x), (a_min_y, b_min_y - 1), (a_min_z, a_max_z)))
        result.append(down)
        a_min_y = b_min_y
    if b_min_z > a_min_z:
        down = Cube(((a_min_x, a_max_x), (a_min_y, a_max_y), (a_min_z, b_min_z - 1)))
        result.append(down)
    return result


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    instructions = []
    for line in data:
        command, raw_ranges = line.split(" ")
        raw_ranges = [r.split("..") for r in raw_ranges.split(",")]
        ranges = []
        for r in raw_ranges:
            beginning = int(r[0].split("=")[1])
            end = int(r[1])
            ranges.append((beginning, end))
        instructions.append((command, Cube(ranges)))

    cubes = []
    for command, b in instructions:
        new_cubes = []
        for a in cubes:  # remove all intersections of existing cubes and new cube
            new_cubes += subtract(a, b)
        if command == "on":  # if "on", add new cube to existing cubes. Volume isn't double-counted since all intersections have been removed by lines 142-143
            new_cubes.append(b)
        else:
            pass
        cubes = new_cubes

    ans = sum([c.volume() for c in cubes])
    print(ans)


# task1()
task2()
