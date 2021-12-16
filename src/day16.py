from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 16


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = bin(int(data[0], 16))[2:]
    data = list(data)
    state = "version"
    i = 0
    versions = [""]
    type_id = ""
    while i < len(data):
        if state == "version":
            versions[-1] += data[i]
            if len(versions[-1]) == 3:
                versions.append("")
                state = "type"
            i += 1
            continue
        elif state == "type":
            type_id += data[i]
            if len(type_id) == 3:
                if int(type_id, 2) == 4:
                    state = "literal_body"
                else:
                    state = "operator_length_type"
                type_id = ""
            i += 1
            continue
        elif state == "literal_body":
            content = data[i:i + 5]
            number = content[1:]
            if content[0] == "0":
                state = "version"
            i += 5
            continue
        elif state == "operator_length_type":
            length_type = data[i]
            if length_type == "0":
                subpackets_length = data[i + 1:i + 15]
                i += 1 + 15
                state = "version"
                continue
            elif length_type == "1":
                subpackets_count = data[i + 1:i + 11]
                i += 1 + 11
                state = "version"
                continue
    ans = sum([int(v, 2) for v in versions if v != ""])
    print(ans)

def parse(data: list[str]):
    state = "version"
    i = 0
    number = "0"
    version = -1
    type_id = -1
    length_type = -1
    subpackets_length = -1
    subpackets_count = -1
    operator = ""
    subpackets = []
    while i < len(data):
        # print(i, "".join(data[i:]), "".join(data), state)
        if state == "version":
            version = int("".join(data[i: i + 3]), 2)
            state = "type"
            i += 3
            continue
        elif state == "type":
            type_id = data[i: i + 3]
            type_id = int("".join(type_id), 2)
            if type_id == 4:
                state = "literal_body"
            else:
                if type_id == 0:
                    operator = "sum"
                if type_id == 1:
                    operator = "product"
                if type_id == 2:
                    operator = "min"
                if type_id == 3:
                    operator = "max"
                if type_id == 5:
                    operator = "gt"
                if type_id == 6:
                    operator = "lt"
                if type_id == 7:
                    operator = "eq"
                state = "operator_length_type"
            i += 3
            continue
        elif state == "literal_body":
            content = data[i:i + 5]
            number += "".join(content[1:])
            i += 5
            if content[0] == "0":
                break
            continue
        elif state == "operator_length_type":
            length_type = data[i]
            if length_type == "0":
                state = "subpackets_length"
            elif length_type == "1":
                state = "subpackets_count"
            i += 1
            continue
        elif state == "subpackets_length":
            subpackets_length = int("".join(data[i:i + 15]), 2)
            i += 15
            start = i
            while i < start + subpackets_length:
                p = parse(data[i:])
                subpackets.append(p)
                i += p["length"]
            break
        elif state == "subpackets_count":
            subpackets_count = int("".join(data[i:i + 11]), 2)
            i += 11
            while len(subpackets) < subpackets_count:
                p = parse(data[i:])
                subpackets.append(p)
                i += p["length"]
            break
    packet = {"number": int(number, 2), "operator": operator, "length": i, "version": version, "type_id": type_id, "length_type_id": length_type,
         "subpackets_length": subpackets_length, "subpackets_count": subpackets_count, "subpackets": subpackets}
    return packet


def compute(p):
    if p["operator"]:
        sub_values = [compute(subp) for subp in p["subpackets"]]
        operator = p["operator"]
        if operator == "sum":
            return sum(sub_values)
        if operator == "product":
            return prod(sub_values)
        if operator == "min":
            return min(sub_values)
        if operator == "max":
            return max(sub_values)
        if operator == "gt":
            return 1 if sub_values[0] > sub_values[1] else 0
        if operator == "lt":
            return 1 if sub_values[0] < sub_values[1] else 0
        if operator == "eq":
            return 1 if sub_values[0] == sub_values[1] else 0
    return p["number"]


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = bin(int(data[0], 16))[2:].zfill(len(data[0] * 4))
    data = list(data)
    p = parse(data)
    ans = compute(p)
    print(ans)


# task1()
task2()
