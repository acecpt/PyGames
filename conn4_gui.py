# https://youtu.be/XGf2GcyHPhc?t=8012

import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COL_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0   #If top row,col = 0 then ok, else, same user try again

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):    
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check Horizontal Win
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check Vertical for Win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check for positive slope diagonal
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check for negative slope diagonal            
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    # Iterate through spots on board
    # background first
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    # player colors from bottom up
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):    
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
WIDTH = COL_COUNT*SQUARESIZE
HEIGHT = (ROW_COUNT+1)*SQUARESIZE
RADIUS = int(SQUARESIZE/2 -5)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION: # without PenUp there's a trial
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            # #Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render("Player 1 WINS!", 1, RED)
                    screen.blit(label, (40,10))
                    game_over = True

            # #Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("Player 2 WINS!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2 # Turn MOD 2 to alternate between 0 and 1   

            if game_over:
                pygame.time.wait(500) #time in miliseconds
