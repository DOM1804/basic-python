# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 10:02:57 2026

@author: DOM1804
"""
import os
from PIL import Image, ImageDraw

GENERATIONS = 10

CELL_SIZE = 20 #pixels
BORDER_WIDTH = 2 #pixels
BASE_COLOR = (0, 255, 0)  #bright green in RGB

def live_neighbors(grid, row, col):
    '''
    @requires: grid which is a list of lists where
      each list contains either 0 or 1
      meaning that the cell is dead(0) or alive(1). The size of the inner lists
      must be the same.
      Row and col are integers such that:
      0 <= row <= number of rows in grid
      0 <= col <= number of columns in grid
      
    @modifies: None
    @effects: None
    @raises: None
    @returns: the number of cells whose value equals 1
    
    TESTS
    >>> grid = [[0, 1, 0], [0, 0, 0], [1, 1, 0]]
    >>> live_neighbors(grid, 1, 0)
    3
    >>> live_neighbors(grid, 2, 2)
    1
    >>> live_neighbors(grid, 0, 1)
    0
    '''
    rows, cols = len(grid), len(grid[0])
    count = 0
    min_r = row - 1 if row >= 1 else 0
    max_r = row + 1 if row < rows - 1 else row
    min_c = col - 1 if col >= 1 else 0
    max_c = col + 1 if col < cols - 1 else col
    for idx_y in range(min_r, max_r + 1): #row index
        for idx_x in range(min_c, max_c + 1): #column index
            if idx_y == row and idx_x == col: #exclude the cell whose neighbors are counted
                continue
            if grid[idx_y][idx_x] == 1:
                count += 1
    return count

#Moves the simulation 1 step forward
#Based on the current state returns the next state generation as output
def model(grid):
    '''
    @requires: grid which is a list of lists where
      each list contains either 0 or 1
      meaning that the cell is dead(0) or alive(1). The size of the inner lists
      must be the same
      E.g.
      [[0,1,0],
       [0,0,0],
       [1,1,0]
       ]
    @modifies: None
    @effects: None
    @raises: None
    @returns: a new grid which follows the format of the input grid
      but with the cell values corresponding to the new generation.
      The generation is determined by the following rules:
          1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
          2. Any live cell with two or three live neighbours lives on to the next generation.
          3. Any live cell with more than three live neighbours dies, as if by overpopulation.
          4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    
    TESTS
    >>> grid = [[0,1,0],[0,0,0],[1,1,0]]
    >>> model(grid)
    [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    '''
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            live_nb = live_neighbors(grid, row, col)
            if grid[row][col] == 1 and (live_nb < 2 or live_nb > 3):
                new_grid[row][col] = 0
            elif grid[row][col] == 1 and live_nb in (2,3):
                new_grid[row][col] = 1
            elif grid[row][col] == 0 and live_nb == 3:
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = 0
    return new_grid


def read_input(filename):
    '''
    @requires: a filename of the valid CSV-file with rows of 0/1 separated by semicolon.
      Each line must have the same number of elements.
      File must exist and be readable from the same directory as the executed .py file
    @modifies: None
    @effects: None
    @raises: FileNotFoundError if the file not found.
      ValueError if the format invalid:
          - the file is empty (contains no valid rows)
          - any line contains non-integer values,
          - any value is not 0 or 1,
          - lines have inconsistent lengths.
    @returns: a grid which is a list of lists of integers (0/1)
    
    '''
    grid = []
    try:
        with open(filename, 'r') as input_file:
            lines = input_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f'File {filename} not found in the current directory.')
        
    for line_num, line in enumerate(lines):        
        stripped = line.strip() #by default strip removes string.whitespace characters 
        if not stripped:
            continue #skip empty lines
        try:
            data_row = [int(elem) for elem in stripped.split(';')]
        except ValueError:
            raise ValueError(f'Line_num {line_num}:non-integer value in {stripped}')
        
        for val in data_row:
            if val not in (0,1):
                raise ValueError(f'Line_num {line_num}: invalid value {val}, expected 0 or 1')
        
        if grid and len(data_row) != len(grid[0]): #length of the current list is not equal to the previously appended one
            raise ValueError(f'Line_num {line_num}: inconsistent number of columns (expected {len(grid[0])}, got {len(data_row)})')            
                    
        grid.append(data_row)
    #Empty/whitespace-only file check
    if not grid:
        raise ValueError(f'The file {filename} is empty or contains no valid data rows')
    
    return grid


def write_output(grid, filename):
    '''
    @requires: grid which is a list of lists of integers (0/1),
               filename to use for naming of the output file
    @modifies: writes CSV-file to file system (the current directory)
    @effects: creates or overwrites filename with grid in CSV format (semicolon-separated)
    @raises: IOError if cannot write the file
    @returns: None
    
    TESTS
    >>> grid = [[1,0],[0,1]]
    >>> import os
    >>> test_file = 'test_write.csv'
    >>> try:
    ...     write_output(grid, test_file)
    ...     with open(test_file, 'r') as f: content = f.read()
    ...     content
    ... finally:
    ...     if os.path.exists(test_file):
    ...         os.remove(test_file)
    '1;0\\n0;1\\n'
    '''
    with open(filename, 'w') as f:
        for row in grid:
            f.write(';'.join([str(elem) for elem in row]) + '\n')
        
def init_age_grid(grid):
    '''
    @requires: grid is a list of lists of 0/1
    @modifies: None
    @effects: None
    @raises: None
    @returns: age_grid with same dimensions as grid

    TESTS:
    >>> grid = [[1,0],[0,1]]
    >>> init_age_grid(grid)
    [[1, 0], [0, 1]]
    '''
    #created from scratch because age grid defines life expectancy, while grid - only current cell state
    return [[1 if cell == 1 else 0 for cell in row] for row in grid]


def update_age_grid(grid, prev_age_grid):
    '''
    @requires: grid and prev_age_grid have same dimensions;
               grid contains only 0/1;
               prev_age_grid contains non-negative integers
    @modifies: None
    @effects: None
    @raises: IndexError if dimensions mismatch
    @returns: new age_grid where alive cells increment age, dead cells reset to 0.

    TESTS:
    >>> grid = [[1,0],[1,1]]
    >>> prev = [[2,0],[3,1]]
    >>> update_age_grid(grid, prev)
    [[3, 0], [4, 2]]
    '''
    rows = len(grid)
    cols = len(grid[0])
    new_age = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                new_age[r][c] = prev_age_grid[r][c] + 1
    return new_age

def write_png(grid, age_grid, filename):
    '''
    @requires: grid and age_grid are same-sized lists of lists,
               grid contains 0/1,
               age_grid contains non-negative integers,
               filename to use for naming of the output file.
    @modifies: writes PNG file to file system (the current directory)
    @effects: saves image as PNG with age-based shading. Alive cells are shaded versions of BASE_COLOR (RGB).
              Darkest shade is 10% brightness. Dead cells are white.
    @raises: IOError if cannot save
    @returns: None

    TESTS:
    >>> grid = [[1,0],[1,1]]
    >>> age = [[1,0],[5,10]]
    >>> import os
    >>> test_file = 'test_shade.png'
    >>> try:
    ...     write_png(grid, age, test_file)
    ...     assert os.path.exists(test_file)
    ... finally:
    ...     if os.path.exists(test_file):
    ...         os.remove(test_file)
    '''    
    rows, cols = len(grid), len(grid[0])
    
    max_age = GENERATIONS
    
    cell_size = CELL_SIZE
    line_width = BORDER_WIDTH
    total_width = cols * (cell_size + line_width) + line_width
    total_height = rows *(cell_size + line_width) + line_width
    
    im = Image.new(mode='RGB', size=(total_width, total_height), color=(255, 255, 255)) #white background
    #im.show()
    #use ImageDraw-object to enable drawing
    draw = ImageDraw.Draw(im)

    #draw grid lines in light-gray
    #vertical
    for col in range(cols + 1):
        x = col * cell_size + col * line_width
        draw.line([(x, 0), (x, total_height)], fill=(200, 200, 200), width=line_width)

    #horizontal
    for row in range(rows + 1):
        y = row * cell_size + row * line_width
        draw.line([(0, y), (total_width, y)], fill=(200, 200, 200), width=line_width)

    #color live cells
    r_base, g_base, b_base = BASE_COLOR
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                age = age_grid[row][col]
                factor = max(0.1, 1.0 - min(age / max_age, 0.9))
                shaded_color = (
                    int(r_base * factor),
                    int(g_base * factor),
                    int(b_base * factor)
                )

                x0 = col * cell_size + col * line_width + line_width
                y0 = row * cell_size + row * line_width + line_width
                x1 = x0 + cell_size - 1
                y1 = y0 + cell_size - 1
                draw.rectangle([x0, y0, x1, y1], fill=shaded_color)

    # draw.rectangle([(BORDER_WIDTH, BORDER_WIDTH), 
    #                 (BORDER_WIDTH + CELL_SIZE, BORDER_WIDTH + CELL_SIZE)],
    #                fill='#00FF00', outline='#00FF00')
    
    im.save(filename)

def run_application():
    '''
    @requires: a valid CSV-file placed in the same directory as the executable file (working directory)
    @modifies: 
        - creates or uses the existing folder 'output_files' in the working directory,
        - creates output files (csv and png) for all generations and saves the result in the 'output_files' folder
    @effects:
        - asks user to enter the filename
        - validates the file format and content
        - simulates cell evolution
        - saves each generation in csv (grid) and png (visualization includes ageing) files.
    @raises:
        - FileNotFoundError — when file is not found by name;
        - ValueError — when the file format is not valid.
    @returns: None
    '''
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    while True:
        upload_file = input('Enter filename for upload, e.g. \'myfile.csv \' (without quotes):').strip()
        if not upload_file:
            print('The filename cannot be empty. Please, try again')
            continue
        if not upload_file.lower().endswith('.csv'):
            print('Accepted only csv format. Please, try again')
        try:
            grid = read_input(upload_file)
            break
        
        except FileNotFoundError as e:
            print(f'{e}')
        
        except ValueError as e:
            print(f'Error in the file: {e}')

    age_grid = init_age_grid(grid)

    #Save initial state in PNG-file
    write_png(grid, age_grid, os.path.join(output_dir, f"generation_{0:02d}.png"))

    for gen in range(1, GENERATIONS + 1):
        grid = model(grid)
        age_grid = update_age_grid(grid, age_grid)
        csv_path = os.path.join(output_dir, f"generation_{gen:02d}.csv")
        png_path = os.path.join(output_dir, f"generation_{gen:02d}.png")
        write_output(grid, csv_path)
        write_png(grid, age_grid, png_path)
    
    print('Simulation status: SUCCESS.\n Please, find the result in \'output_files\' folder (current directory)')
    
    
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    run_application()

