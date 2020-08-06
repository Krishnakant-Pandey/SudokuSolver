import pygame as pg
import sys
from gui_constants import *
import math
from interface_button import *
import copy
from solvers import solve, single_solver
import pickle
import random
from image_recognizer import recognize_image
from validatiors import valid_grid

with open("Easy_Games", "rb") as easy:
    easy_games = pickle.load(easy)

with open("Medium_Games", "rb") as medium:
    medium_games = pickle.load(medium)

with open("Hard_Games", "rb") as hard:
    hard_games = pickle.load(hard)

game_list = [easy_games, medium_games, hard_games]


class App:
    def __init__(self):
        pg.init()
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.caption = pg.display.set_caption("Sudoku")
        self.running = True

        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.time_elapsed = 0

        self.empty_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.original_grid = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        self.grid = copy.deepcopy(self.original_grid)
        self.grid_solution = [
            [7, 8, 5, 4, 3, 9, 1, 2, 6],
            [6, 1, 2, 8, 7, 5, 3, 4, 9],
            [4, 9, 3, 6, 2, 1, 5, 7, 8],
            [8, 5, 7, 9, 4, 3, 2, 6, 1],
            [2, 6, 1, 7, 5, 8, 9, 3, 4],
            [9, 3, 4, 1, 6, 2, 7, 8, 5],
            [5, 7, 8, 3, 9, 4, 6, 1, 2],
            [1, 2, 6, 5, 8, 7, 4, 9, 3],
            [3, 4, 9, 2, 1, 6, 8, 5, 7]
        ]

        self.wrong_list = set()
        self.buttons = []

        self.state = "playing"
        self.new_mode = False

        self.selected = None
        self.mouse_pos = None

        self.wrong_option = True
        self.timer_running = True
        self.finished = False
        self.address_input = False

        self.font = pg.font.Font("Arial.ttf", int(5 * CELL_WIDTH / 8))
        self.address_font = pg.font.Font("Arial.ttf", 23)

        self.image_name = ""
        self.message = "Running"
        self.difficulty = 0
        self.allow_save = False
        self.allow_load = False

    def run(self):
        while self.running:
            if self.state == "playing":
                self.events()
                self.draw()
                self.update()
                self.load_buttons()
                if (math.floor(self.time_elapsed / 1000) % 4) == 0:
                    self.message = "Running"
                self.clock.tick(60)  # Frame rate

        pg.quit()
        sys.exit()

    # ---------- State Functions -----------#

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for index, button in enumerate(self.buttons):
                        if index == 6:
                            self.allow_save = True
                        elif index == 7:
                            self.allow_load = True
                        else:
                            self.allow_save = False
                            self.allow_load = False

                        if button.clicked:
                            button.output()

            if event.type == pg.MOUSEBUTTONUP:
                location = self.mouse_on_grid()
                if not location:
                    self.allow_save = False
                    self.allow_load = False

            if event.type == pg.KEYDOWN:
                if event.key in number_list:
                    val = number_list.index(event.key)
                    loc = self.selected  # using loc as an alias to avoid clutter

                    if loc is not None:
                        if len(self.wrong_list) == 0:
                            self.wrong_option = False

                        if self.original_grid[loc[1]][loc[0]] == 0:
                            if val == 0:
                                self.grid[loc[1]][loc[0]] = val

                                if loc in self.wrong_list:
                                    self.wrong_list.discard(loc)

                            elif val != self.grid_solution[loc[1]][loc[0]]:
                                self.wrong_list.add(loc)

                                self.grid[loc[1]][loc[0]] = val
                                self.wrong_option = True

                            else:
                                if loc in self.wrong_list:
                                    self.wrong_list.remove(loc)

                                self.grid[loc[1]][loc[0]] = val

                if event.key in alphabet_list and self.address_input:
                    if event.key == pg.K_BACKSPACE:
                        self.image_name = self.image_name[0:-1]
                    else:
                        index = alphabet_list.index(event.key)
                        val = alphabet_value[index]
                        self.img_name(val)

                if event.key == pg.K_RETURN:

                    if self.address_input:
                        self.image_to_text()

    def update(self):
        self.mouse_pos = pg.mouse.get_pos()

        for button in self.buttons:
            button.update(self.mouse_pos)

        if self.timer_running:
            self.time_elapsed = pg.time.get_ticks() - self.start_time

    def draw(self):
        self.window.fill(self.WHITE)
        if self.selected:
            if self.grid[self.selected[1]][self.selected[0]] == 0:
                self.make_cell_blue(self.selected)

        if self.wrong_option and not self.new_mode:
            self.make_cell_red(self.wrong_list)

        for button in self.buttons:
            button.draw(self.window)

        self.draw_number()

        self.wait_message_to_screen(self.message, (GRID_POS[0] + 160, GRID_POS[0] + GRID_WIDTH + 53))

        self.draw_grid(self.window)

        self.draw_timer(math.floor(self.time_elapsed / 1000))

        self.address_to_screen(self.image_name, (GRID_POS[0], 575))

        pg.display.update()

    # ----------- Button Functions ------------#

    def print_solution(self):
        if not self.new_mode:
            self.wrong_list.clear()
            self.grid = self.grid_solution
        else:
            single_solver(self.grid)
            solve(self.grid)
        self.timer_running = False

    def make_empty(self):
        self.wrong_list.clear()
        self.time_elapsed = 0
        self.timer_running = False
        self.new_mode = True
        self.grid = copy.deepcopy(self.empty_grid)
        self.grid_solution = copy.deepcopy(self.empty_grid)
        self.original_grid = copy.deepcopy(self.empty_grid)

    def load_game(self, difficulty):
        self.difficulty = difficulty
        self.wrong_list.clear()
        self.time_elapsed = 0
        self.timer_running = True
        self.new_mode = False

        choice = random.randint(0, len(game_list[difficulty]) - 1)

        self.grid = copy.deepcopy(((game_list[difficulty])[choice])[1])
        self.grid_solution = copy.deepcopy(((game_list[difficulty])[choice])[0])
        self.original_grid = copy.deepcopy(((game_list[difficulty])[choice])[1])

    def img_name(self, char):  # image has to be in the same directory

        self.image_name = self.image_name + str(char)

    def image_to_text(self):

        try:
            with open(self.image_name, "r") as f:
                pass
            valid_file = True
            self.message = f"Processing"
            self.draw()
            self.timer_running = False

        except FileNotFoundError:
            valid_file = False
            self.message = "Not found"
            self.image_name = ""
            self.draw()

        if valid_file:
            recognized_grid = recognize_image(self.image_name)

            self.image_name = ""
            self.message = "Recognized"

            self.wrong_list.clear()
            self.time_elapsed = 0
            self.new_mode = True

            self.grid = copy.deepcopy(recognized_grid)
            self.grid_solution = copy.deepcopy(recognized_grid)
            self.original_grid = copy.deepcopy(recognized_grid)
            self.timer_running = True

    def change_theme(self):
        self.BLACK, self.WHITE = self.WHITE, self.BLACK

    def save_game(self):
        if self.allow_save:
            print("save")

            with open("saved_games", "rb") as games:
                saved_games = pickle.load(games)

            valid = valid_grid(self.grid)

            if valid:
                self.message = "Saving"
                self.draw()
                saved_games.append(copy.deepcopy(self.grid))

                with open("saved_games", "wb") as games:
                    pickle.dump(saved_games, games)

                self.message = "Saved"
            else:
                self.message = "Invalid save"

            self.allow_save = False

    def load_last_game(self):
        if self.allow_load:
            self.message = "loading"
            self.draw()

            with open("saved_games", "rb") as games:
                saved_games = pickle.load(games)

            if len(saved_games):
                self.grid = copy.deepcopy(saved_games[-1])
                self.original_grid = copy.deepcopy(saved_games[-1])
                self.grid_solution = copy.deepcopy(self.grid)

                single_solver(self.grid_solution)
                solve(self.grid_solution)

                self.message = "Loaded"
            else:
                self.message = "No saves"

            self.allow_load = False

    # ----------- Helper Functions ------------#

    def draw_number(self):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = (xidx * CELL_WIDTH + GRID_POS[0] + 17, yidx * CELL_WIDTH + GRID_POS[1] + 9)
                    self.text_to_screen(str(num), pos)

    def make_cell_blue(self, loc):
        block_x, block_y = loc
        block_loc = (GRID_POS[0] + block_x * CELL_WIDTH, GRID_POS[1] + block_y * CELL_WIDTH)
        pg.draw.rect(self.window, BLUE, (block_loc[0], block_loc[1], CELL_WIDTH, CELL_WIDTH))

    def make_cell_red(self, loc_list):
        for loc in loc_list:
            block_x, block_y = loc
            block_loc = GRID_POS[0] + block_x * CELL_WIDTH, GRID_POS[1] + block_y * CELL_WIDTH
            pg.draw.rect(self.window, RED, (block_loc[0], block_loc[1], CELL_WIDTH, CELL_WIDTH))

    def draw_grid(self, window):
        pg.draw.rect(window, self.BLACK, (GRID_POS[0], GRID_POS[1], GRID_WIDTH - 6, GRID_WIDTH - 6), 2)
        pg.draw.rect(window, self.BLACK, (GRID_POS[0], 575, 306, 30), 3)
        pg.draw.rect(window, self.BLACK, (GRID_POS[0] + 155, GRID_POS[0] + GRID_WIDTH + 53, 150, 37), 3)

        for x in range(1, 9):
            if x % 3 == 0:
                border = 2
            else:
                border = 1

            start = (GRID_POS[0] + x * CELL_WIDTH, GRID_POS[1])
            end = (GRID_POS[0] + x * CELL_WIDTH, GRID_POS[1] + GRID_WIDTH - 6)
            pg.draw.line(window, self.BLACK, start, end, border)

        for y in range(1, 9):
            if y % 3 == 0:
                border = 2
            else:
                border = 1

            start = (GRID_POS[0], GRID_POS[1] + y * CELL_WIDTH)
            end = (GRID_POS[0] + GRID_WIDTH - 6, GRID_POS[1] + y * CELL_WIDTH)
            pg.draw.line(window, self.BLACK, start, end, border)

    def mouse_on_grid(self):
        top_left = GRID_POS[0]
        bottom_right = GRID_POS[0] + GRID_WIDTH - 8
        self.address_input = False

        if self.mouse_pos[0] in range(top_left, bottom_right) and self.mouse_pos[1] in range(top_left, bottom_right):
            block = (np.subtract(self.mouse_pos, GRID_POS) / CELL_WIDTH)
            ans = math.floor(block[0]), math.floor(block[1])
            return ans

        elif self.mouse_pos[0] in range(GRID_POS[0] + 305) and self.mouse_pos[1] in range(572, 575 + 30 + 3):
            self.address_input = True

        else:
            return False

    def load_buttons(self):

        top_left = GRID_POS[0]
        bottom_right = GRID_POS[0] + GRID_WIDTH
        x1 = top_left
        y1 = bottom_right + 50
        x2 = top_left + 105
        level_button_width = 90
        x3 = bottom_right - level_button_width

        self.buttons.append(Button(x3 - 18, y1 - 35, 103, 52, (x3 - 4, y1 - 28), text="Solve",
                                   function=self.print_solution, color=BUTTON_GREEN, font_size=30))

        self.buttons.append(Button(x3 - 18, y1 + 28, 103, 52, (x3 - 4, y1 + 35), text="Setup",
                                   function=self.make_empty, color=BUTTON_BLUE, font_size=30))

        self.buttons.append(Button(x1, y1 - 35, level_button_width, 30, (x1 + 13, y1 - 35), text="Easy",
                                   function=self.load_game, color=BUTTON_RED, font_size=25, params=0))
        self.buttons.append(Button(x2 - 5, y1 - 35, level_button_width + 15, 30, (x2 + 5, y1 - 35), text="Medium",
                                   function=self.load_game, color=BUTTON_RED, font_size=25, params=1))
        self.buttons.append(Button(x2 + 110, y1 - 35, level_button_width, 30, (x2 + 123, y1 - 35), text="Hard",
                                   function=self.load_game, color=BUTTON_RED, font_size=25, params=2))

        self.buttons.append(Button(x1, 0, 97, 30, (x1 + 6, 0), text="Theme",
                                   function=self.change_theme, color=BUTTON_TURQUOISE, font_size=25))

        self.buttons.append(Button(x1, y1 + 1, 72, 40, (x1 + 7, y1 + 4), text="Save",
                                   function=self.save_game, color=BUTTON_MAGENTA, font_size=25))

        self.buttons.append(Button(x1 + 78, y1 + 1, 72, 40, (x1 + 84, y1 + 4), text="Load",
                                   function=self.load_last_game, color=BUTTON_MAGENTA, font_size=25))

    def text_to_screen(self, text, pos):
        font = self.font.render(text, False, self.BLACK)
        self.window.blit(font, pos)

    def address_to_screen(self, text, pos):
        font = self.address_font.render(text, False, self.BLACK)
        self.window.blit(font, (pos[0] + 10, pos[1] + 2))

    def draw_timer(self, total_seconds):
        minutes = total_seconds // 60

        seconds = format(math.floor(total_seconds - (minutes * 60)), "02")
        minutes = format(minutes, "02")

        self.text_to_screen(f"{str(minutes)}:{str(seconds)}", (400, -4))

    def wait_message_to_screen(self, text, pos):
        message_font = pg.font.Font("Roboto-MediumItalic.ttf", 28)
        font = message_font.render(text, False, BUTTON_GREEN)
        self.window.blit(font, pos)
