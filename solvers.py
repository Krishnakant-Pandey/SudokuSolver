from validatiors import find_empty, valid_number, valid_candidates
import config
import copy


def fill_naked_single(board, loc):
    x, y = loc
    if board[y][x] == 0:
        possibilities = []
        for i in range(10):
            if valid_number(board, i, loc):
                possibilities.append(i)

        if len(possibilities) == 1:
            board[y][x] = possibilities[0]
            return 1
        else:
            return 0
    else:
        return 0


# Fills all the cells that have only one possible answer a.k.a naked singles
def fill_naked_singles(board):
    flag = True
    total_singles = 0
    round_singles = 0

    while flag:
        for y in range(9):
            for x in range(9):
                loc = x, y
                singles = fill_naked_single(board, loc)
                round_singles += singles

        total_singles += round_singles
        if round_singles == 0:
            flag = False

        else:
            round_singles = 0

    return total_singles


def solve(board):
    find = find_empty(board)

    if not find:
        return True

    else:
        loc = find_empty(board)
        x, y = loc

    for i in range(1, 10):
        if valid_number(board, i, loc):
            board[y][x] = i

            if solve(board):
                return True

            board[y][x] = 0

    return False


def solution(board):
    fill_naked_singles(board)

    config.backtracks = 0
    find = find_empty(board)

    if not find:
        return True

    else:
        loc = find_empty(board)
        x, y = loc

    for i in range(1, 10):
        if valid_number(board, i, loc):
            board[y][x] = i

            if solve(board):
                return True
            config.backtracks += 1
            board[y][x] = 0

    return False


# Brute Force solver using backtracking
def solver(board):
    for y in range(9):
        for x in range(9):
            loc = x, y
            if board[y][x] == 0:
                for n in range(1, 10):
                    if valid_number(board, n, loc):
                        board[y][x] = n
                        solver(board)
                        board[y][x] = 0
                return
    return


def is_solvable(board):
    ref_board = copy.deepcopy(board)
    solve(board)

    if board == ref_board:
        return False
    else:
        return True


def fill_row_table(board):
    row_table = config.row_table()
    for y, row in enumerate(board):
        for x, elem in enumerate(row):
            loc = x, y
            if board[y][x] == 0:
                candidates = valid_candidates(board, loc)
                for candidate in candidates:
                    (row_table[y])["freq"][candidate - 1] += 1
                    (row_table[y])["tracker"][candidate - 1].add(x)

    return row_table


def fill_column_table(board):
    column_table = config.column_table()

    for x in range(9):
        for y in range(9):
            loc = x, y
            if board[y][x] == 0:
                candidates = valid_candidates(board, loc)
                for candidate in candidates:
                    (column_table[x])["freq"][candidate - 1] += 1
                    (column_table[x])["tracker"][candidate - 1].add(y)

    return column_table


def fill_block_table(board):
    block_table = config.block_table()

    for block, (x, y) in enumerate(config.block_loc_list):

        range_x = (x // 3) * 3
        range_y = (y // 3) * 3

        for elem_x in range(range_y, range_y + 3):
            for elem_y in range(range_x, range_x + 3):
                loc = elem_x, elem_y
                if board[elem_y][elem_x] == 0:
                    candidates = valid_candidates(board, loc)
                    for candidate in candidates:
                        (block_table[block])["freq"][candidate - 1] += 1
                        (block_table[block])["tracker"][candidate - 1].add((elem_x, elem_y))

        return block_table


def fill_blocks(board):
    block_table = fill_block_table(board)

    for block_loc, block in enumerate(block_table):
        for x, freq_record in enumerate(block["freq"]):
            if freq_record == 1:
                config.singles += 1
                block["freq"][x] = 0
                partial_loc = block["tracker"][x].pop()
                loc = (lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1]))(partial_loc, config.block_loc_list[block_loc])
                a, b = loc
                board[b][a] = x + 1
                return loc, x

    return None, None


def fill_rows(board):
    row_table = fill_row_table(board)

    for row_loc, row in enumerate(row_table):
        for x, freq_record in enumerate(row["freq"]):
            if freq_record == 1:
                config.singles += 1
                row["freq"][x] = 0
                loc_x = row["tracker"][x].pop()
                loc_y = row_loc
                loc = loc_x, loc_y
                a, b = loc
                board[b][a] = x + 1
                return loc, x

    return None, None


def fill_columns(board):
    column_table = fill_column_table(board)

    for column_loc, column in enumerate(column_table):
        for x, freq_record in enumerate(column["freq"]):
            if freq_record == 1:
                config.singles += 1
                column["freq"][x] = 0
                loc_y = column["tracker"][x].pop()
                loc_x = column_loc
                loc = loc_x, loc_y
                a, b = loc
                board[b][a] = x + 1
                return loc, x

    return None, None


def update_row_table(loc, candidate):
    y = loc[1]
    row_table = config.row_table()
    (row_table[y])["freq"][candidate] = 0
    (row_table[y])["tracker"][candidate].clear()


def update_column_table(loc, candidate):
    x = loc[0]
    column_table = config.column_table()
    (column_table[x])["freq"][candidate] = 0
    (column_table[x])["tracker"][candidate].clear()
    return column_table


def update_block_table(loc, candidate):
    x, y = loc
    block_x, block_y = (x // 3), (y // 3)
    block_no = config.loc_to_block_number[(block_x, block_y)]

    block_table = config.block_table()
    (block_table[block_no])["freq"][candidate] = 0
    (block_table[block_no])["tracker"][candidate].clear()


def update_tables(loc, candidate):
    update_row_table(loc, candidate)

    update_column_table(loc, candidate)

    update_block_table(loc, candidate)


def fill_singles(board):
    while True:

        start = config.singles
        loc, candidate = fill_blocks(board)
        if candidate is not None:
            update_tables(loc, candidate)

        loc, candidate = fill_rows(board)
        if candidate is not None:
            update_tables(loc, candidate)

        loc, candidate = fill_columns(board)
        if candidate is not None:
            update_tables(loc, candidate)

        end = config.singles
        if end == start:
            break

    return board


def single_solver(board):
    while True:
        start = config.singles
        fill_naked_singles(board)
        fill_singles(board)
        # print_board(board)
        # print(f"singles: {config.singles}")
        end = config.singles
        if start == end:
            break
