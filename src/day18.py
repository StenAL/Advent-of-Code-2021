from util import *
from collections import *
import copy
from functools import reduce
from math import prod, floor, ceil

day = 18


class Number:
    def __init__(self, value, left, right):
        self.parent = None
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f"[{self.left},{self.right}]"

    def set_parent(self, parent):
        self.parent = parent

    def copy(self):
        l = self.left.copy() if self.left else None
        r = self.right.copy() if self.right else None
        v = self.value if self.value is not None else None
        root = Number(v, l, r)
        if l:
            l.set_parent(root)
        if r:
            r.set_parent(root)
        return root


def explode(n: Number, level: int):
    if level == 5 and n.value is None:
        node = n
        seen = {n}
        while node.parent:
            node = node.parent
            if node.left and node.left not in seen:
                node = node.left
                while node.right:
                    node = node.right
                node.value += n.left.value
                break
            seen.add(node)
        node = n
        seen = {n}
        while node.parent:
            node = node.parent
            if node.right and node.right not in seen:
                node = node.right
                while node.left:
                    node = node.left
                node.value += n.right.value
                break
            seen.add(node)

        zero = Number(0, None, None)
        zero.set_parent(n.parent)
        if n == n.parent.left:
            n.parent.left = zero
        if n == n.parent.right:
            n.parent.right = zero

    if n.left:
        explode(n.left, level + 1)
    if n.right:
        explode(n.right, level + 1)


def split(n: Number):
    if n.value and n.value >= 10:
        n.left = Number(floor(n.value / 2), None, None)
        n.right = Number(ceil(n.value / 2), None, None)
        n.left.set_parent(n)
        n.right.set_parent(n)
        n.value = None
        return True
    elif n.value is not None:
        return False
    if split(n.left):
        return True
    if split(n.right):
        return True
    return False


def reduce(n: Number):
    keep_going = True
    while keep_going:
        explode(n, 1)
        if not split(n):
            keep_going = False
    return n


def add(a: Number, b: Number):
    a_copy = a.copy()
    b_copy = b.copy()
    p = Number(None, a_copy, b_copy)
    a_copy.set_parent(p)
    b_copy.set_parent(p)
    return reduce(p)


def magnitude(n: Number):
    if n.value is not None:
        return n.value
    else:
        return magnitude(n.left) * 3 + magnitude(n.right) * 2

def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    acc = []
    for line in data:
        for i in range(len(line)):
            c = line[i]
            if c == "[":
                pass
            elif c == "]":
                right = acc.pop()
                left = acc.pop()
                parent = Number(None, left, right)
                right.set_parent(parent)
                left.set_parent(parent)
                acc.append(parent)
            elif c == ",":
                pass
            else:
                acc.append(Number(int(c), None, None))
    result = acc[0]
    for el in acc[1:]:
        result = add(result, el)
    ans = magnitude(result)
    print(ans)

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    acc = []
    for line in data:
        for i in range(len(line)):
            c = line[i]
            if c == "[":
                pass
            elif c == "]":
                right = acc.pop()
                left = acc.pop()
                parent = Number(None, left, right)
                right.set_parent(parent)
                left.set_parent(parent)
                acc.append(parent)
            elif c == ",":
                pass
            else:
                acc.append(Number(int(c), None, None))
    ans = -1
    for el in acc:
        for el2 in acc:
            s1 = magnitude(add(el, el2))
            s2 = magnitude(add(el, el2))
            ans = max(ans, s1, s2)
    print(ans)

# task1()
task2()
