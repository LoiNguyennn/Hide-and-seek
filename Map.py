# global constants
import random
import pygame
import threading
import time
import sys
import threading
from Seeker import *
TILE_SIZE = 30
SEEKER_COLOR = (69, 115, 195)
HIDER_COLOR  = (199, 51, 21)
WALL_COLOR = (200, 200, 200) 
GROUND_COLOR = (100, 100, 100)
LIGHT_COLOR = (255, 255, 102)
ALERT_COLOR = (168, 208, 141)

class Hider():
    def __init__(self, position):
        self.position = position

def check_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return True
    except FileNotFoundError:
        return False
    except IOError:
        return False
    
class Map():
    def __init__(self, file_name):
        self.list_hider = list()
        self.__map = list()
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"The file {file_name} could not be opened.", end = ' ')
            return False
        self.width, self.length = (map(int, lines[0].split()))
        #Input map
        for i in range(1, self.width + 1):
            self.__map.append(lines[i].split())
        seeker_pos = (-1, -1)
        #Find all the hiders and seeker
        for col in range(self.width):
            for row in range(self.length):
                if self.__map[col][row] == '2':
                    self.list_hider.append(Hider((col, row)))
                elif self.__map[col][row] == '3':
                    seeker_pos = (col, row)
        #Assign the seeker
        if seeker_pos != (-1, -1):
            self.seeker = Seeker(len(self.list_hider), seeker_pos, self.__map)
        i += 1 #object's line's index
        #Generate additional objects
        for j in range(i, len(lines)):
            self.generate_object(tuple(map(int, lines[j].split())))
    #Erase hider to remain number
    def level1(self):
        num_hider = len(self.list_hider)
        while num_hider > 1:
            self[self.list_hider.pop().position] = '0'
            num_hider -= 1
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
                self.__map[top - 1][left] = '1'
        if top > 0 and right < self.length - 1 and self.__map[top - 1][right + 1] == '1': #top right
            if self.__map[top][right + 1] != '1' and self.__map[top - 1][right] != '1':
                self.__map[top - 1][right] = '1'
        if bottom < self.width - 1 and right < self.length - 1 and self.__map[bottom + 1][right + 1] == '1': #bottom right
            if self.__map[bottom + 1][right] != '1' and self.__map[bottom][right + 1] != '1':
                self.__map[bottom + 1][right] ='1'
        if bottom < self.width - 1 and left > 0 and self.__map[bottom + 1][left - 1] == '1': #bottom left
            if self.__map[bottom][left - 1] != '1' and self.__map[bottom + 1][left] != '1':
                self.__map[bottom + 1][left] = '1'
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
            for row in range(self.width):
                for col in range(self.length):
                    # draw map in the game window
                    color = (0,0,0)
                    if self.__map[row][col] == '0':
                        color = GROUND_COLOR
                    elif self.__map[row][col] == '1':
                        color = WALL_COLOR
                    elif self.__map[row][col] == '2':
                        color = HIDER_COLOR
                    elif self.__map[row][col] == '3':
                        color = SEEKER_COLOR
                    
                    pygame.draw.rect (
                        win, color , (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                    )
                for pos in self.seeker.checkVision():
                    if pos == self.seeker.position:
                        continue 
                    pygame.draw.rect (
                        win, LIGHT_COLOR , (pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                    )
       
        path = self.seeker.GoTo((9, 24))
        scene = 0
        # game loop
        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            draw_map()
            if scene < len(path):
                self.seeker.Move((path[scene][0] - self.seeker.position[0], path[scene][1] - self.seeker.position[1]))
                scene += 1
            # draw_seen(self.seeker.checkVision(self.__map))
            # draw_hider(self.list_hider)
            # draw_seeker(self.seeker.position)
            # update display
            pygame.display.flip()
            # set FPS
            clock.tick(2)
    #run game
    def run_game(self):
        # Create and start the display_game thread
        
        '''
        display_thread = threading.Thread(target=self.display_game, daemon=True)
        display_thread.start()

        #an array to store all hiders' positions has been spotted by the seeker
        while self.seeker.num_hiders_left > 0:

            points = self.seeker.mapSweeping(self.__map)
        
            for point in points:
                path = self.seeker.GoTo(point, self.__map.copy())
                #mark visited position
                self.seeker.visited.append(point)

            for step in path:
                self.seeker.position = step
                if self.__map[step[0]][step[1]] == '2':
                    self.__map[step[0]][step[1]] = '0'
                    self.seeker.num_hiders_left -= 1
                    self.blank += 1
                    self.point += 1
                time.sleep(0.2)
            
            
        # Join the display_game thread after all update_seeker threads have finished
        display_thread.join()
        '''


class HideAndSeek():
    def __init__(self):
        #Input Map size
        file_name = input("Please enter the name of the map's file: ")
        while check_file(file_name) != True:
            file_name = input("There something went wrong, please enter file'name again: ")
        self.__map = Map(file_name)
        self.__level = -1
        while self.__level < 1 or self.__level > 4:
            self.__level = int(input("Please input the level of the game: "))
        if self.__level == 1:
           self.__map.level1()
        self.__point = 0

    def run_game(self):
       # self.__map.run_game()
        self.__map.display_game()
        
###test run game:
        
game = HideAndSeek()
game.run_game()