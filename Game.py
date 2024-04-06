# global constants
import pygame
import time
import sys
from Seeker import *
from Hider import *
from GameMenu import *

Speed = 2
Tile_Size = 25
SEEKER_COLOR = (69, 115, 195)
HIDER_COLOR  = (199, 51, 21)
OBJECT_COLOR = (254, 254, 254)
WALL_COLOR = (200, 200, 200) 
GROUND_COLOR = (0, 0, 0) 
LIGHT_COLOR = (255, 255, 102)
HIDER_LIGHT_COLOR = (236, 59, 119)
ALERT_COLOR = (168, 208, 141)
DOT_COLOR = (210, 15, 233)
ANNOUNCE_COLOR = (0, 153, 76)
OVERLAP_COLOR = (204, 130, 66)


class Game():
    def __init__(self):
        self.menu = GameMenu()
        if self.menu.exit or self.menu.file_name is None or self.menu.level is None:
            pass
        else:
            self.run_game()

    def run_game(self):
        global Speed
        Speed = self.menu.speed
        self.game = HideAndSeek(self.menu.file_name, self.menu.level)
        self.game.run_game()
        self.handle_end_menu()

    def handle_end_menu(self):
        self.end = EndMenu(self.game.win, self.game.point)
        while not self.end.goBack:
            self.game = HideAndSeek(self.menu.file_name, self.menu.level)
            self.game.run_game()    
            self.end = EndMenu(self.game.win, self.game.point)
        return Game()


