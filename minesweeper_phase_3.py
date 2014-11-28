from graphics import *
import random

TILE_IMAGE = 'tile.gif'
FLAG_IMAGE = 'flag.gif'
MINE_IMAGE = 'mine.gif'
LOSE_IMAGE = 'lose.gif'
SMILEY_IMAGE = 'smiley.gif'
BLANK_CELL = 0
EXPOSED_CELL = 10
MINE_CELL = 13
MAX_ADJACENT_MINES = 8
WIDTH_OF_IMAGES = 32
HEIGHT_OF_IMAGES = 32
LEFT_OFFSET = 100
RIGHT_OFFSET = 100
TOP_OFFSET = 120
BOTTOM_OFFSET = LEFT_OFFSET // 2
X_OFFSET = LEFT_OFFSET
Y_OFFSET = TOP_OFFSET

unflipped_no_neighbor = 0
FLIPPED_SQUARE_ID = 10
mine_id = 13


def get_difficulty():
    '''
    Prompts the user for a level of difficulty
    (beginner, intermediate, or expert).
    The function will continue to ask until a valid difficulty has
    been inputted.
    Returns the difficulty level
    '''
    difficulty = None
    while difficulty == None:
        user_input = input('Enter a level of difficulty (beginner, intermediate, or expert): ')
        if user_input == 'beginner' or user_input == 'intermediate' or\
           user_input == 'expert':
            difficulty = user_input
        else:
            print('That is not a valid level of difficulty.')
    return difficulty


def get_difficulty_variables(difficulty):
    '''
    Uses the difficulty to determine the number of rows and columns
    that will be used in the game.
    Beginner is 9 rows, 9 columns, 10 mines
    Intermediate is 16 rows, 16 columns, 40 mines
    Expert is 16 rows, 30 columns, 99 mines
    Returns a list in the form of:
    [number of rows, number of columns, number of mines]
    '''
    if difficulty == 'beginner':
        rows = 9
        columns = 9
        mines = 10
    elif difficulty == 'intermediate':
        rows = 16
        columns = 16
        mines = 40
    elif difficulty == 'expert':
        rows = 16
        columns = 30
        mines = 99
    return [rows, columns, mines]


def create_minesweeper_matrix(rows, columns):
    '''
    Uses rows and columns to create a simple 2D list that
    is populated with 0s.
    Returns the created matrix.
    '''
    matrix = []
    for row in range(rows):
        matrix.append([])
        for column in range(columns):
            matrix[row].append(0)
    return matrix


def print_board_game(game_board_marker):
    '''
    Prints the 2D list that represents the value of each square
    on the game board.
    0s represent no mines being around that tile
    1-8 represent the number of mines adjacent to that tile
    10 represents a flipped tile that has no mines that are adjacent
    13 represents a mine
    '''
    for row in range(len(game_board_marker)):
        for column in range(len(game_board_marker[row])):
            print(str(game_board_marker[row][column]).rjust(3), end='')
        print()


def is_in_list(value, list_to_check):
    '''
    Checks to see if a value is in a normal list.
    Returns True if it is, otherwise it returns False.
    '''
    for i in range(len(list_to_check)):
        if value == list_to_check[i]:
            return True
    return False


def get_new_random_tile_coordinates(rows, columns, filled_tiles):
    '''
    Based on rows and columns, the function will create a coordinate
    pair in the form of [row, column] that is not currently in
    filled_tiles and returns it. filled_tiles should be a list of
    coordinates in the form of [[row, column], [row, column]].
    '''
    while True:
        row_id = random.randint(0,rows)
        column_id = random.randint(0,columns)
        if is_in_list([row_id, column_id], filled_tiles) == False:
            return [row_id, column_id]


def populate_with_mines(game_board_markers, number_of_mines, rows, columns):
    '''
    Adds mines (represented by 13s) to game_board_markers and returns
    game_board_markers when all the mines have been added.
    Mines will not be put on top of each other.
    '''
    mine_locations = []
    for i in range(number_of_mines):
        new_mine_location = get_new_random_tile_coordinates(rows-1, columns-1,
                                                            mine_locations)
        row_id = new_mine_location[0]
        column_id = new_mine_location[1]
        game_board_markers[row_id][column_id] = mine_id
        mine_locations.append(new_mine_location)
    return game_board_markers

def is_mine(value):
    '''
    Checks to see if two values are equal.
    Returns 1 if they are and 0 if they are not.
    '''
    if value == mine_id:
        return 1
    else:
        return 0

def find_neighbor_count(game_board_markers, row, column):
    '''
    Checks to see how many mines are around a certain cell in a matrix,
    and returns that number. Mines can be diagonal, horizontal,
    or vertical.
    Works by seeing if cells relative to the selected cell exist,
    and then checks to see if they contain a mine.
    Returns the number of mines relative to the cell.
    '''
    neighbor_count = 0
    surrounding_coords = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1],
                          [1,0],[1,1]]
    for i in range(len(surrounding_coords)):
        row_change = surrounding_coords[i][0]
        column_change = surrounding_coords[i][1]
        if 0 <= row + row_change <= len(game_board_markers) - 1 and\
           0 <= column + column_change <= len(game_board_markers[row]) - 1:
            neighbor_count += is_mine(game_board_markers[row + row_change][column + column_change])
    return neighbor_count


