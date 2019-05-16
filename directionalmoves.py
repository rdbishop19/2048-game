# move logic for 2048 board
import copy, random, time
global arr

def move():
    """Base logic for all directional moves."""
    global TOTAL_POINTS
    global arr  

    for row in arr:
        # move zeros to end of row
        for col, current_num in enumerate(row):
            if current_num == 0:
                row.remove(current_num)
                row.append(0)
        # combine adjacent tiles that match
        for col, current_num in enumerate(row):
            if current_num != 0 and col < 3:
                adjacent_num = row[col+1]
                if current_num == adjacent_num:
                    new = current_num + adjacent_num
                    TOTAL_POINTS += new
                    time.sleep(0.01)
                    row.pop(col)
                    time.sleep(0.01)
                    row.insert(col, new)
                    time.sleep(0.01)
                    row.append(0)
                    time.sleep(0.01)
                    row.pop(col+1)
                    print(row)

        
def left():
    """Slide tiles LEFT"""
    global arr

    # check_non_move()
    move()
    add_new()
    # check_if_manual()
    
def right():
    """Slide tiles RIGHT"""

    # check_non_move()
    row_reverse()
    move()
    row_reverse()
    add_new()
    # check_if_manual()
        
def up():
    """Slide tiles UP"""

    # check_non_move()   
    zip_arr()
    move()
    zip_arr()
    add_new()
    # check_if_manual()
    
def down():
    """Slide tiles DOWN"""

    # check_non_move()    
    zip_arr()
    row_reverse()
    move()
    row_reverse()
    zip_arr()
    add_new()
    # check_if_manual()

def row_reverse():
    global arr

    for row in arr:
        row.reverse()   
        
def zip_arr():
    """Transform rows to columns"""
    
    global arr
    arr = list(map(list, zip(*arr)))
    return arr

    
def add_new():
    """Add new number to board."""
    global move_count

    if not original_arr == arr:
        row = random.randint(0,3)
        new = get_new_number()
        
        if 0 in arr[row]:
            zeros = [i for i, val in enumerate(arr[row]) if val==0]
            replace = random.choice(zeros)
            arr[row].remove(arr[row][replace])
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