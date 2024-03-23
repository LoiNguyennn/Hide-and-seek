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
    def __init__(self, inputByKeyboard: bool):
        self.__map = list()
        if inputByKeyboard:
            width = int(input("Please enter the width of the map: "))
            length = int(input("Please enter the length of the map: "))
            self.width, self.length = (width, length)
            self.__map = [['0'] * length for _ in range(width)]
            self.blank = self.length * self.width
            #Input objects
            input_str = input("Please enter the object (a b c d): ")
            while input_str != "-1 0 0 0":
                input_list = input_str.split(' ')
                self.__map.generate_object(tuple(int(num) for num in input_list))
                input_str = input("Please enter the object (-1 0 0 0 to stop): ")
        else:
            with open('map.txt', 'r') as file:
                lines = file.readlines()
            self.width, self.length = (map(int, lines[0].split()))
            for i in range(1, self.width + 1):
                self.__map.append(lines[i].split())
            self.blank = self.length * self.width
            self.num_hider = sum(sublist.count('2') for sublist in self.__map)
            self.seek = any('3' in sublist for sublist in self.__map)
            i += 1 #object's line's index
            for j in range(i, len(lines)):
                self.generate_object(tuple(map(int, lines[j].split())))
    #Erase hider to remain number
    def erase_hider(self, remain: int):
        if self.num_hider <= remain:
            return
        for i in range(self.width):
                for j in range(self.length):
                    if self.__map[i][j] == '2':
                        self.num_hider -= 1
                        self.__map[i][j] = '0'
                        if self.num_hider == remain:
                            return  
    #Create object
    def generate_object(self, object: tuple):
        top, left, bottom, right = object
        if top > self.width or left > self.length or bottom > self.width or right > self.length or top > bottom or left > right:
            print("Invalid object")
            return
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                self.__map[i][j] = '1'
        if top > 0 and left > 0 and self.__map[top - 1][left - 1] == '1': #top left
            if self.__map[top][left - 1] != '1' and self.__map[top - 1][left] != '1':
                self.blank -= 1
                self.__map[top - 1][left] = '1'
        if top > 0 and right < self.length - 1 and self.__map[top - 1][right + 1] == '1': #top right
            if self.__map[top][right + 1] != '1' and self.__map[top - 1][right] != '1':
                self.blank -= 1
                self.__map[top - 1][right] = '1'
        if bottom < self.width - 1 and right < self.length - 1 and self.__map[bottom + 1][right + 1] == '1': #bottom right
            if self.__map[bottom + 1][right] != '1' and self.__map[bottom][right + 1] != '1':
                self.blank -= 1
                self.__map[bottom + 1][right] ='1'
        if bottom < self.width - 1 and left > 0 and self.__map[bottom + 1][left - 1] == '1': #bottom left
            if self.__map[bottom][left - 1] != '1' and self.__map[bottom + 1][left] != '1':
                self.blank -= 1
                self.__map[bottom + 1][left] = '1'
        self.blank -= (bottom - top + 1) * (right - left + 1)
    #Create mobs (hiders and seeker)
    def generate_mobs(self, list_hiders: list, num_hiders: int, seeker):
        num_hiders = min(num_hiders, self.blank) - self.num_hider
        for i in range(num_hiders):
            while True:
                row = random.randint(0, self.width - 1)
                col = random.randint(0, self.length - 1)
                if self.__map[row][col] == '0':
                    list_hiders.append(Hider((row, col)))
                    self.__map[row][col] = '2'
                    break
        if self.seek:
            for i, row in enumerate(self.__map):
                for j, elem in enumerate(row):
                    if elem == '3':
                        seeker = Seeker(num_hiders, (i, j))
            return
        while True:
            row = random.randint(0, self.width - 1)
            col = random.randint(0, self.length - 1)
            if self.__map[row][col] == '0':
                seeker = Seeker(num_hiders, (row, col))
                self.__map[row][col] = '3'
                break
    #Get square's value
    def __getitem__(self, position):
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
        pygame.display.set_caption('Hide and seek')
        clock = pygame.time.Clock()
        def draw_map():
            # loop over map rows
            for row in range(self.width):
                # loop over map columns
                for col in range(self.length):
                    # calculate square index
                    if self.__map[row][col] == '2':
                        pygame.draw.rect (
                            win,(69, 115, 195),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    elif self.__map[row][col] == '3':
                        pygame.draw.rect (
                            win,(199, 51, 21),(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    # draw map in the game window
                    pygame.draw.rect(
                        win,
                        (200, 200, 200) if self.__map[row][col] == '1' else (100, 100, 100),
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
        while True:
            cmd = int(input("How do you like to input map by: 1. File\t2. Keyboard\nYour call: "))
            if cmd == 1 or cmd == 2:
                break
        self.__map = Map(cmd - 1)
        self.__level = int(input("Please input the level of the game: "))
        #Generate mobs
        self.__list_hiders = []  # Initialize the list of hiders
        self.__seeker = None  # Initialize the seeker
        num_hider = 1
        if self.__level > 1:
            num_hider = int(input("Please enter number of hiders: "))
            while num_hider < 1:
                num_hider = int(input("Please re-enter number of hiders: "))
        else:
           self.__map.erase_hider(1)
        self.__map.generate_mobs(self.__list_hiders, num_hider, self.__seeker)
        self.__point = MAX_POINT

    def run_game(self):
        self.__map.display_game()
        
###test run game:
        
# game = HideAndSeek()
# game.run_game()