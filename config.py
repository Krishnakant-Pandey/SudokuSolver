backtracks = 0
block_loc_list = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

loc_to_block_number = {(0, 0): 0, (1, 0): 1, (2, 0): 2, (0, 1): 3, (1, 1): 4, (2, 1): 5, (0, 2): 6, (1, 2): 7,
                       (2, 2): 8}

singles = 0


def row_table():
    def row_freq():
        row_frequency = {"freq": [0] * 9, "tracker": [set() for track in range(9)]}
        return row_frequency

    row_tracker = []
    for y in range(9):
        row_frequency = row_freq()
        row_frequency["row"] = y
        row_tracker.append(row_frequency)
    return row_tracker


def column_table():
    def column_freq():
        column_frequency = {"freq": [0] * 9, "tracker": [set() for track in range(9)]}
        return column_frequency

    column_tracker = []
    for y in range(9):
        column_frequency = column_freq()
        column_frequency[" column"] = y
        column_tracker.append(column_frequency)
    return column_tracker


def block_table():
    def block_freq():
        block_frequency = {"freq": [0] * 9, "tracker": [set() for track in range(9)]}
        return block_frequency

    block_tracker = []
    for y in range(9):
        block_frequency = block_freq()
        block_frequency["block"] = y
        block_tracker.append(block_frequency)
    return block_tracker
