'''
    Created on Thu May  9 11:54:42 2019

    @author: BishopRD
'''

import random
import copy
import math
import time
import sys
import collections
import matplotlib.pyplot as plt

import pygame as pg
from myColors import *

# global game_over
# global arr
# global high_scores_board
# global move_count
# global top_score_move_count
# global manual

manual = True
pg.init()
my_font = pg.font.SysFont('Monospace', 25)
my_font.set_bold(True)
header_font = pg.font.SysFont('Monospace', 40)
score_font = pg.font.SysFont('Monospace', 25)
high_score_font = pg.font.SysFont('Monospace', 20)
restart_font = pg.font.SysFont('Monospace', 30)

header = header_font.render('2048', 1, (0, 255, 0))
GAME_BOARD = pg.display.set_mode((400, 500), 0, 32)
pg.display.set_caption('2048')


def main(manual=True):

    new_game()
    print_matrix()
    # manual = False
    if not manual:
        while not check_game_over():
            logic_algorithms()

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if not check_game_over():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        # print('U')
                        up()
                    elif event.key == pg.K_DOWN:
                        # print('D')
                        down()
                    elif event.key == pg.K_LEFT:
                        # print('L')
                        left()
                    elif event.key == pg.K_RIGHT:
                        # print('R')
                        right()
                    print_matrix()
                    time.sleep(0.08)
                    add_new()
                    print_matrix()
            else:
                print_game_over()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        main()


def print_matrix():

    global high_score

    GAME_BOARD.fill((0, 0, 0))
    pg.draw.rect(GAME_BOARD, (0, 50, 0), (155, 25, 110, 23))
    GAME_BOARD.blit(header, ((400/2)-40, 10))

    current_score = score_font.render(str(TOTAL_POINTS), 1, (0, 255, 0))
    GAME_BOARD.blit(current_score, ((200 - len(str(TOTAL_POINTS))*5), 60))

    if TOTAL_POINTS > high_score:
        high_score = TOTAL_POINTS

    high_score_alltime = high_score_font.render(
        str(high_score), 1, (0, 255, 0))
    GAME_BOARD.blit(high_score_alltime, (3, 3))

    tileMatrix2 = [[str(x) if x != 0 else str() for x in row] for row in arr]
    # print(tileMatrix2)
    for i in range(0, 4):
        for j in range(0, 4):
            pg.draw.rect(GAME_BOARD, get_color_tile(
                arr[j][i]), (i*(400/4)+4.5, j*(400/4) + 100, 400/4.3, 400/4.3))

            tile_value = my_font.render(
                str(tileMatrix2[j][i]), 1, get_color_num(arr[j][i]))

            len_value = len(tileMatrix2[j][i])
            GAME_BOARD.blit(tile_value, (i*(400/4) + 40 -
                                         (len_value*5), j*(400/4) + 138))

    pg.display.update()


def print_game_over():

    print_matrix()
    pg.draw.rect(GAME_BOARD, (0, 0, 0), (90, 260, 240, 100))
    game_over_banner = header_font.render('GAME OVER', 1, (0, 255, 0))
    reset_banner = restart_font.render('(r)estart', 1, (0, 255, 0))

    GAME_BOARD.blit(game_over_banner, (100, 265))
    GAME_BOARD.blit(reset_banner, (130, 320))

    if check_high_score():
        high_score_banner = header_font.render('HIGH SCORE!', 1, (0, 0, 0))
        pg.draw.rect(GAME_BOARD, (0, 255, 0), (40, 85, 330, 80))
        GAME_BOARD.blit(high_score_banner, (60, 100))

    pg.display.update()


def update_score(new_num):
    global TOTAL_POINTS
    TOTAL_POINTS += new_num
    return

def move(array):
    """
    Base logic for all directional moves.
    """
    
    for row in array:
        # move zeros to end of row
        for _ in range(row.count(0)):
            row.remove(0)
            row.append(0)

        # combine adjacent tiles that match
        points_to_add = 0

        for index, current_num in enumerate(row):
            if current_num != 0 and index < 3 and current_num == row[index+1]:
                adjacent_num = row[index+1]
                new_num = current_num + adjacent_num
                points_to_add += new_num
                time.sleep(0.01)
                row.pop(index)
                time.sleep(0.01)
                row.insert(index, new_num)
                time.sleep(0.01)
                row.append(0)
                time.sleep(0.01)
                row.pop(index+1)

        update_score(points_to_add)
    return

