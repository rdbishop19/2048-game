# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:54:42 2019

@author: BishopRD
"""
import random
import collections
import matplotlib.pyplot as plt
import copy
import math
import time

#import pygame as pg
#import sys
#pg.init()

#screen = pg.display.set_mode((400,400))
manual = False

def l():
    left()
def r():
    right()
def u():
    up()
def d():
    down()
    
def move():
    """Base logic for all directional moves."""
    
    for row in arr:
        # move zeros to end of row
        for col, current_num in enumerate(row):
            if current_num == 0:
                row.remove(current_num)
                row.append(current_num)
        # combine adjacent tiles that match
        for col, current_num in enumerate(row):
            if current_num != 0 and col < 3:
                adjacent_num = row[col+1]
                if current_num == adjacent_num:
                    new = current_num + adjacent_num
                    row.remove(current_num)
                    row.pop(col)
                    row.insert(col, new)
                    row.append(0)

def check_if_manual():
    if manual:
        print_arr()
        
def left():
    """Slide tiles LEFT"""
    
    check_non_move()
    move()
    add_new()
    check_if_manual()
    
def right():
    """Slide tiles RIGHT"""

    check_non_move()
    row_reverse()
    move()
    row_reverse()
    add_new()
    check_if_manual()
        
def up():
    """Slide tiles UP"""

    check_non_move()   
    zip_arr()
    move()
    zip_arr()
    add_new()
    check_if_manual()
    
def down():
    """Slide tiles DOWN"""

    check_non_move()    
    zip_arr()
    row_reverse()
    move()
    row_reverse()
    zip_arr()
    add_new()
    check_if_manual()

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
        row = random.randint(0,3)
        new = get_new_number()
        
        if 0 in arr[row]:
            zeros = [i for i, val in enumerate(arr[row]) if val==0]
            replace = random.choice(zeros)
            arr[row].remove(arr[row][replace])
            arr[row].insert(replace, new)
#            print_arr()
#            time.sleep(0.5)
            move_count += 1
            check_game_over()
        else:
            add_new()

def get_new_number():
    """Create new random number to add to board."""
    
    new = 2
    new_prob = random.randrange(0,10)
    if new_prob >= 9:
        new = 4
    return new

def check_game_over():
    """Stop game if no more moves."""
    
    global game_over
    
#    available_moves = 0
    if any(0 in row for row in arr):
        return False
    elif any([arr[i][j] == arr[i][j+1] for i in range(0,3) for j in range(0,3)]):
        return False
    elif any([arr[i][j] == arr[i+1][j] for i in range(0,3) for j in range(0,3)]):
        return False
    else:
        game_over = True
        return True
#        # row check
#        available_moves += find_available_moves()
#        # column check
#        zip_arr()
#        available_moves += find_available_moves()
#        # reset
#        zip_arr()
#    if not available_moves:
#        game_over = True

#def find_available_moves():
#    """Checks for adjacent tiles with same value on board."""
#    
#    count = 0
#    for row in arr:
#        for col, current_num in enumerate(row):
#            if col < 3:
#                adjacent_num = row[col+1]
#                if current_num == adjacent_num:
#                    count += 1
#    return count
    
def print_arr():
    """Print game board."""
    
    max_width = len(str(max([max(n) for n in arr])))+1
    row_format = ("{:"+str(max_width)+"}")*4
    print()
    for row in arr:
        print(row_format.format(*row))
        print()

def reset_arr():
    """Reset game board and populate with 2 random tiles."""
    global arr
    
    first_val = get_new_number()
    second_val = get_new_number()
    arr = [[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0]]
    first_coord_x = random.randint(0,3)
    first_coord_y = random.randint(0,3)
    second_coord_x = random.randint(0,3)
    second_coord_y = random.randint(0,3)
    
    # make sure new tiles aren't both in same spot
    if not (first_coord_x == second_coord_x and first_coord_y == second_coord_y):
        arr[first_coord_x][first_coord_y] = first_val
        arr[second_coord_x][second_coord_y] = second_val
    else:
        reset_arr()

def new_game():
    reset_arr()
    print_arr()
    
def test_game(iterations):
    """Runs iterations and reports frequency distribution of high scores."""
    
    global game_over
    global arr
    global high_scores_board
    global move_count
    global top_score_move_count
    
    high_scores_dict = collections.defaultdict(int)
    dict_double = collections.defaultdict(int)
    move_count_dict = collections.defaultdict(int)
    high_scores_board = list()
    
    for game in enumerate(range(iterations)):
        reset_arr()
        game_over = False
        move_count = 0
        
        while not game_over:
            logic_algorithms()

        high_score = max([max(n) for n in arr])
        high_scores_dict[high_score] += 1
        move_count_dict[move_count] += 1
#        
#        ## was curious and exploring a hypothesis about 128 and 256
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
#                
    sorted_dict = collections.defaultdict(int)
    for key in sorted(high_scores_dict.keys()):
        sorted_dict[key] = high_scores_dict[key]
#    plt.bar(range(len(high_scores_dict)), list(sorted_dict.values()), align='center')
#    plt.xticks(range(len(high_scores_dict)), list(sorted_dict.keys()))
#    plt.show()
    
    plt.bar(list(move_count_dict.keys()), move_count_dict.values(), 
                color='b', width=2)
    y_int = range(0, math.ceil(max(move_count_dict.values())+1))
    plt.yticks(y_int)
    plt.xlabel('# of moves')
    plt.ylabel('# of games')

    print(sorted_dict)
    print(dict_double)
    try:
        print("Top Score Move Count:",top_score_move_count)
    except NameError:
        print("No 2048 board.")

def print_turn(turn):
    """If enabled, prints list of turns."""
    enabled = False
    if enabled:
        print(turn)
        
def logic_algorithms():
    """Tuning for best performance."""
    
    # check first for no moves left/up/down
#    if gridlock() == True:
#        print_arr()
#        right()
    if check_game_over():
        return
    
    else:
        max_val_first_col = max(*[n[0] for n in arr])      
        if arr[1][0] == max_val_first_col and arr[0][0] == 0 and max_val_first_col:
            print_turn('4a')
            up()
            logic_algorithms()
            
        elif arr[2][0] == max_val_first_col and arr[3][0] == 0 and max_val_first_col:
            print_turn('4b')
            down()
            logic_algorithms()
            
        if arr[0][0] != 0 and arr[0][0] == arr[1][1] and arr[1][0] == arr[2][1]:
            up()
            left()
#            logic_algorithms()
        
        # Ex; [2,2,2,2]
        if check_same_four_one_row():
            print_turn('1a')
            left()
            left()
            logic_algorithms()
        # Ex: [2,0,0,0],[2,0,0,0],[2,0,0,0],[2,0,0,0]
        elif check_same_four_one_col():
            print_turn('1b')
            down()
            down()
            logic_algorithms()
    
        # slides if 2 rows or columns that could combine tiles
        if check_double_move_horizontal():
            print_turn('2a')
            left()
            logic_algorithms()
        elif check_double_move_vertical():
            print_turn('2b')
            down()
            logic_algorithms()
         
        # if max cell in top left or bottom left, keep it there
        ## TOP LEFT  
        if arr[0][0] == max_val_first_col and (any([row[0] == 0 for row in arr])
        or any([arr[i][0] == arr[i+1][0] for i in range(1,3)])):
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
        ## BOTTOM LEFT
        elif arr[3][0] == max_val_first_col and (any([row[0] == 0 for row in arr])
        or any([arr[i][0] == arr[i+1][0] for i in range(0,2)])):
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
    
        # regular left shuffle algorithm
        if all([arr[i][0] != arr[i+1][0] for i in range(0,3)]) and 0 not in [n[0] for n in arr]:
            print_turn('5')
            algorithm = [left, down, left, up]
            check_original_arr = copy.deepcopy(original_arr)
            for move_choice in algorithm:
                move_choice()
#                if original_arr != arr:
#                    break
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
#                if original_arr != arr:
#                    break
            if check_original_arr == arr:
                right()
                left()
            logic_algorithms()
        
#def gridlock():
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
        print("Tile Total:",highest_board_score)
        max_width = len(str(max([max(n) for n in highest_board_arr])))+1
        row_format = ("{:"+str(max_width)+"}")*4
        print("Final Board:")
        for row in highest_board_arr:
            print(row_format.format(*row))
    else:
        print('No winning games')      
        
test_game(1000)
get_highest_board_score()

#print_high_scores()


