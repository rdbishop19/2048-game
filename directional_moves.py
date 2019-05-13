# -*- coding: utf-8 -*-
"""
Created on Sun May 12 13:20:01 2019

@author: BishopRD
"""
global arr

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
            if current_num != 0:
                if col < 3:
                    adjacent_num = row[col+1]
                    if current_num == adjacent_num:
                        new = current_num + adjacent_num
                        row.remove(current_num)
                        row.pop(col)
                        row.insert(col, new)
                        row.append(0)

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
#    print('r')
    add_new()
    check_if_manual()
    
def row_reverse():
    for row in arr:
        row.reverse()
        
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
    
def zip_arr():
    """Transform rows to columns"""
    
    global arr
    arr = list(map(list, zip(*arr)))
    return arr
