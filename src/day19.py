from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 19


class Scanner:
    def __init__(self, points: set[tuple[int, int, int]], name: str):
        self.location = None
        self.locked = None
        self.name = name

        permutations = []
        for i in [0, 1, 2]:
            shifted = []
            for point in points:
                shifted.append(tuple(point[i:] + point[:i]))
            initial = shifted.copy()
            counter_clockwise_1 = [(x, z, -y) for x, y, z in shifted]
            counter_clockwise_2 = [(x, -y, -z) for x, y, z in shifted]
            counter_clockwise_3 = [(x, -z, y) for x, y, z in shifted]

            rotate_180 = [(-x, -y, z) for x, y, z in shifted]
            rotate_180_clockwise_1 = [(-x, z, y) for x, y, z in shifted]
            rotate_180_clockwise_2 = [(-x, y, -z) for x, y, z in shifted]
            rotate_180_clockwise_3 = [(-x, -z, -y) for x, y, z in shifted]
            permutations += [initial, counter_clockwise_1, counter_clockwise_2, counter_clockwise_3, rotate_180, rotate_180_clockwise_1, rotate_180_clockwise_2, rotate_180_clockwise_3]
        arrangements = []
        for el in permutations:
            arrangements.append(Arrangement(set(el)))
        self.arrangements = arrangements


    def lock(self, arrangement, location: tuple[int, int, int]):
        self.locked = arrangement
        self.location = location


class Arrangement:
    def __init__(self, points: set[tuple[int, int, int]]):
        self.points = defaultdict(set)
        distances = set()
        for el1 in points:
            for el2 in points:
                if el1 != el2:
                    d = (el1[0] - el2[0], el1[1] - el2[1], el1[2] - el2[2])
                    self.points[el1].add(d)
                    distances.add(d)
        self.distances = distances

    def __repr__(self):
        return f"{len(self.points)} points"


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    raw_scanners = []
    for line in data:
        if "scanner" in line:
            raw_scanners.append(set())
            continue
        if line == "":
            continue
        coordinates = tuple([int(el) for el in line.split(",")])
        raw_scanners[-1].add(coordinates)
    scanners = []
    for i in range(len(raw_scanners)):
        scanner = raw_scanners[i]
        scanners.append(Scanner(scanner, str(i)))

    scanners[0].lock(scanners[0].arrangements[0], (0, 0, 0))
    q = [scanners[0]]
    done = set()
    beacons = set(scanners[0].locked.points.keys())
    while len(q) > 0:
        locked_scanner = q.pop(0)
        done.add(locked_scanner)
        locked_arrangement = locked_scanner.locked
        for scanner in scanners:
            if scanner in done:
                continue
            # print(f"checking scanner {scanner.name}'s overlap with scanner {locked_scanner.name}")
            for arrangement in scanner.arrangements:
                matches = set()
                for k1, v1 in locked_arrangement.points.items():
                    for k2, v2 in arrangement.points.items():
                        if len(v1.intersection(v2)) >= 11:
                            # print(f"found point {k2} from scanner {scanner.name} in scanner {locked_scanner.name}: {k1}")
                            matches.add((k2, k1))
                if len(matches) >= 12:
                    matched_point = next(iter(matches))
                    location_delta = (matched_point[1][0] - matched_point[0][0], matched_point[1][1] - matched_point[0][1], matched_point[1][2] - matched_point[0][2])
                    location = (locked_scanner.location[0] + location_delta[0], locked_scanner.location[1] + location_delta[1], locked_scanner.location[2] + location_delta[2])
                    # print(f"s{scanner.name} at {location} ({location_delta} relative to s{locked_scanner.name})")
                    scanner.lock(arrangement, location)
                    q.append(scanner)
                    for beacon in arrangement.points:
                        beacons.add((beacon[0] + location[0], beacon[1] + location[1], beacon[2] + location[2]))
                    break
    ans = len(beacons)
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    raw_scanners = []
    for line in data:
        if "scanner" in line:
            raw_scanners.append(set())
            continue
        if line == "":
            continue
        coordinates = tuple([int(el) for el in line.split(",")])
        raw_scanners[-1].add(coordinates)
    scanners = []
    for i in range(len(raw_scanners)):
        scanner = raw_scanners[i]
        scanners.append(Scanner(scanner, str(i)))

    scanners[0].lock(scanners[0].arrangements[0], (0, 0, 0))
    q = [scanners[0]]
    done = set()
    beacons = set(scanners[0].locked.points.keys())
    while len(q) > 0:
        locked_scanner = q.pop(0)
        done.add(locked_scanner)
        locked_arrangement = locked_scanner.locked
        for scanner in scanners:
            if scanner in done:
                continue
            # print(f"checking scanner {scanner.name}'s overlap with scanner {locked_scanner.name}")
            for arrangement in scanner.arrangements:
                matches = set()
                for k1, v1 in locked_arrangement.points.items():
                    for k2, v2 in arrangement.points.items():
                        if len(v1.intersection(v2)) >= 11:
                            # print(f"found point {k2} from scanner {scanner.name} in scanner {locked_scanner.name}: {k1}")
                            matches.add((k2, k1))
                if len(matches) >= 12:
                    matched_point = next(iter(matches))
                    location_delta = (matched_point[1][0] - matched_point[0][0], matched_point[1][1] - matched_point[0][1], matched_point[1][2] - matched_point[0][2])
                    location = (locked_scanner.location[0] + location_delta[0], locked_scanner.location[1] + location_delta[1], locked_scanner.location[2] + location_delta[2])
                    # print(f"s{scanner.name} at {location} ({location_delta} relative to s{locked_scanner.name})")
                    scanner.lock(arrangement, location)
                    q.append(scanner)
                    for beacon in arrangement.points:
                        beacons.add((beacon[0] + location[0], beacon[1] + location[1], beacon[2] + location[2]))
                    break

    distances = set()
    for e1 in scanners:
        for e2 in scanners:
            if e1 != e2:
                distances.add(abs(e1.location[0] - e2.location[0]) + abs(e1.location[1] - e2.location[1]) + abs(e1.location[2] - e2.location[2]))
    ans = max(distances)
    print(ans)


# task1()
task2()
