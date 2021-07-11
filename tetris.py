# https://youtu.be/XGf2GcyHPhc?t=9767
# 2:44:15
import pygame
import random

pygame.font.init()

# Global Vars Tetris has a 10 x 20 grid
s_width = 800   # screen width
s_height = 700  # screen height
play_width = 300    # 300 // 10 = 30 width per block
play_height = 600   # 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):    # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # defned by whichever shape, using index of shape and color
        self.color = shape_colors[shapes.index(shape)]
        # start with zeroth index of shape in shape list, click up arrow, index list to rotate
        self.rotation = 0


# * # Locked position is for any at-rest piece eg: (1:1), (255,255,255) for dict row
def create_grid(locked_pos={}):
    # list comprehension: create 1 black list for every 20 rows 10 squares/row
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):            # rows = i
        for j in range(len(grid[i])):   # colums = j
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c      # where c = color
    return grid


def convert_shape_format(shape):  # from lists above to list of only existing
    positions = []
    s_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(s_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # make an i,j list of where the shapes actually appear
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        # modify coordinates offset to recenter from upper left to center center
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                    for i in range(20)]    # if condition to check for black/empty
    # from [[(0,1)], [(2,3)]] to [(0,1), (2,3)] format - no sublists, easier to loop
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # in [(i,j), (i,j)] format - building an list of locked positions with zero collisions
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:     # check in exsting list
            if pos[1] > -1:     # skip y values that are spawned off screen due to offset login in convert_shape_format
                return False
    return True


# check to see if any position is above the screen and therfore you lost
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():  # *
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):  # draw lines for grid
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size),
                         (sx + play_width, sy + i*block_size))     # horiz lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),
                             (sx + j*block_size, sy + play_height))    # vert lines


def clear_rows(grid, locked):  # loop throug grid backward (bottom to top)

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:  # check to see that there's no black
            inc += 1    # if deleting a row, add one to increment so total shift is correct
            ind = i     # indexed row for removal
            for j in range(len(row)):  # get all the positions in the row
                try:
                    # delete from the locked_pos dictionary
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:     # have shifted and removed at least one row
        # sort list based on common y value; [::-1] = backwards
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:     # above (in pygame) the row for removal 
                newKey = (x, y + inc)   # move the stuff above down
                locked[newKey] = locked.pop(key)    # pop it onto anew list
    # bottom up scanning is to prevent over-writing upper objects onto lower locked positions (scanning to add to locked)
    return inc  # inc is the number of rows cleared

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    # Position the title and image
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    s_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(s_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # draw the next shape when needed
                pygame.draw.rect(surface, shape.color, (sx + j*block_size,
                                                        sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

def update_score(nscore):
    score = max_score()

    with open("PYGames\\tetris_scores.txt", 'w') as f:
        if int(score) > nscore: 
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open("PYGames\\tetris_scores.txt", 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score    

def draw_window(surface, grid, score = 0, last_score = 0):      # *
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))       # Format title
    surface.blit(label, (top_left_x + play_width/2 -
                         (label.get_width()/2), 30))       # Draw the title

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    # Position the score
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # Top score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))
    # Position the score
    sx = top_left_x - 220
    sy = top_left_y + 100
    surface.blit(label, (sx + 20, sy + 160))    

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                                                   top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                                            top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    # pygame.display.update()


def main(win):  # *
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        # update drawn grid to for locked positions
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()  # forcing tick instead of using fps which is machine specific

        if level_time/1000 > 5: 
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1  # placeholder for full drop
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # not above the screen so don't draw
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                # dictonary with key of position and rgb {(1,2):(255,0,0)} data structure of locked_positions
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # only call when changing pieces to prevent row clearing during fall
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "Game Over!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    
    pygame.display.quit()
    


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