def add_mine_counts(game_board_markers):
    '''
    This function loops through every cell in the matrix to see
    how many mines are next to it, with the help of
    find_neighbor_count. Each cell is then updated to display
    the number of adjacent mines.
    Returns an updated version of game_board_markers.
    '''
    for row in range(len(game_board_markers)):
        for column in range(len(game_board_markers[row])):
            if game_board_markers[row][column] != mine_id:
                neighbor_mine_count = find_neighbor_count(game_board_markers, row, column)
                game_board_markers[row][column] = neighbor_mine_count
    return game_board_markers


def draw_the_grid(rows, columns, window):
    '''
    Draws a grid in the window that will be used for the game.
    Does not return anything.
    '''
    grid_cells = []
    for row_number in range(rows):
        grid_cells.append([])
        for column_number in range(columns):
            top_left = Point(LEFT_OFFSET + WIDTH_OF_IMAGES*column_number,
                             TOP_OFFSET + HEIGHT_OF_IMAGES*row_number)
            bottom_right = Point(LEFT_OFFSET + WIDTH_OF_IMAGES*column_number +\
                                 WIDTH_OF_IMAGES,
                                 TOP_OFFSET + HEIGHT_OF_IMAGES*row_number +
                                 HEIGHT_OF_IMAGES)
            cell = Rectangle(top_left, bottom_right)
            cell.draw(window)
            grid_cells[row_number].append(cell)
    return grid_cells

    

def draw_board_numbers(game_board_markers, window):
    '''
    Draws the numbers into the cells.
    If the number represents a mine, then a mine is drawn instead.
    0s are not represented by blank cells.
    '''
    for row in range(len(game_board_markers)):
        for column in range(len(game_board_markers[row])):
            location_x = LEFT_OFFSET + WIDTH_OF_IMAGES*column + WIDTH_OF_IMAGES//2
            location_y = TOP_OFFSET + HEIGHT_OF_IMAGES*row + HEIGHT_OF_IMAGES//2

            if game_board_markers[row][column] == mine_id:
                mine = Image(Point(location_x, location_y), 'mine.gif')
                mine.draw(window)
            elif game_board_markers[row][column] == 0:
                pass
            elif game_board_markers[row][column] != mine_id:
                num = Text(Point(location_x, location_y), game_board_markers[row][column])
                num.draw(window)


def draw_tiles(game_board_markers, window):
    '''
    Draws blank tiles over the numbers and mines.
    Returns tiles, which is a list of each of the tile objects.
    '''
    tiles = []
    for row in range(len(game_board_markers)):
        tiles.append([])
        for column in range(len(game_board_markers[row])):
            location_x = LEFT_OFFSET + WIDTH_OF_IMAGES*column + WIDTH_OF_IMAGES//2
            location_y = TOP_OFFSET + HEIGHT_OF_IMAGES*row + HEIGHT_OF_IMAGES//2
            tile = Image(Point(location_x, location_y), 'tile.gif')
            tile.draw(window)
            tiles[row].append(tile)
    return tiles


def get_square_clicked(game_board_markers, click_point):
    '''
    Gets the coordinates of a tile that is clicked.
    For example, clicking the top left tile would return 0,0
    If no tile is clicked, it will return None.
    '''
    row = (click_point.getY() - TOP_OFFSET) // HEIGHT_OF_IMAGES
    column = (click_point.getX() - LEFT_OFFSET) // WIDTH_OF_IMAGES
    if 0 <= row <= len(game_board_markers) -1 and\
       0 <= column <= len(game_board_markers[0]) -1:
        return row, column
    else:
        return None


def was_new_cell_clicked(game_board_markers, click_point):
    '''
    Returns True if a new cell was clicked.
    Otherwise, returns False if the click was out of the grid or
    if the cell has already been clicked.
    '''
    row = (click_point.getY() - TOP_OFFSET) // HEIGHT_OF_IMAGES
    column = (click_point.getX() - LEFT_OFFSET) // WIDTH_OF_IMAGES
    if 0 <= row <= len(game_board_markers) -1 and\
       0 <= column <= len(game_board_markers[0]) -1:
        if game_board_markers[row][column] != EXPOSED_CELL:
            return True
    return False
    

def flip_tile(game_board_markers, click_point, tiles, row, column):
    '''
    Takes a mouse click and tries to flip over the tile that was clicked.
    Does not do anything if the mouse was not clicked on a tile, or
    if the tile was already flipped.
    '''
    tiles[row][column].undraw()
    #game_board_markers[row][column] = FLIPPED_SQUARE_ID


def flip_mines(game_board_markers, tiles):
    '''
    Undraws the tiles over every mine on the board.
    '''
    for row in range(len(game_board_markers)):
        for column in range(len(game_board_markers[row])):
            if game_board_markers[row][column] == MINE_CELL:
                tiles[row][column].undraw()


