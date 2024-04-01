# global constants
import pygame
import os
import threading
import time
import sys
import threading
from Seeker import *
from Hider import *
from GameMenu import *
# from Hider import *
SPEED = 4
TILE_SIZE = 15
SEEKER_COLOR = (69, 115, 195)
HIDER_COLOR  = (199, 51, 21)
WALL_COLOR = (200, 200, 200) 
GROUND_COLOR = (0, 0, 0) 
LIGHT_COLOR = (255, 255, 102)
ALERT_COLOR = (168, 208, 141)
DOT_COLOR = (210, 15, 233)
ANNOUNCE_COLOR = (0, 153, 76)

class Game():
    def __init__(self):
        #Initialized game
        self.win = None

        self.point = 0
        self.list_hider = list()
        self.__map = list()
        self.list_announce = list()
        #Input game
        menu = GameMenu()
        self.__level = int(menu.level)
        file_name = menu.file_name
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
                with open('map/' + file_name + '.txt', 'r') as file:
                    lines = file.readlines()
        # #Input map
        self.width, self.length = (map(int, lines[0].split()))
        for i in range(1, self.width + 1):
            self.__map.append(lines[i].split())
        #Find all the hiders and seeker
        for col in range(self.width):
            for row in range(self.length):
                if self[(col, row)] == '2':
                    id = len(self.list_hider) + 1
                    self.list_hider.append(Hider((col, row), self.__map, id))
                elif self[(col, row)] == '3':
                    seeker_pos = (col, row)
        if self.__level == 1:
           self.level1_mobs()
        #Assign seeker
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
                return
                    
    #drawing funcions
    def draw_map(self):
        for row in range(self.width):
            for col in range(self.length):
                # draw map in the game window
                if self[(row, col)] == '1':
                    color = WALL_COLOR
                else:
                    color = GROUND_COLOR
                pygame.draw.rect (self.win, color , (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
        self.show_points()

    def draw_mobs(self):
        for spot in self.seeker.checkVision():
            pygame.draw.rect (self.win, LIGHT_COLOR , (spot[1] * TILE_SIZE, spot[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
        for hider in self.list_hider:
            pygame.draw.rect (self.win, HIDER_COLOR , (hider.position[1] * TILE_SIZE, hider.position[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
        for pos in self.list_announce:
            pygame.draw.rect(self.win, ANNOUNCE_COLOR, (pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
        pygame.draw.rect (self.win, SEEKER_COLOR , (self.seeker.position[1] * TILE_SIZE, self.seeker.position[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
        # schedule = self.seeker.Scheduling()
        # for pos in schedule:
        #     pygame.draw.rect (self.win, DOT_COLOR, (pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
    
    def announce(self):
        list_announce = list()
        for hider_pos in self.list_hider:
            pos = hider_pos.generate_random_pos(self.width, self.length)
            list_announce.append(pos)
            if pos in self.list_hider:
                continue
            self.__map[pos[0]][pos[1]] = '-' + str(hider_pos.id + 1)
        # avoid two different hiders using the same random positions
        return list_announce

    def show_points(self):
        font = pygame.font.SysFont('arial', 15)
        point_text = font.render(f'Point: {self.point}', True, (255, 255, 255))
        
        self.win.blit(point_text, (10, self.width * TILE_SIZE + 10))

    #-------------------------GAME LEVELS-------------------------------------
    #LEVEL 1 AND 2
    def level_1_2(self):
        # init pygame:
        pygame.init()
        pygame.font.init()
        SCREEN_HEIGHT = self.width * TILE_SIZE + 30
        SCREEN_WIDTH = self.length * TILE_SIZE

        # create game window
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.show_points()
        pygame.display.set_caption('Hide and seek')

        target = self.seeker.dpBitmask()
        canUseDP = True
        if target == None:
            target = self.seeker.Scheduling()
            canUseDP = False

        best_choice_index = 0
        visited = [False for _ in range(len(target))]

        step = 0
        self.point = 100 # initial points
        # # game loop
        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            if self.seeker.num_hiders_left == 0:
                time.sleep(3)
                return
            if canUseDP:
                path = self.seeker.GoTo(target[best_choice_index])
                
                for pos in path:
                    clock = pygame.time.Clock()
                    
                    seen = set()
                    hiders = self.seeker.checkHiderInVision()
                    for hider in hiders:
                        seen.add(hider)

                    if hiders:
                        while len(hiders):
                            location = hiders.pop(0)
                            path2 = self.seeker.GoTo(location)
                            for (x, y) in path2:
                                self.seeker.Move((x - self.seeker.position[0], y - self.seeker.position[1]))
                                if self[(x, y)] == '2':
                                    self[(x, y)] = '3'
                                    self.remove_hider((x, y))
                                    self.point += 20
                                self.point -= 1
                                self.win.fill((0, 0, 0))
                                self.draw_map()
                                self.draw_mobs()

                                step += 1
                                if step % 5 == 0:
                                    if self.list_announce:
                                        for pos in self.list_announce:
                                            if self.__map[pos[0]][pos[1]][0] == '-':
                                                self.__map[pos[0]][pos[1]] = '0'

                                    self.draw_mobs()

                                    self.list_announce.clear()
                                    self.list_announce = self.announce()

                                for hider in self.seeker.checkHiderInVision():
                                    if hider not in seen:
                                        hiders.append(hider)
                                        seen.add(hider)
                            
                                clock.tick(SPEED)
                                pygame.display.flip()
                        break
                    
                    if self.seeker.IsSignificantMove(path[-1]):
                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                    else:
                        if best_choice_index < len(target) - 1:
                            best_choice_index += 1           
                        else:
                            best_choice_index = 0    
                        break

                    self.point -= 1
                    step += 1
                    self.win.fill((0, 0, 0))
                    self.draw_map()
                    self.draw_mobs()

                    if step % 5 == 0:
                        if self.list_announce:
                            for pos in self.list_announce:
                                if self.__map[pos[0]][pos[1]][0] == '-':
                                    self.__map[pos[0]][pos[1]] = '0'

                        self.draw_mobs()
                        self.list_announce.clear()
                        self.list_announce = self.announce()
                        
                    clock.tick(SPEED)
                    pygame.display.flip()
                if best_choice_index < len(target) - 1:
                    best_choice_index += 1           
                else:
                    best_choice_index = 0          
            else: # Can't use DP
                best_choice_index = self.seeker.FindBestSpotIndex(target, visited)
                if best_choice_index == -1:
                    visited = [False for _ in range(len(target))]

                if visited[best_choice_index] == False:
                    best = target[best_choice_index]
                    visited[best_choice_index] = True

                path = self.seeker.GoTo(best)
                for pos in path:
                    clock = pygame.time.Clock()
                    
                    seen = set()
                    hiders = self.seeker.checkHiderInVision()
                    for hider in hiders:
                        seen.add(hider)

                    if hiders:
                        while len(hiders):
                            location = hiders.pop(0)
                            path2 = self.seeker.GoTo(location)
                            for (x, y) in path2:
                                self.seeker.Move((x - self.seeker.position[0], y - self.seeker.position[1]))
                                if self[(x, y)] == '2':
                                    self[(x, y)] = '3'
                                    self.remove_hider((x, y))
                                    self.point += 20
                                self.point -= 1
                                step += 1
                                self.win.fill((0, 0, 0))
                                self.draw_map()
                                self.draw_mobs()
                           
                                if step % 5 == 0:
                                    if self.list_announce:
                                        for pos in self.list_announce:
                                            if self.__map[pos[0]][pos[1]][0] == '-':
                                                self.__map[pos[0]][pos[1]] = '0'

                                    self.draw_mobs()
                                    self.list_announce.clear()
                                    self.list_announce = self.announce()
                                
                                for hider in self.seeker.checkHiderInVision():
                                    if hider not in seen:
                                        hiders.append(hider)
                                        seen.add(hider)
                                clock.tick(SPEED)
                                pygame.display.flip()
                        break
                    if self.seeker.IsSignificantMove(path[-1]):
                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                    else:
                        break
                    self.point -= 1
                    step += 1
                    # self.show_points()
                    self.win.fill((0, 0, 0))
                    self.draw_map()
                    self.draw_mobs()
                    if step % 5 == 0:
                        if self.list_announce:
                            for pos in self.list_announce:
                                if self.__map[pos[0]][pos[1]][0] == '-':
                                    self.__map[pos[0]][pos[1]] = '0'
                        self.draw_mobs()
                        self.list_announce.clear()
                        self.list_announce = self.announce()

                    clock.tick(SPEED)
                    pygame.display.flip()

    def getIdHider(self, position):
        for hider in self.list_hider:
            if hider.position == position:
                return hider.id
        return 0

    #LEVEL 3
    def level_3(self):  
       # init pygame:
        pygame.init()
        pygame.font.init()

        SCREEN_HEIGHT = self.width * TILE_SIZE + 30
        SCREEN_WIDTH = self.length * TILE_SIZE
        # create game window
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Hide and seek')

        spots = self.seeker.Scheduling()
        visited = [False for _ in range(len(spots))]
        steps = 0
        self.point = 100
        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            if self.seeker.num_hiders_left == 0:
                time.sleep(3)
                return

            closest_spot_index = self.seeker.FindBestSpotIndex(spots, visited)
            if closest_spot_index == -1:
                visited = [False for _ in range(len(spots))]

            if spots[closest_spot_index] == self.seeker.position:
                visited[closest_spot_index] = True
                continue

            path_to_closest_spot = self.seeker.GoTo(spots[closest_spot_index])
            clock = pygame.time.Clock()
            for step in path_to_closest_spot:
                foundHider = False
                last_seen = (-1, -1)
                while True:
                    # check if on the way to closest spot, are there any hiders
                    seen_hiders = self.seeker.checkHiderInVision()
                   
                    for i in range(len(self.__map)):
                        print(self.__map[i])
                    print()

                    if len(seen_hiders): # if see hider
                        # choose the closest hider to catch 
                        foundHider = True 
                        best_hider_idx = self.seeker.FindBestSpotIndex(seen_hiders)
                        path_to_best_hider = self.seeker.GoTo(seen_hiders[best_hider_idx])
                        pos = path_to_best_hider[0]
                        last_seen = seen_hiders[best_hider_idx]

                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                        
                        if self[pos] == '2':
                            self.__map[pos[0]][pos[1]] = '3'
                            self.remove_hider(pos)
                            self.point += 20

                        for i in range(len(self.list_hider)):
                            self.list_hider[i].Escape()  
                        
                        self.point -= 1

                        ############################################3
                        steps += 1
                        if steps % 5 == 0:
                            if self.list_announce:
                                for pos in self.list_announce:
                                    if self.__map[pos[0]][pos[1]][0] == '-':
                                        self.__map[pos[0]][pos[1]] = '0'
                            self.list_announce.clear()

                            for i in range(len(self.list_hider)):
                                self.list_hider[i].Escape()
                            self.list_announce = self.announce()
                        ############################################

                        self.win.fill((0, 0, 0))
                        self.draw_map()
                        self.draw_mobs()
                        
                        clock.tick(SPEED)      
                        pygame.display.flip()      
                    elif last_seen != (-1, -1):  
                        path_to_last_seen = self.seeker.GoTo(last_seen)
                        for step_to_last_seen in path_to_last_seen:
                            dx = step_to_last_seen[0] - self.seeker.position[0]
                            dy = step_to_last_seen[1] - self.seeker.position[1]
                            self.seeker.Move((dx, dy))

                            if self[step_to_last_seen] == '2':
                                self.__map[step_to_last_seen[0]][step_to_last_seen[1]] = '3'
                                self.remove_hider(step_to_last_seen)
                                self.point += 20

                            for i in range(len(self.list_hider)):
                                self.list_hider[i].Escape()  

                            self.point -= 1

                            ############################################
                            steps += 1
                            if steps % 5 == 0:
                                if self.list_announce:
                                    for pos in self.list_announce:
                                        if self.__map[pos[0]][pos[1]][0] == '-':
                                            self.__map[pos[0]][pos[1]] = '0'
                                self.list_announce.clear()
                                self.list_announce = self.announce()

                            ############################################
                            self.win.fill((0, 0, 0))
                            self.draw_map()
                            self.draw_mobs()
                            clock.tick(SPEED)      
                            pygame.display.flip()         
                        last_seen = (-1, -1)     
                        break
                    else: 
                        break    
                if foundHider:    
                    break
                else:
                    if self.seeker.IsSignificantMove(path_to_closest_spot[-1]):
                        self.seeker.Move((step[0] - self.seeker.position[0], step[1] - self.seeker.position[1]))
                    else:
                        visited[closest_spot_index] = True
                        break
                    for i in range(len(self.list_hider)):
                        self.list_hider[i].Escape() 
                    
                    self.point -= 1
                    ############################################
                    steps += 1
                    if steps % 5 == 0:
                        if self.list_announce:
                            for pos in self.list_announce:
                                if self.__map[pos[0]][pos[1]][0] == '-':
                                    self.__map[pos[0]][pos[1]] = '0'
                        self.list_announce.clear()
                        self.list_announce = self.announce()
                    ############################################

                    self.win.fill((0, 0, 0))
                    self.draw_map()
                    self.draw_mobs()
                    clock.tick(SPEED)     
                    pygame.display.flip()
                    if step == path_to_closest_spot[-1]:
                        visited[closest_spot_index] = True
                
    
    #LEVEL 4
    def level_4(self):
        return
    
    #PLAY
    def run_game(self):
        # Create and start the display_game thread
        # display_thread = threading.Thread(target=self.display_game, daemon=True)
        # display_thread.start()

        # Loop through each hider and create an update_seeker thread
        if self.__level < 3:
            self.level_1_2()
        elif self.__level == 3:
            self.level_3()
        else:
            self.level_4()

        # Join the display_game thread after all update_seeker threads have finished
        # display_thread.join()

        
###test run game:
        
game = Game()
game.run_game()