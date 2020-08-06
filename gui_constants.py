import pygame as pg

# window size
WIDTH = 510
HEIGHT = 630

# colours
BLUE = (137, 207, 240)
RED = (255, 105, 97)
BUTTON_GREEN = (0, 120, 0)
BUTTON_BLUE = (0, 0, 128)
BUTTON_RED = (122, 21, 20)
BUTTON_ORANGE = (45, 19, 44)
BUTTON_TURQUOISE = (0, 110, 110)
BUTTON_MAGENTA = (109, 0, 109)

# grid dimensions
GRID_POS = (35, 35)
GRID_WIDTH = WIDTH - 2 * GRID_POS[0]
CELL_WIDTH = int(GRID_WIDTH / 9)

# key-press lookup tables
number_list = [pg.K_BACKSPACE, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]

alphabet_list = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_a, pg.K_b,
                 pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m,
                 pg.K_n, pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t, pg.K_u, pg.K_v, pg.K_w, pg.K_x, pg.K_y, pg.K_z,
                 pg.K_UNDERSCORE, pg.K_PERIOD, pg.K_MINUS, pg.K_BACKSPACE
                 ]

alphabet_value = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k",
                  "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
                  "z", "_", ".", "-", ""]