def uncover_adjacent_blank_cells(game_board_markers, tiles, row, column):
    '''
    Flips all of the blank cells that are adjacent to a specific cell.
    Returns the number of adjacent cells flipped.
    '''
    surrounding_coords = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1],
                          [1,0],[1,1]]
    flipped_cells = 0
    for i in range(len(surrounding_coords)):
        row_change = surrounding_coords[i][0]
        column_change = surrounding_coords[i][1]
        if 0 <= row + row_change <= len(game_board_markers) - 1 and\
           0 <= column + column_change <= len(game_board_markers[row]) - 1:
            if game_board_markers[row + row_change][column + column_change] == BLANK_CELL:
                tiles[row + row_change][column + column_change].undraw()
                game_board_markers[row + row_change][column + column_change] = EXPOSED_CELL
                flipped_cells += 1
    return flipped_cells

def handle_click(game_board_markers, click_point, tiles):
    '''
    Flips a tile if one is clicked.
    If the tile is a mine, it will uncover all other mines and the game will end.
    If the tile is a number cell, it will uncover the only that cell.
    If the tile is a blank cell, it will uncover that cell and any
    adjacent blank cells.
    Returns True if a mine was clicked, otherwise the number of cells flipped is returned.
    Note: 0 <= the number of cells flipped <= 9
    '''
    flipped_cells = 0
    if get_square_clicked(game_board_markers, click_point) != None:
        row, column = get_square_clicked(game_board_markers, click_point)
        flip_tile(game_board_markers, click_point, tiles, row, column)
        clicked_cell_id = game_board_markers[row][column]
        if clicked_cell_id == MINE_CELL:
            flip_mines(game_board_markers, tiles)
            return 'mine'
        elif clicked_cell_id == BLANK_CELL:
            flipped_cells = 1
            flipped_cells += uncover_adjacent_blank_cells(game_board_markers, tiles, row, column)
            game_board_markers[row][column] = EXPOSED_CELL
        elif 1 <= clicked_cell_id <= 8:
            flipped_cells = 1
        return flipped_cells
    
        


def draw_column_headers(game_board_markers, window):
    '''
    Draws the numbers at the top of each column.
    '''
    location_y = TOP_OFFSET - HEIGHT_OF_IMAGES/2
    for column in range(len(game_board_markers[0])):
        location_x = LEFT_OFFSET + WIDTH_OF_IMAGES*column + WIDTH_OF_IMAGES//2
        num = Text(Point(location_x, location_y), column)
        num.draw(window)


def draw_row_headers(game_board_markers, window):
    '''
    Draws the numbers at the side of each row.
    '''
    location_x = LEFT_OFFSET - HEIGHT_OF_IMAGES/2
    for row in range(len(game_board_markers)):
        location_y = TOP_OFFSET + WIDTH_OF_IMAGES*row + WIDTH_OF_IMAGES//2
        num = Text(Point(location_x, location_y), row)
        num.draw(window)


def draw_game_message(window, window_width, message):
    text = Text(Point(window_width / 2, TOP_OFFSET / 2), message)
    text.setSize(16)
    text.draw(window)
        
def main():
    difficulty = get_difficulty()
    difficulty_variables = get_difficulty_variables(difficulty)
    rows = difficulty_variables[0]
    columns = difficulty_variables[1]
    number_of_mines = difficulty_variables[2]

    game_board_markers = create_minesweeper_matrix(rows, columns)

    game_board_markers = populate_with_mines(game_board_markers, number_of_mines,
                                            rows, columns)
    
    game_board_markers = add_mine_counts(game_board_markers)

    window_width = LEFT_OFFSET + RIGHT_OFFSET + columns*WIDTH_OF_IMAGES
    window_height = TOP_OFFSET + BOTTOM_OFFSET + rows*HEIGHT_OF_IMAGES
    window = GraphWin('Minesweeper',window_width, window_height, autoflush=False)

    grid_cells = draw_the_grid(rows, columns, window)
    draw_board_numbers(game_board_markers, window)

    draw_column_headers(game_board_markers, window)
    draw_row_headers(game_board_markers, window)
    tiles = draw_tiles(game_board_markers, window)

    flipped_cells = 0
    
    #Here is where the game actually begins being played.
    game_status = 'playing'
    while game_status == 'playing':
        click_point = window.getMouse()
        if was_new_cell_clicked(game_board_markers, click_point) == True:
            print('we are in a new cell')
            click_output = handle_click(game_board_markers, click_point, tiles)
            if click_output == 'mine':
                print('Clicked a mine')
                game_status = 'lose'
                draw_game_message(window, window_width, 'Game Over')
            elif 0 <= click_output <= 9:
                print('flipping a cell')
                flipped_cells += click_output
        if flipped_cells == rows * columns - number_of_mines:
            game_status == 'win'
            draw_game_message(window, window_width, 'Winner')

        print(flipped_cells)

        
        
main()
