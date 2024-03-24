# global constants
import random
import pygame
import sys
from Seeker import *
MAX_POINT = 1000000
TILE_SIZE = 30
SEEKER_COLOR = (69, 115, 195)
HIDER_COLOR  = (199, 51, 21)
WALL_COLOR = (200, 200, 200) 
VISIBLE_COLOR = (255, 255, 102)

class Hider():
    def __init__(self, position):
        self.position = position
    
class Map():
    def __init__(self, inputByKeyboard: bool):
        self.list_hider = list()
        self.__map = list()
        self.seeker = None
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
            #Input map
            for i in range(1, self.width + 1):
                self.__map.append(lines[i].split())
            self.blank = self.length * self.width
            seeker_pos = (-1, -1)
            #Find all the hiders
            for col in range(self.width):
                for row in range(self.length):
                    if self.__map[col][row] == '2':
                        self.list_hider.append(Hider((col, row)))
                    elif self.__map[col][row] == '3':
                        seeker_pos = (col, row)
            #Assign the seeker
            if seeker_pos != (-1, -1):
                self.seeker = Seeker(len(self.list_hider), seeker_pos)
            i += 1 #object's line's index
            for j in range(i, len(lines)):
                self.generate_object(tuple(map(int, lines[j].split())))
    #Erase hider to remain number
    def level1(self):
        num_hider = len(self.list_hider)
        if num_hider > 1:
            for i in range(self.width):
                    for j in range(self.length):
                        if self.__map[i][j] == '2':
                            num_hider -= 1
                            self.__map[i][j] = '0'
                            if num_hider == 1:
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
    def generate_mobs(self, num_hiders: int):
        num_hider = min(num_hiders, self.blank) - len(self.list_hider)
        for i in range(num_hider):
            while True:
                row = random.randint(0, self.width - 1)
                col = random.randint(0, self.length - 1)
                if self.__map[row][col] == '0':
                    self.list_hider.append(Hider((row, col)))
                    self.__map[row][col] = '2'
                    break
        while self.seeker == None:
            row = random.randint(0, self.width - 1)
            col = random.randint(0, self.length - 1)
            if self.__map[row][col] == '0':
                self.seeker = Seeker(num_hiders + num_hider, (row, col))
                self.__map[row][col] = '3'
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
                            win,HIDER_COLOR,(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    elif self.__map[row][col] == '3':
                        pygame.draw.rect (
                            win,SEEKER_COLOR,(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
                        continue
                    # draw map in the game window
                    pygame.draw.rect(
                        win,
                        WALL_COLOR if self.__map[row][col] == '1' else VISIBLE_COLOR ,
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
        num_hider = 1
        if self.__level != 1:
            num_hider = int(input("Please enter number of hiders: "))
            while num_hider < 1:
                num_hider = int(input("Please re-enter number of hiders: "))
        else:
           self.__map.level1()
        self.__map.generate_mobs(num_hider)
        self.__point = MAX_POINT

    def run_game(self):
        self.__map.display_game()
        
###test run game:
        
game = HideAndSeek()
game.run_game()