import numpy as np
# import pygame

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

# def draw_board(board):
#     pass

board = create_board()
print_board(board)
game_over = False
turn = 0

# pygame.init()

# SQUARESIZE = 100
# WIDTH = COL_COUNT*SQUARESIZE
# HEIGHT = (ROW_COUNT+1)*SQUARESIZE

# size = (WIDTH, HEIGHT)
# screen = pygame.display.set_mode(size)


while not game_over:
    #Ask for Player 1 Input
    if turn == 0:
        col = int(input("Player 1 Make your Selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

        if winning_move(board, 1):
            print("Player 1 WINS!!")
            game_over = True

    #Ask for Player 2 Input
    else:
        col = int(input("Player 2 Make your Selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

        if winning_move(board, 2):
            print("Player 2 WINS!!")
            game_over = True

    print_board(board)

    turn += 1
    turn = turn % 2 # Turn MOD 2 to alternate between 0 and 1    
