from util import *
from collections import *
import copy

day = 5


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [line.replace(" -> ", ",").split(",") for line in data]
    data = [[int(point) for point in points] for points in data]
    straight_lines = [points for points in data if points[0] == points[2] or points[1] == points[3]]
    streams = defaultdict(int)
    for points in straight_lines:
        if points[0] + points[1] < points[2] + points[3]:
            start = points[0:2]
            end = points[2:]
        else:
            start = points[2:]
            end = points[0:2]
        for x in range(end[0] - start[0] + 1):
            for y in range(end[1] - start[1] + 1):
                streams[(x + start[0], y + start[1])] += 1

    dangerous_points = [val for val in streams.values() if val >= 2]
    ans = len(dangerous_points)
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [line.replace(" -> ", ",").split(",") for line in data]
    data = [[int(point) for point in points] for points in data]
    streams = defaultdict(int)
    for points in data:
        if points[0] == points[2] or points[1] == points[3]:
            # Straight line
            if points[0] + points[1] < points[2] + points[3]:
                start = points[0:2]
                end = points[2:]
            else:
                start = points[2:]
                end = points[0:2]
            for x in range(end[0] - start[0] + 1):
                for y in range(end[1] - start[1] + 1):
                    streams[(x + start[0], y + start[1])] += 1
        else:
            # Diagonal
            l = abs(points[0] - points[2])
            if points[1] < points[3]:
                start = points[0:2]
                if points[0] < points[2]:
                    dir = "right"
                else:
                    dir = "left"
            else:
                start = points[2:]
                if points[0] < points[2]:
                    dir = "left"
                else:
                    dir = "right"
            for x in range(l + 1):
                if dir == "right":
                    p = (start[0] + x, start[1] + x)
                else:
                    p = (start[0] - x, start[1] + x)
                streams[p] += 1


    dangerous_points = [val for val in streams.values() if val >= 2]
    ans = len(dangerous_points)
    print(ans)


task1()
task2()
