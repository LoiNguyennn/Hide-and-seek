# global constants
import random
import pygame
import threading
import time
import sys
import threading
from Seeker import *
# from Hider import *
TILE_SIZE = 15
SEEKER_COLOR = (69, 115, 195)
HIDER_COLOR  = (199, 51, 21)
WALL_COLOR = (200, 200, 200) 
GROUND_COLOR = (0, 0, 0) 
LIGHT_COLOR = (255, 255, 102)
ALERT_COLOR = (168, 208, 141)

class Hider():
    def __init__(self, position):
        self.position = position

class Game():
    def __init__(self):
        #Initialized game
        self.point = 0
        self.list_hider = list()
        self.__map = list()
        #Input game
        def read_file(file_name):
            try:
                with open(file_name + '.txt', 'r') as file:
                    return file.readlines()
            except FileNotFoundError:
                print(f"The file {file_name} could not be opened.", end = ' ')
                return None
        file_name = input("Please enter the name of the map's file: ")
        lines = read_file(file_name)
        while lines == None:
            file_name = input("There something went wrong, please enter file'name again: ")
            lines = read_file(file_name)
        self.__level = -1
        while self.__level < 1 or self.__level > 4:
            self.__level = int(input("Please input the level of the game: "))
        #Input map
        self.width, self.length = (map(int, lines[0].split()))
        for i in range(1, self.width + 1):
            self.__map.append(lines[i].split())
        #Find all the hiders and seeker
        seeker_pos = None
        for col in range(self.width):
            for row in range(self.length):
                if self[(col, row)] == '2':
                    self.list_hider.append(Hider((col, row)))
                elif self[(col, row)] == '3':
                    seeker_pos = (col, row)
        if self.__level == 1:
           self.level1_mobs()
        #Assign seeker
        if seeker_pos != None:
            self.seeker = Seeker(len(self.list_hider), seeker_pos, self.__map)
        #Generate additional objects
        for j in range(i + 1, len(lines)):
            self.generate_object(tuple(map(int, lines[j].split())))

    #Erase hider to remain number
    def level1_mobs(self):
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
        #Update map after each move
        
    #Delete caught hider
    def remove_hider(self, position):
            for hider in self.list_hider:
                if hider.position == position:
                    self.list_hider.remove(hider)
                    
    #-----------map's GUI------------#
    def display_game(self):
        # init pygame:
        pygame.init()
        SCREEN_HEIGHT = self.width * TILE_SIZE
        SCREEN_WIDTH = self.length * TILE_SIZE
        # create game window
        win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Hide and seek')
        clock = pygame.time.Clock()
        #drawing funcions
        def draw_map():
            for row in range(self.width):
                for col in range(self.length):
                    # draw map in the game window
                    if self[(row, col)] == '0':
                        color = GROUND_COLOR
                    else:
                        color = WALL_COLOR
                
                    pygame.draw.rect (
                        win, color , (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                    )
        def draw_hiders():
            for hider in self.list_hider:
                pygame.draw.rect (
                    win, HIDER_COLOR , (hider.position[1] * TILE_SIZE, hider.position[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
        def draw_seeker():
            pygame.draw.rect (
                win, SEEKER_COLOR , (self.seeker.position[1] * TILE_SIZE, self.seeker.position[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )
        def draw_seen():
            for pos in self.seeker.checkVision():
                pygame.draw.rect (
                    win, LIGHT_COLOR , (pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )
        # # game loop
        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            draw_map()
            draw_seen()
            draw_hiders()
            draw_seeker()
            
            pygame.display.flip()
            # set FPS
            clock.tick(30)
   
    #-------------------------GAME LEVELS-------------------------------------
    #LEVEL 1 AND 2
    def level_1_2(self):
        # i = 0
        # while self.seeker.num_hiders_left > 0:
        #     path = self.seeker.GoTo(self.seeker.greedySearch())
        #     for step in path:
        #         self.seeker.Move((step[0] - self.seeker.position[0], step[1] - self.seeker.position[1]))
        #         hiders = self.seeker.checkHiderInVision()
        #         if hiders:
        #             if (i == 1):
        #                 i = 0
        #                 continue
        #             i+=1
        #             print("Alert")
        #             break
        #         if self[step] == '2':
        #             self.remove_hider(step)
        #             self[step] = '3'
        #             self.point += 20
        #         else:
        #             self.point -= 1
        #         time.sleep(0.5)

        path = self.seeker.dpBitmask()
    
    #LEVEL 3
    def level_3(self):
        return
    
    #LEVEL 4
    def level_4(self):
        return
    
    #PLAY
    def run_game(self):
        # Create and start the display_game thread
        display_thread = threading.Thread(target=self.display_game, daemon=True)
        display_thread.start()

        # Loop through each hider and create an update_seeker thread
        if self.__level < 3:
            self.level_1_2()
        elif self.__level == 3:
            self.level_3()
        else:
            self.level_4()

        # Join the display_game thread after all update_seeker threads have finished
        display_thread.join()

        
###test run game:
        
game = Game()
game.run_game()