class HideAndSeek():
    def __init__(self, file_name, level):
        #Initialized game
        self.win = 0
        self.point = 0
        self.list_hider = list()
        self.__map = list()
        self.list_announce = list()
        self.__level = level
        self.list_objects = []
        self.file_name = file_name
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
                cleaned_string  = file_name[:file_name.index("(")].strip()
                with open('map/' + cleaned_string + '.txt', 'r') as file:
                    lines = file.readlines()
        # #Input map
        self.width, self.length = map(int, lines[0].split())
        self.__map = [['1'] * (self.length + 2)]  # Initialize map with top border

        for i in range(1, self.width + 1):
            # Add '1' to the beginning and end of each line
            bordered_line = ['1'] + lines[i].split() + ['1']
            self.__map.append(bordered_line)

        self.__map.append(['1'] * (self.length + 2))  # Add bottom border
        self.length += 2
        self.width += 2
        
        #Set game window size
        global Tile_Size
        Tile_Size = min(750 // self.width, 1380 // self.length, Tile_Size)
        
        #Find all the hiders and seeker
        id = 0
        for col in range(1, self.width - 1):
            for row in range(1, self.length - 1):
                if self[(col, row)] == '2':
                    id += 1
                    self.list_hider.append(Hider((col, row), self.__map, id))
                elif self[(col, row)] == '3':
                    seeker_pos = (col, row)
        if self.__level == 1:
           self.level1_mobs()
        #Assign seeker
        self.seeker = Seeker(len(self.list_hider), seeker_pos, self.__map)
        #Generate additional objects
        fix_pos = (1,1,1,1)
        for j in range(i + 1, len(lines)):
            object = tuple(map(lambda x, y: x + y, fix_pos, tuple(map(int, lines[j].split()))))
            self.generate_object(object)

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
                if self[(i, j)] == '1':     
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
        self.list_objects.append(object)

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
        for i in range(0, len(self.list_hider)):
            if self.list_hider[i].position == position:
                self.list_hider.remove(self.list_hider[i])
                self.list_announce.remove(self.list_announce[i])
                return
                 
   
    def announce(self):
        list_announce = list()
        for hider_pos in self.list_hider:
            pos = hider_pos.generate_random_pos(self.width, self.length)
            list_announce.append(pos)
            if pos in self.list_hider:
                continue
            self.__map[pos[0]][pos[1]] = '-' + str(hider_pos.id)
        # avoid two different hiders using the same random positions
        return list_announce
    
    def getIdHider(self, position):
        for hider in self.list_hider:
            if hider.position == position:
                return hider.id
        return 0
    
    def checkSolvable(self):
        for hider in self.list_hider:
            dist = hider.CalcDist(hider.position, self.seeker.position)
            if dist == 'inf':
                print('unsolvable')
                return False 
        print('solvable')
        return True
    
    #drawing funcions
    def draw_map(self):
        self.win.fill((0,0,0))
        for row in range(self.width):
            for col in range(self.length):
                # draw map in the game window
                if self[(row, col)] == '1':
                    color = WALL_COLOR
                else:
                    color = GROUND_COLOR
                pygame.draw.rect (self.win, color , (col * Tile_Size, row * Tile_Size, Tile_Size , Tile_Size))
        for object in self.list_objects:
            top, left, bottom, right = object
            for i in range(top, bottom + 1):
                for j in range(left, right + 1):
                     pygame.draw.rect (self.win, OBJECT_COLOR , (j * Tile_Size, i * Tile_Size, Tile_Size , Tile_Size))
        self.show_attributes()
    
    def draw_seen_squares(self, spots, color):
        for spot in spots:
            pygame.draw.rect(self.win, color, (spot[1] * Tile_Size, spot[0] * Tile_Size, Tile_Size, Tile_Size))  

    def draw_mobs(self):
        #draw mobs's vision
        seeker_vision = self.seeker.checkVision()
        self.draw_seen_squares(seeker_vision, LIGHT_COLOR)
        overlap_pos = []
        if self.__level > 2:
            for hider in self.list_hider:
               hider_vision = hider.checkVision()
               overlap_pos.extend(hider_vision)
               self.draw_seen_squares((hider_vision), HIDER_LIGHT_COLOR)
            overlap_pos = set(overlap_pos).intersection(seeker_vision)
            self.draw_seen_squares(overlap_pos, OVERLAP_COLOR)
        #draw mobs
        for hider in self.list_hider:
            pygame.draw.rect (self.win, HIDER_COLOR , (hider.position[1] * Tile_Size, hider.position[0] * Tile_Size, Tile_Size - 2, Tile_Size - 2))
        for pos in self.list_announce:
            if self.__map[pos[0]][pos[1]][0] == '-':
                pygame.draw.rect(self.win, ANNOUNCE_COLOR, (pos[1] * Tile_Size, pos[0] * Tile_Size, Tile_Size - 2, Tile_Size - 2))
        pygame.draw.rect (self.win, SEEKER_COLOR , (self.seeker.position[1] * Tile_Size, self.seeker.position[0] * Tile_Size, Tile_Size - 2, Tile_Size - 2))

    def show_attributes(self):
        font = pygame.font.SysFont('arial', 22)
        text_surface = font.render(f' Level: {self.__level}, Size: {self.width-2}x{self.length-2}, Point: {self.point}, Hider left: {len(self.list_hider)}', True, (169, 205, 227))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)  # Position of the text on the window
        self.win.blit(text_surface, (10, self.width * Tile_Size + 10))
    
    #-------------------------GAME LEVELS-------------------------------------
    #LEVEL 1 AND 2
    def level_1_2(self):
        # init pygame:
        pygame.init()
        pygame.font.init()
        SCREEN_HEIGHT = self.width * Tile_Size + 40
        SCREEN_WIDTH = self.length * Tile_Size

        # create game window
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Hide and seek')

        target = self.seeker.dpBitmask()
        canUseDP = True
        if target == None:
            target = self.seeker.Scheduling()
            canUseDP = False

        best_choice_index = 0
        visited = [False for _ in range(len(target))]

        step = 0
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
                            
                                clock.tick(Speed)
                                pygame.display.flip()
                        break
                    if self.seeker.IsSignificantMove(path[-1]):
                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                    else:
                        break

                    self.point -= 1
                    step += 1
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
                        
                    clock.tick(Speed)
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
                                clock.tick(Speed)
                                pygame.display.flip()
                        break
                    if self.seeker.IsSignificantMove(path[-1]):
                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                    else:
                        break
                    self.point -= 1
                    step += 1
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

                    clock.tick(Speed)
                    pygame.display.flip()


    #LEVEL 3
    def level_3(self):  
       # init pygame:
        pygame.init()
        pygame.font.init()

        SCREEN_HEIGHT = self.width * Tile_Size + 40
        SCREEN_WIDTH = self.length * Tile_Size
        # create game window
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Hide and seek')

        spots = self.seeker.Scheduling()
        visited = [False for _ in range(len(spots))]
        steps = 0
        self.point = 0
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
                    announce_in_vision = []
                    seen_hiders = self.seeker.checkHiderInVision(announce_in_vision)
                   
                    # for i in range(len(self.__map)):
                    #     print(self.__map[i])
                    # print()

                    if len(seen_hiders): # if see hider
                        # choose the closest hider to catch 
                        foundHider = True 
                        best_hider_idx = self.seeker.FindBestSpotIndex(seen_hiders)
                        path_to_best_hider = self.seeker.GoTo(seen_hiders[best_hider_idx])
                        pos = path_to_best_hider[0]
                        last_seen = seen_hiders[best_hider_idx]

                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                        for idx, position in enumerate(spots):
                            if position == self.seeker.position:
                                visited[idx] = True

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
                            self.list_announce = self.announce()
                        ############################################

                        self.draw_map()
                        self.draw_mobs()
                        
                        clock.tick(Speed)      
                        pygame.display.flip()      
                    elif last_seen != (-1, -1):  
                        path_to_last_seen = self.seeker.GoTo(last_seen)
                        for step_to_last_seen in path_to_last_seen:
                            dx = step_to_last_seen[0] - self.seeker.position[0]
                            dy = step_to_last_seen[1] - self.seeker.position[1]
                            self.seeker.Move((dx, dy))
                            for idx, position in enumerate(spots):
                                if position == self.seeker.position:
                                    visited[idx] = True

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
                            self.draw_map()
                            self.draw_mobs()
                            clock.tick(Speed)      
                            pygame.display.flip()         
                        last_seen = (-1, -1)     
                        break                    
                    elif len(announce_in_vision):
                        foundHider = True
                        best_announce_idx = self.seeker.FindBestSpotIndex(announce_in_vision)
                        path_to_best_announce = self.seeker.GoTo(announce_in_vision[best_announce_idx])
                        pos = path_to_best_announce[0]
                        last_seen = announce_in_vision[best_announce_idx]

                        self.seeker.Move((pos[0] - self.seeker.position[0], pos[1] - self.seeker.position[1]))
                        for idx, position in enumerate(spots):
                            if position == self.seeker.position:
                                visited[idx] = True

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
                            self.list_announce = self.announce()
                        ############################################

                        self.draw_map()
                        self.draw_mobs()
                        
                        clock.tick(Speed)      
                        pygame.display.flip()                    
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

                    self.draw_map()
                    self.draw_mobs()
                    clock.tick(Speed)     
                    pygame.display.flip()
                    if step == path_to_closest_spot[-1]:
                        visited[closest_spot_index] = True
                
    
    #LEVEL 4
    def level_4(self):
        return

    #PLAY
    def run_game(self):
        if self.checkSolvable():
            if self.__level < 3:
                self.level_1_2()
            elif self.__level == 3:
                self.level_3()
            else:
                self.level_4()

        
###test run game:
