# https://youtu.be/XGf2GcyHPhc?t=3015


import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):  # segment of snake
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1  # not at zero so the head, 0th cube, moves immediatly
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx  # keeping variable in move function
        self.dirny = dirny  # keeping variable in move function
        # incrementing through grid, not pixel count
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # like drawing grid below
        i = self.pos[0]
        j = self.pos[1]

        # sizing rect to be able to still see grid
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):    # whole snake
    body = []    # list of how many cubes
    turns = {}   # dictionary of movements

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)  # how many cubes
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # describe snake movement input

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # i = index, c = cubes objects enumerating a list of poisitions
        for i, c in enumerate(self.body):
            p = c.pos[:]    # p is the list of positions of the cubes
            # if position is in turns (key presses were added to terns list above)
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # only save the turns in the dictionary needed to describe the snake
                if i == len(self.body)-1:
                    # remove the last cube if it hits the turn
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:  # hit left side of screen
                    c.pos = (c.rows-1, c.pos[1])    # go to the right side
                # hit right side of screen
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    # the go to left side
                    c.pos = (0, c.pos[1])
                # hit the top of the screen
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)                   # go to the bottom
                # hit the bottom of the screen
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)        # go to the top
                else:
                    # move in the direction of the turn
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:  # depending on which way the tail was going, add a cube
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):   # index and cube defineing the snake body
            if i == 0:      # check to make sure the first cube has eyes
                c.draw(surface, True)
            else:           # draw the snake
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # vertical lines at different x's
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        # horizontal lines at different y's
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))  # fill with black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # make sure snack can't go on snake
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = cube.w
    height = width
    rows = cube.rows   # should divide height evenly
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    clock = pygame.time.Clock()

    flag = True
    while flag:
        pygame.time.delay(50)   # delay tick to 50ms so it doesn't run too fast
        clock.tick(10)          # 10 frames per second
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            # check the list of body positions for collision
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ' + str(len(s.body)))
                message_box('You lost! ', 'Play again...')
                s.reset(10, 10)
                break

        redrawWindow(win)       # redraw picture

    pass

# rows =
# w =
# h =

# cube.rows = rows
# cube.w = w


main()
