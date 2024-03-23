import pygame
import sys
import math
from settings import *

ROW = 10
COL = 25

SCREEN_HEIGHT = ROW * TILE_SIZE
SCREEN_WIDTH = COL * TILE_SIZE

# map
MAP = (
'111111111111111111111111111'
'100000000000000000000000001'
'100000000000000001100000001'
'100000000000000001000000001'
'100000000001000101011111111'
'100000000001000100000020001'
'111111111001000100020000001'
'100000000001000111000000201'
'100030000001000001000200001'
'100000000001000001000000001'
'100000000000000001000000001'
'111111111111111111111111111'
)

MAP = Map(False)
list = list()
seeker = None
MAP.generate_mobs(list, 4, seeker)

# init pygame
pygame.init()

# create game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set window title
pygame.display.set_caption('Hide and seek')

# init timer
clock = pygame.time.Clock()

# draw map
def draw_map():
    # loop over map rows
    for row in range(ROW):
        # loop over map columns
        for col in range(COL):
            # calculate square index
            square = row * COL + col
            if MAP[row, col] == '2':
                pygame.draw.rect (
                    win,(69, 115, 195),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
                continue
            elif MAP[row, col] == '3':
                pygame.draw.rect (
                    win,(199, 51, 21),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
                continue
            # draw map in the game window
            pygame.draw.rect(
                win,
                (200, 200, 200) if MAP[row, col] == '1' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )

# game loop
while True:
    # escape condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    
    # draw 2D map
    draw_map()
    

    # update display
    pygame.display.flip()
    
    # set FPS
    clock.tick(30)