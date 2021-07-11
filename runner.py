# https://youtube/watch?v=-8n91btt5d8
import random   # library for generating random numbers
import sys      # python window controls
import pygame   # https://www.pygame.org/docs


pygame.init()
print(pygame.get_init())

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
myFont = pygame.font.SysFont("monospace", 30)

BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

PLAYER_SIZE = 50
PLAYER_MOVE = 50
PLAYER_POS = [WIDTH/2, HEIGHT- 2 * PLAYER_SIZE]     # half way x, two players up from the bottom

ENEMY_SIZE = 50
ENEMY_POS = [random.randint(0,WIDTH - ENEMY_SIZE), 0]   # create enemy inside width of screen
ENEMY_LIST = [ENEMY_POS]    # List to handle multiple enemies
ENEMY_COUNT = 10
SPEED = ENEMY_SIZE / 5

GAME_OVER = False

SCORE = 0

CLOCK = pygame.time.Clock()

def set_level(SCORE, SPEED):
    if SCORE < 20:
        SPEED = 5
    elif SCORE < 40:
        SPEED = 8
    elif SCORE < 60:
        SPEED = 11
    else:
        SPEED = 15
    return SPEED

def drop_enemies(ENEMY_LIST):   # Send Enemies in waves, drop at the bottom of the window
    delay = random.random()
    if len(ENEMY_LIST) < ENEMY_COUNT and delay < 0.1:   # Populate the list at a delay
        x_pos = random.randint(0,WIDTH-ENEMY_SIZE)
        y_pos = 0
        ENEMY_LIST.append([x_pos, y_pos])

def draw_enemies(ENEMY_LIST):   # Draw Enemies in the generated list
    for ENEMY_POS in ENEMY_LIST:
        pygame.draw.rect(screen, BLUE, (ENEMY_POS[0], ENEMY_POS[1], ENEMY_SIZE, ENEMY_SIZE))

def update_enemy_pos(ENEMY_LIST, SCORE):
    for idx, ENEMY_POS in enumerate(ENEMY_LIST):    #while loop trick to index list
        if ENEMY_POS[1] >= 0 and ENEMY_POS[1] < HEIGHT:     # On the screen
            ENEMY_POS[1] += SPEED                           # Move it down
        else: 
            ENEMY_LIST.pop(idx)     # pop / drop off list when at bottom 0
            SCORE += 1
    return SCORE

def collision_check(ENEMY_LIST, PLAYER_POS):
    for ENEMY_POS in ENEMY_LIST:
        if detect_collision(PLAYER_POS, ENEMY_POS):
            return True
    return False

def detect_collision(PLAYER_POS, ENEMY_POS):    # Both positions are upper left of the drawn square
    p_x = PLAYER_POS[0]     # ranges left to right from player_pos[0] to player_pos[0] + player_size 
    p_y = PLAYER_POS[1]     # ranges top to bottom from player_pos[1] to player_pos[1] + player_size

    e_x = ENEMY_POS[0]      # ranges left to right from enemy_pos[0] to enemy_pos[0] + enemy_size
    e_y = ENEMY_POS[1]      # ranges top to bottom from enemy_pos[1] to enemy_pos[1] + enemy_size

    if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x + ENEMY_SIZE)):     # Check X overlap
        if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y + ENEMY_SIZE)):     # Check Y overlap
            return True     # only return after checking both X and Y
    return False


while not GAME_OVER:
    for event in pygame.event.get():
        print(event) # watch events in console
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            X = PLAYER_POS[0]
            Y = PLAYER_POS[1]
            if event.key == pygame.K_LEFT:
                X -= PLAYER_MOVE
            elif event.key == pygame.K_RIGHT:
                X += PLAYER_MOVE
            elif event.key == pygame.K_UP:
                Y -= PLAYER_MOVE
            elif event.key == pygame.K_DOWN:
                Y += PLAYER_MOVE
            PLAYER_POS = [X,Y] # use modified position for draw

    screen.fill(BLACK) # Background color

    # Update the position of the enemy  #Commented out upon multiple enemies: def update_enemy_pos
    # if ENEMY_POS[1] >= 0 and ENEMY_POS[1] < HEIGHT:   # On the screen
    #     ENEMY_POS[1] += SPEED                         # move it down
    # else: 
    #     ENEMY_POS[0] = random.randint(0, WIDTH-ENEMY_SIZE) # New Rand x at top
    #     ENEMY_POS[1] = 0

    # if detect_collision(PLAYER_POS, ENEMY_POS):  #Commented out since: def collision_check
    #     GAME_OVER = True
    #     break # breaks out before overlap redraw

    drop_enemies(ENEMY_LIST)
    SCORE = update_enemy_pos(ENEMY_LIST, SCORE)
    SPEED = set_level(SCORE, SPEED)

    text = "Score: " + str(SCORE)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(ENEMY_LIST, PLAYER_POS):
        GAME_OVER = True
        break
    
    draw_enemies(ENEMY_LIST)
    pygame.draw.rect(screen, RED, (PLAYER_POS[0], PLAYER_POS[1], PLAYER_SIZE, PLAYER_SIZE))

    CLOCK.tick(30)

    pygame.display.update()
