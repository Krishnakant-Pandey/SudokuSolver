import copy


def valid_in_row(board, ans, loc):
    x, y = loc
    for elem_x in board[y]:
        if ans == elem_x:
            return False
    return True


def valid_in_column(board, ans, loc):
    x, y = loc
    for j in range(9):
        elem_y = board[j][x]
        if ans == elem_y:
            return False
    return True


def valid_in_box(board, ans, loc):
    x, y = loc
    range_x = (x // 3) * 3
    range_y = (y // 3) * 3

    for elem_x in range(range_y, range_y + 3):
        for elem_y in range(range_x, range_x + 3):
            if board[elem_x][elem_y] == ans:
                return False
    return True


def valid_number(board, ans, loc):
    vr = valid_in_row(board, ans, loc)
    if not vr:
        return False

    vc = valid_in_column(board, ans, loc)
    if not vc:
        return False

    vb = valid_in_box(board, ans, loc)
    if not vb:
        return False

    return vr and vc and vb


def valid_candidates(board, loc):
    candidate = []
    for i in range(10):
        if valid_number(board, i, loc):
            candidate.append(i)
    return candidate


def find_empty(board):
    for i, row in enumerate(board):
        for j, elem in enumerate(row):
            if elem == 0:
                return j, i
    return None


def valid_grid(board):
    temp_board = copy.deepcopy(board)
    grid_validity = True
    for y, row in enumerate(temp_board):
        for x, elem in enumerate(row):
            if board[y][x] != 0:
                temp = elem
                temp_board[y][x] = 0
                valid = valid_number(temp_board, temp, (x, y))
                grid_validity = grid_validity & valid

                temp_board[y][x] = temp
    return grid_validity
