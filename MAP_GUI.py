import pygame
import sys
import math
from settings import *

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
            if MAP[row, col] == 2:
                pygame.draw.rect (
                    win,(69, 115, 195),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
                continue
            elif MAP[row, col] == 3:
                pygame.draw.rect (
                    win,(199, 51, 21),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
                continue
            # draw map in the game window
            pygame.draw.rect(
                win,
                (200, 200, 200) if MAP[row, col] == 1 else (100, 100, 100),
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