def check_if_manual():
    if manual:
        print_arr()


def left():
    """Slide tiles LEFT"""

    check_non_move()
    move(arr)
    # add_new()
    # check_if_manual()


def right():
    """Slide tiles RIGHT"""

    check_non_move()
    row_reverse()
    move(arr)
    row_reverse()
    # add_new()
    # check_if_manual()


def up():
    """Slide tiles UP"""

    check_non_move()
    zip_arr()
    move(arr)
    zip_arr()
    # add_new()
    # check_if_manual()


def down():
    """Slide tiles DOWN"""

    check_non_move()
    zip_arr()
    row_reverse()
    move(arr)
    row_reverse()
    zip_arr()
    # add_new()
    # check_if_manual()


def row_reverse():
    for row in arr:
        row.reverse()


def zip_arr():
    """Transform rows to columns"""

    global arr
    arr = list(map(list, zip(*arr)))
    return arr


def check_non_move():
    """If move didn't move any tiles, do nothing."""

    global original_arr
    original_arr = copy.deepcopy(arr)
    return original_arr


def add_new():
    """Add new number to board."""
    global move_count

    if original_arr == arr:
        return False
    else:
        row = random.randint(0, 3)
        new = get_new_number()

        if 0 in arr[row]:
            zeros = [i for i, val in enumerate(arr[row]) if val == 0]
            replace = random.choice(zeros)
            arr[row].pop(replace)
            arr[row].insert(replace, new)
            move_count += 1
            if not manual:
                time.sleep(0.2)
                print_matrix()
                pg.display.update()
            else:
                print_arr()
            check_game_over()
            # return True
        else:
            add_new()


def get_new_number():
    """Create new random number to add to board."""
    new = 2
    if random.randint(0, 10) >= 9:
        new = 4
    return new


def check_game_over():
    """Stop game if no more moves."""
    global game_over

    # available_moves = 0
    if any(0 in row for row in arr):
        return False
    elif any([arr[i][j] == arr[i][j+1] for i in range(0, 4) for j in range(0, 3)]):
        return False
    elif any([arr[i][j] == arr[i+1][j] for i in range(0, 3) for j in range(0, 4)]):
        return False
    else:
        game_over = True
        return True


def check_high_score():

    try:
        load_high_score()
        if TOTAL_POINTS >= high_score:
            save_high_score()
            return True
        else:
            return False
    except FileNotFoundError:
        save_high_score()


def save_high_score():

    with open("2048_meta", "w") as f:
        f.write(str(TOTAL_POINTS))


def load_high_score():

    global high_score

    try:
        with open('2048_meta', 'r') as f:
            high_score = int(f.readline())
    except FileNotFoundError:
        high_score = 0


def track_high_score():
    """
    If high score is surpassed during a game, 
    track in memory to continuously update game board.
    """
    pass

def print_arr():
    """Print game board to command output."""

    # minimalist game board format
    max_width = len(str(max([max(n) for n in arr])))+1
    row_format = ("{:"+str(max_width+1)+"}")*4
    print()
    print('.'+(' '*(max_width-1)+'.')*4)
    for row in arr:
        display_row = [str(x) if x != 0 else str() for x in row]
        print(row_format.format(*display_row))
        print('.'+(' '*(max_width-1)+'.')*4)
    print()

    # fancy pants game board formatting
    # row_format = ("{:^9}")*4
    # print()
    # for row in arr:
    #     display_row = [str(x) if x != 0 else str() for x in row]
    #     print('------'*6+'-')
    #     print('|        '*4+'|')
    #     print(row_format.format(*display_row))
    #     print('|        '*4+'|')
    # print('------'*6+'-')


def reset_arr():
    """Reset game board and populate with 2 random tiles."""
    global arr

    first_val = get_new_number()
    second_val = get_new_number()
    arr = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
    first_coord_x = random.randint(0, 3)
    first_coord_y = random.randint(0, 3)
    second_coord_x = random.randint(0, 3)
    second_coord_y = random.randint(0, 3)

    # make sure new tiles aren't both in same spot
    if not (first_coord_x == second_coord_x and first_coord_y == second_coord_y):
        arr[first_coord_x][first_coord_y] = first_val
        arr[second_coord_x][second_coord_y] = second_val
    else:
        reset_arr()


