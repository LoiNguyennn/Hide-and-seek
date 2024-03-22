# global constants
import random
import pygame
import sys
from Seeker import *
MAX_POINT = 1000000
TILE_SIZE = 30

class Hider():
    def __init__(self, position):
        self.position = position
    
class Map():
    def __init__(self, width: int, length: int):
        self.width, self.length = (width, length)
        self.__map = [[0] * length for _ in range(width)]
        self.blank = length * width
    #Create object
    def generate_object(self, object: tuple):
        top, left, bottom, right = object
        if top > self.width or left > self.length or bottom > self.width or right > self.length or top > bottom or left > right:
            print("Invalid object")
            return
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                self.__map[i][j] = 1
        if top > 0 and left > 0 and self.__map[top - 1][left - 1] == 1:
            if self.__map[top][left - 1] != 1 or self.__map[top - 1][left] != 1:
                self.blank -= 1
                self.__map[top - 1][left] = 1
        if top > 0 and right < self.length - 1 and self.__map[top - 1][right + 1] == 1:
            if self.__map[top][right + 1] != 1 or self.__map[top - 1][right] != 1:
                self.blank -= 1
                self.__map[top - 1][right] = 1
        if bottom < self.width - 1 and right < self.length - 1 and self.__map[bottom + 1][right + 1] == 1:
            if self.__map[bottom + 1][right] != 1 or self.__map[bottom][right + 1] != 1:
                self.blank -= 1
                self.__map[bottom + 1][right] = 1
        if bottom < self.width - 1 and left > 0 and self.__map[bottom + 1][left - 1] == 1:
            if self.__map[bottom][left - 1] != 1 or self.__map[bottom + 1][left] != 1:
                self.blank -= 1
                self.__map[bottom + 1][left] = 1
        self.blank -= (bottom - top + 1) * (right - left + 1)
    #Create mobs (hiders and seeker)
    def generate_mobs(self, list_hiders: list, num_hiders: int, seeker: Seeker):
        for i in range(min(num_hiders, self.blank)):
            while True:
                row = random.randint(0, self.width - 1)
                col = random.randint(0, self.length - 1)
                if self.__map[row][col] == 0:
                    list_hiders.append(Hider((row, col)))
                    self.__map[row][col] = 2
                    break
        while True:
            row = random.randint(0, self.width - 1)
            col = random.randint(0, self.length - 1)
            if self.__map[row][col] == 0:
                seeker = Seeker(num_hiders, (row, col))
                self.__map[row][col] = 3
                break
    #Get square's value
    def __getitem__(self, position) -> int:
        row, col = position
        return self.__map[row][col]
    #Set square's value
    def __setitem__(self, position, value: int):
        row, col = position
        self.__map[row][col] = value
    #map's gui
    def display_game(self):
        # init pygame:
        pygame.init()
        SCREEN_HEIGHT = self.width * TILE_SIZE
        SCREEN_WIDTH = self.length * TILE_SIZE
        # create game window
        win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # set window title
        pygame.display.set_caption('Hide and seek')

        # init timer
        clock = pygame.time.Clock()

        # draw map
        def draw_map():
            # loop over map rows
            for row in range(self.width):
                # loop over map columns
                for col in range(self.length):
                    # calculate square index
                    if self.__map[row][col] == 2:
                        pygame.draw.rect (
                            win,(69, 115, 195),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    elif self.__map[row][col] == 3:
                        pygame.draw.rect (
                            win,(199, 51, 21),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    # draw map in the game window
                    pygame.draw.rect(
                        win,
                        (200, 200, 200) if self.__map[row][col] == 1 else (100, 100, 100),
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

class HideAndSeek():
    def __init__(self):
        #Input Map size
        self.__level = int(input("Please input the level of the game: "))
        width = int(input("Please enter the width of the map: "))
        length = int(input("Please enter the length of the map: "))
        self.__map = Map(width, length) # Initialize map
        #Input objects
        input_str = input("Please enter the object (a b c d): ")
        while input_str != "-1 0 0 0":
            input_list = input_str.split(' ')
            self.__map.generate_object(tuple(int(num) for num in input_list))
            input_str = input("Please enter the object (-1 0 0 0 to stop): ")
        #Generate mobs
        self.__list_hiders = []  # Initialize the list of hiders
        self.__seeker = None  # Initialize the seeker
        num_hider = 1
        if self.__level > 1:
            num_hider = int(input("Please enter number of hiders: "))
            while num_hider < 1:
                num_hider = int(input("Please re-enter number of hiders: "))
        self.__map.generate_mobs(self.__list_hiders, num_hider, self.__seeker)
        self.__point = MAX_POINT

    def run_game(self):
        self.__map.display_game()
        

game = HideAndSeek()
game.run_game()