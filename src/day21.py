import itertools

from util import *
from collections import *
import copy
from functools import reduce
from math import prod, floor

day = 21


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    positions = [int(el.split("starting position: ")[1]) for el in data]
    scores = [0, 0]
    die = 1
    roll_count = 0
    stop = False
    while not stop:
        for i in range(len(positions)):
            roll_sum = 0
            for j in range(3):
                roll_sum += die
                die += 1
                if die > 100:
                    die %= 100
            roll_count += 3
            positions[i] = (positions[i] + roll_sum) % 10
            if positions[i] == 0:
                positions[i] = 10

            scores[i] += positions[i]
            if len([s for s in scores if s >= 1000]) > 0:
                stop = True
                break
    ans = min(scores) * roll_count
    print(ans)


class Game:
    def __init__(self, position1, position2, score1, score2, turn):
        self.position1 = position1
        self.position2 = position2
        self.score1 = score1
        self.score2 = score2
        self.turn = turn

    def __hash__(self):
        return hash((self.position1, self.position2, self.score1, self.score2, self.turn))

    def __eq__(self, other):
        return (self.position1, self.position2, self.score1, self.score2, self.turn) == (other.position1, other.position2, other.score1, other.score2, other.turn)

    def __repr__(self):
        return f"Turn {self.turn}: p1: {self.position1}, p2: {self.position2}, score {self.score1}:{self.score2}"

def get_winners(config: Game, possible_sums: dict[int, int], memo: dict[Game, tuple[int,int]]) -> tuple[int, int]:
    if config in memo:
        return memo[config]
    if config.score1 >= 21:
        return 1, 0
    if config.score2 >= 21:
        return 0, 1
    total_wins = [0, 0]
    for roll, roll_count in possible_sums.items():
        new_position = config.position1 if config.turn == 0 else config.position2
        new_position = (new_position + roll) % 10
        if new_position == 0:
            new_position = 10
        if config.turn == 0:
            wc = get_winners(Game(new_position, config.position2, min(config.score1 + new_position, 21), config.score2, (config.turn + 1) % 2), possible_sums, memo)
        else:
            wc = get_winners(Game(config.position1, new_position, config.score1, min(config.score2 + new_position, 21), (config.turn + 1) % 2), possible_sums, memo)
        total_wins[0] += wc[0] * roll_count
        total_wins[1] += wc[1] * roll_count
    total_wins = tuple(total_wins)
    memo[config] = total_wins
    return total_wins

def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    initial_positions = [int(el.split("starting position: ")[1]) for el in data]
    outcomes = [1, 2, 3]
    possible_rolls = [p for p in itertools.product(outcomes, repeat=3)]
    possible_sums = [sum(p) for p in possible_rolls]
    possible_sums = Counter(possible_sums)
    memo = dict()
    win_count = get_winners(Game(initial_positions[0], initial_positions[1], 0, 0, 0), possible_sums, memo)
    ans = max(win_count)
    print(ans)


# task1()
task2()