def new_game():
    global move_count
    global game_over
    global TOTAL_POINTS

    game_over = False
    move_count = 0
    TOTAL_POINTS = 0
    reset_arr()
    print_arr()
    load_high_score()

def test_game(iterations):
    """Runs iterations and reports frequency distribution of high scores."""

    # global game_over
    # global arr
    global high_scores_board
    global move_count
    global top_score_move_count
    global manual

    high_scores_dict = collections.defaultdict(int)
    dict_double = collections.defaultdict(int)
    move_count_dict = collections.defaultdict(int)
    high_scores_board = list()
    manual = False

    for game in range(iterations):

        main(manual=False)

        while not game_over:
            # logic_algorithms()
            shuffle_algorithm()

        high_score = max([max(n) for n in arr])
        high_scores_dict[high_score] += 1
        move_count_dict[move_count] += 1

        # was curious and exploring a hypothesis about 128 and 256
        winning_score = 2048
        if high_score >= winning_score:
            high_scores_board.append(arr)
            count = sum([n.count(winning_score) for n in arr])
            count_half = sum([n.count(winning_score//2) for n in arr])
            if count > 1:
                dict_double['2 top tiles'] += 1
            else:
                dict_double['1 top tile'] += 1
                if count_half >= 1:
                    dict_double['2 sub-tiles unmatched'] += 1
            top_score_move_count = move_count

    sorted_dict = collections.defaultdict(int)
    for key in sorted(high_scores_dict.keys()):
        sorted_dict[key] = high_scores_dict[key]

    plt.bar(list(move_count_dict.keys()), move_count_dict.values(),
            color='b', width=2)
    y_int = range(0, math.ceil(max(move_count_dict.values())+1))
    plt.yticks(y_int)
    plt.xlabel('# of moves')
    plt.ylabel('# of games')

    print(dict(sorted_dict))
    print(dict(dict_double))

    try:
        print("Top Score Move Count:", top_score_move_count)
    except NameError:
        print("No 2048 board.")


def print_turn(turn):
    """If enabled, prints list of turns."""
    enabled = False
    if enabled:
        print(turn)

# testing only
def shuffle_algorithm():
    """Only left, down, left, up."""
    if check_game_over():
        return

    else:
        algorithm = [left, down, left, up]
        check_original_arr = copy.deepcopy(arr)
        for move_choice in algorithm:
            move_choice()
            # if original_arr != arr:
            #     break
        if check_original_arr == arr:
            right()
            down()
            left()


def logic_algorithms():
    """Tuning for best performance."""

    # check first for no moves left/up/down
    # if gridlock() == True:
    #    print_arr()
    #    right()
    if check_game_over():
        return

    else:
        max_val_first_col = max(*[n[0] for n in arr])

        if arr[0][0] != 0 and arr[0][0] == arr[1][1] and arr[1][0] == arr[2][1]:
            up()
            left()
            # logic_algorithms()

        # Ex; [2,2,2,2]
        if check_same_four_one_row():
            print_turn('1a')
            left()
            left()
            logic_algorithms()
        # Ex: [2,0,0,0],[2,0,0,0],[2,0,0,0],[2,0,0,0]
        elif check_same_four_one_col():
            print_turn('1b')
            up()
            up()
            logic_algorithms()

        # slides if 2 rows or columns that could combine tiles
        if check_double_move_horizontal():
            print_turn('2a')
            left()
            logic_algorithms()
        elif check_double_move_vertical():
            print_turn('2b')
            up()
            logic_algorithms()

        # if max cell in top left or bottom left, keep it there
        # TOP LEFT
        if arr[0][0] == max_val_first_col and (any([row[0] == 0 for row in arr])
                                               or any([arr[i][0] == arr[i+1][0] for i in range(1, 3)])):
            top_left_moves = [left, up]
            print_turn('3a')
            check_original_arr = copy.deepcopy(arr)
            for move_choice in top_left_moves:
                move_choice()
                if original_arr != arr:
                    logic_algorithms()
            if check_original_arr == arr:
                down()
                logic_algorithms()

        # BOTTOM LEFT
        elif arr[3][0] == max_val_first_col and (any([row[0] == 0 for row in arr])
                                                 or any([arr[i][0] == arr[i+1][0] for i in range(0, 2)])):
            bottom_left_moves = [left, down]
            print_turn('3b')
            check_original_arr = copy.deepcopy(arr)
            for move_choice in bottom_left_moves:
                move_choice()
                if original_arr != arr:
                    logic_algorithms()
            if check_original_arr == arr:
                up()
                logic_algorithms()

        if arr[1][0] == max_val_first_col and arr[0][0] == 0 and max_val_first_col:
            print_turn('4a')
            up()
            logic_algorithms()

        elif arr[2][0] == max_val_first_col and arr[3][0] == 0 and max_val_first_col:
            print_turn('4b')
            down()
            logic_algorithms()

        elif arr[1][0] == max_val_first_col and arr[2:][0] == 0 and max_val_first_col:
            print_turn('4a')
            down()
            logic_algorithms()

        elif arr[2][0] == max_val_first_col and arr[0:2][0] == 0 and max_val_first_col:
            print_turn('4b')
            down()
            logic_algorithms()

        # regular left shuffle algorithm
        if all([arr[i][0] != arr[i+1][0] for i in range(0, 3)]) and 0 not in [n[0] for n in arr]:
            print_turn('5')
            algorithm = [left, up, left, down]
            check_original_arr = copy.deepcopy(original_arr)
            for move_choice in algorithm:
                move_choice()
                # if original_arr != arr:
                #     break
            if check_original_arr == arr:
                right()
                left()
            logic_algorithms()

        else:
            print_turn('6')
            algorithm = [left, down, left, up]
            check_original_arr = copy.deepcopy(original_arr)
            for move_choice in algorithm:
                move_choice()
                # if original_arr != arr:
                #     break
            if check_original_arr == arr:
                right()
                left()
            logic_algorithms()

# def gridlock():
#    """Check if no left/up/down move. If so, move right."""
#    moves_list = [left, up, down]
#    no_moves = False
#    for move_choice in moves_list:
#        if no_moves:
#            break
#        else:
#            move_choice()
#            if original_arr == arr:
#                no_moves = True
#            else:
#                continue
#    return no_moves


def check_same_four_one_row():
    """Check if one row has same 4 numbers and slide 2 times HORIZONTAL."""
    count = 0
    for row in arr:
        if all([row[0] == row[1] and row[0] != 0,
                row[1] == row[2] and row[1] != 0,
                row[2] == row[3] and row[2] != 0]):
            count += 1
    if count > 1:
        return True
    else:
        return False


def check_same_four_one_col():
    """Check if one column has same 4 numbers and slide 2 times VERTICAL."""
    # transposes rows into columns in array first
    zip_arr()
    vertical_same = check_same_four_one_row()
    zip_arr()
    if vertical_same:
        return True


def check_double_move_horizontal():
    """Check if two sets of combine moves available with one HORIZONTAL slide."""

    count = 0
    for row in arr:
        if any([row[0] == row[1] and row[0] != 0,
                row[1] == row[2] and row[1] != 0,
                row[2] == row[3] and row[2] != 0]):
            count += 1
    if count > 1:
        return True
    else:
        return False


def check_double_move_vertical():
    """Check if two sets of combine moves available with one VERTICAL slide."""
    # transposes rows into colummns in arr first
    zip_arr()
    down_move = check_double_move_horizontal()
    zip_arr()
    if down_move:
        return True


def print_high_scores():
    """Prints game_over board of each game that reached 2048."""

    for board in high_scores_board:
        max_width = len(str(max([max(n) for n in board])))+1
        row_format = ("{:"+str(max_width)+"}")*4
        print()
        for row in board:
            print(row_format.format(*row))


def get_highest_board_score():
    """Prints highest board score/final board from test_game() function."""
    highest_board_score = 0
    highest_board_arr = list()
    if high_scores_board:
        for board in high_scores_board:
            total_sum = sum([sum(rows) for rows in board])
            if total_sum > highest_board_score:
                highest_board_score = total_sum
                highest_board_arr = board
        print()

        print("Highest Scoring Board")
        print("Tile Total:", highest_board_score)
        max_width = len(str(max([max(n) for n in highest_board_arr])))+1
        row_format = ("{:"+str(max_width)+"}")*4
        print("Final Board:")
        for row in highest_board_arr:
            print(row_format.format(*row))
    else:
        print('No winning games')


# test_game(2)
# get_highest_board_score()
# print_high_scores()
main()
