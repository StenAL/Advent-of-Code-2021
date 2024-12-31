from util import *
from collections import *
import copy
from functools import reduce
from math import prod

day = 24


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    ops = []
    all = []
    for line in data:
        if line.startswith("inp"):
            all.append(ops)
            ops = []
        ops.append(line)
    all.append(ops)
    all = all[1:]
    z_divisors = [int(s[4].split()[-1]) for s in all]
    somethings = [int(s[5].split()[-1]) for s in all]
    something_elses = [int(s[-3].split()[-1]) for s in all]
    # ['inp w', 'mul x 0', 'add x z', 'mod x 26', 'div z 1', 'add x 12', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25', 'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w', 'add y 6', 'mul y x', 'add z y']
    # ['inp w', 'mul x 0', 'add x z', 'mod x 26', 'div z 1', 'add x 11', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25', 'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w', 'add y 12', 'mul y x', 'add z y']
    # ['inp w', 'mul x 0', 'add x z', 'mod x 26', 'div z 1', 'add x 10', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25', 'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w', 'add y 5', 'mul y x', 'add z y']
    # ['inp w', 'mul x 0', 'add x z', 'mod x 26', 'div z 1', 'add x 10', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25', 'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w', 'add y 10', 'mul y x', 'add z y']
    # ['inp w', 'mul x 0', 'add x z', 'mod x 26', 'div z 26', 'add x -16', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25', 'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w', 'add y 7', 'mul y x', 'add z y']
    # every iteration same thing happens:
    # 1. w = input
    # 2. x = 0
    # 3. x = z | TODO COMBINE 2 and 3
    # 4. x = x % 26
    # 5. EITHER z = z / 26 or NOOP
    # 6. x = x + SOMETHING
    # 7. x = (x == w)
    # 8. x = (x == 0) | TODO COMBINE 7 and 8
    # 9. y = 0
    # 10. y = 25 | TODO COMBINE 9 and 10
    # 11. y = y * x
    # 12. y = y + 1
    # 13. z = z * y
    # 14. y = 0
    # 15. y = y + w
    # 16. y = y + SOMETHING ELSE
    # 17. y = y * x
    # 18. z = z + y
    # need z to be 0 at end

    # 2. x = z % 26
    # 5. EITHER (z = z // 26) or NOOP
    # 6. x = x + SOMETHING
    # 18. if x != input then (z = z * 26 + input + SOMETHING_ELSE)

    # a: [12, 11, 10, 10, -16, 14, 12, -4, 15, -7, -8, -4, -15, -8]
    # b: [ 6, 12,  5, 10,   7,  0,  4, 12, 14, 13, 10, 11,   9,  9]
    # z: [ 1,  1,  1,  1,  26,  1,  1, 26,  1, 26, 26, 26,  26, 26]

    candidates = []
    for i in range(1, 10):
        print(f"{i} / 9")
        for j in range(1, 10):
            for k in range(1, 10):
                for l in range(1, 10):
                    for m in range(1, 10):
                        for o in range(1, 10):
                            for p in range(1,10):
                                    # XXXX (93|82|71) X NN (18|29) 1 XX
                                    n1 = str(i) + str(j)  + str(k) + "9" + "3" + str(l) + str(m) + str(m) + "2" + "9" + "1" + str(o) + str(p)
                                    z = calc(n1, z_divisors, somethings, something_elses)
                                    if z < 100:
                                        candidates.append(n1)
    valid_models = []
    for n in candidates:
        for i in range(1,10):
            n1 = str(n) + str(i)
            z = calc(n1, z_divisors, somethings, something_elses)
            if z == 0:
                valid_models.append(n1)
    ans = max(valid_models)
    print(ans)
    return ans
        

def calc(n, z_divisors, somethings, something_elses):
    z = 0
    for i in range(len(str(n))):
        inp = int(str(n)[i])
        z_divisor = z_divisors[i]
        a = somethings[i]
        b = something_elses[i]

        if z % 26 + a != inp:
            z = (z // z_divisor) * 26 + inp + b
        else:
            z = z // z_divisor

    # print(f"input={str(n)} z={z}, (z % 26)={z%26}")
    return z


def sim(insns, n):
    n = str(n)
    i = 0
    registers = defaultdict(int)
    for insn in insns:
        command, a, *rest = insn.split()
        if command == "inp":
            if i >= len(n):
                return registers
            registers[a] = int(n[i])
            i += 1
            continue
        b = rest[0]
        if b.isalpha():
            b = registers[b]
        else:
            b = int(b)

        match command:
            case "add":
                registers[a] += b
            case "mul":
                registers[a] *= b
            case "div":
                registers[a] //= b
            case "mod":
                registers[a] %= b
            case "eql":
                registers[a] = 1 if registers[a] == b else 0
    return registers


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    ops = []
    all = []
    for line in data:
        if line.startswith("inp"):
            all.append(ops)
            ops = []
        ops.append(line)
    all.append(ops)
    all = all[1:]
    z_divisors = [int(s[4].split()[-1]) for s in all]
    somethings = [int(s[5].split()[-1]) for s in all]
    something_elses = [int(s[-3].split()[-1]) for s in all]
    candidates = []
    for i in range(1, 10):
        print(f"{i} / 9")
        for j in range(1, 10):
            for k in range(1, 10):
                for l in range(1, 10):
                    for m in range(1, 10):
                        for o in range(1, 10):
                            for p in range(1,10):
                                    # XXXX (93|82|71) X NN (18|29) 1 XX
                                    n1 = str(i) + str(j)  + str(k) + "7" + "1" + str(l) + str(m) + str(m) + "1" + "8" + "1" + str(o) + str(p)
                                    z = calc(n1, z_divisors, somethings, something_elses)
                                    if z < 100:
                                        # print(f"input={n1} z={z}, (z % 26)={z%26}")
                                        candidates.append(n1)
    valid_models = []
    for n in candidates:
        for i in range(1,10):
            n1 = str(n) + str(i)
            z = calc(n1, z_divisors, somethings, something_elses)
            if z == 0:
                valid_models.append(n1)
    ans = min(valid_models)
    print(ans)
    return ans


task1()
task2()
