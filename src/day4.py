from util import *
from collections import *
import copy

day = 4


def task1():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    numbers = data[0].split(",")
    data = [line.split() for line in data]
    boards_data = [data[i:i+5] for i in range(2, len(data), 6)]

    board_height = len(boards_data[0])
    board_width = len(boards_data[0][0])
    boards = []
    for i in range(len(boards_data)):
        board = boards_data[i]
        boards.append(dict())
        for y in range(board_height):
            for x in range(board_width):
                boards[i][(x, y)] = board[y][x]

    def is_winner(board):
        for x in range(board_width):
            row = [board[x, y] for y in range(board_height)]
            col = [board[y, x] for y in range(board_height)]
            if row.count("X") == board_width or col.count("X") == board_width:
                return True
        return False

    winner = None
    for number in numbers:
        for board in boards:
            for key in board.keys():
                if board[key] == number:
                    board[key] = "X"
            if is_winner(board):
                winner = board
                break
        if winner:
            break

    s = sum([int(v) for v in winner.values() if v != "X"])
    ans = s * int(number)
    print(ans)



def task2():
    data = get_input_for_day(day)
    # data = get_input_for_file("test")
    numbers = data[0].split(",")
    data = [line.split() for line in data]
    boards_data = [data[i:i+5] for i in range(2, len(data), 6)]

    board_height = len(boards_data[0])
    board_width = len(boards_data[0][0])
    boards = []
    for i in range(len(boards_data)):
        board = boards_data[i]
        boards.append(dict())
        for y in range(board_height):
            for x in range(board_width):
                boards[i][(x, y)] = board[y][x]

    def is_winner(board):
        for x in range(board_width):
            row = [board[x, y] for y in range(board_height)]
            col = [board[y, x] for y in range(board_height)]
            if row.count("X") == board_width or col.count("X") == board_width:
                return True
        return False

    loser = None
    for number in numbers:
        losers = []
        for board in boards:
            for key in board.keys():
                if board[key] == number:
                    board[key] = "X"
            if not is_winner(board):
                losers.append(board)
        if len(losers) == 0:
            loser = boards[0]
            break
        boards = losers

    s = sum([int(v) for v in loser.values() if v != "X"])
    ans = s * int(number)
    print(ans)


task1()
task2()
