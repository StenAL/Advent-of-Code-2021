from util import *
from collections import *
import copy

day = 8


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [line.split(" | ") for line in data]
    ans = 0
    for signal_sequence, display in data:
        signal_sequence = signal_sequence.split(" ")
        display = display.split(" ")
        easy_signals = [s for s in signal_sequence if len(s) in [2, 4, 3, 7]]  # corresponding to 1, 4, 7, 8
        digit_to_signals = defaultdict(set)
        for signals in easy_signals:
            if len(signals) == 2:
                digit_to_signals[1] = set(signals)
            elif len(signals) == 4:
                digit_to_signals[4] = set(signals)
            elif len(signals) == 3:
                digit_to_signals[7] = set(signals)
            elif len(signals) == 7:
                digit_to_signals[8] = set(signals)

        easy_digits = 0
        for digit in display:
            if set(digit) in digit_to_signals.values():
                easy_digits += 1
        ans += easy_digits
    print(ans)


def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    data = [line.split(" | ") for line in data]
    positions = {"up", "up_left", "up_right", "middle", "down_left", "down_right", "down"}
    letters = {"a", "b", "c", "d", "e", "f", "g"}
    values = []
    for signal_sequence_input, display in data:
        signal_to_candidates = defaultdict(lambda: positions.copy())
        signal_sequence = signal_sequence_input.split(" ")
        for signals in signal_sequence:
            filled = positions.copy()
            empty = positions.copy()
            if len(signals) == 2:  # 1
                filled = {"up_right", "down_right"}
                empty = positions.difference(filled)
            elif len(signals) == 4:  # 4
                filled = {"up_left", "up_right", "middle", "down_right"}
                empty = positions.difference(filled)
            elif len(signals) == 3:  # 7
                filled = {"up", "up_right", "down_right"}
                empty = positions.difference(filled)
            elif len(signals) == 7:  # 8
                pass  # no-op
            elif len(signals) == 6:
                empty = {"middle", "up_right", "down_left"}  # 0, 6, 9
                filled = positions.copy()
            elif len(signals) == 5:
                empty = {"up_left", "down_right", "down_left", "up_right"}  # 2, 3, 5
                filled = positions.copy()
            for signal in signals:
                signal_to_candidates[signal] = filled.intersection(signal_to_candidates[signal])
            for signal in letters.difference(signals):
                signal_to_candidates[signal] = empty.intersection(signal_to_candidates[signal])
            new_signal_to_candidates = signal_to_candidates.copy()
            for k, v in signal_to_candidates.items():
                if len(v) == 1:
                    for l in letters.difference({k}):
                        new_signal_to_candidates[l] = new_signal_to_candidates[l].difference(v)
            signal_to_candidates = new_signal_to_candidates
        display = display.split(" ")
        nums = []
        for digit in display:
            filled = set()
            for signal in digit:
                filled = filled.union(signal_to_candidates[signal])
            if filled == {"up", "up_left", "up_right", "down_left", "down_right", "down"}:
                nums.append("0")
            elif filled == {"up_right", "down_right"}:
                nums.append("1")
            elif filled == {"up", "up_right", "middle", "down_left", "down"}:
                nums.append("2")
            elif filled == {"up", "up_right", "middle", "down_right", "down"}:
                nums.append("3")
            elif filled == {"up_left", "up_right", "middle", "down_right"}:
                nums.append("4")
            elif filled == {"up", "up_left", "middle", "down_right", "down"}:
                nums.append("5")
            elif filled == {"up", "up_left", "middle", "down_left", "down_right", "down"}:
                nums.append("6")
            elif filled == {"up", "up_right", "down_right"}:
                nums.append("7")
            elif filled == positions:
                nums.append("8")
            elif filled == {"up", "up_left", "up_right", "middle", "down_right", "down"}:
                nums.append("9")
        values.append(int("".join(nums)))
    ans = sum(values)
    print(ans)

# task1()
task2()
