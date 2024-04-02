import random
from copy import deepcopy
from Seeker import DIRECTION
from Seeker import DARK_CELL
from queue import Queue

# L1
class Hider:
    def __init__(self, position, map, id):
        self.position = position
        self.map = map
        self.id = id

    def checkVision(self):
        _map = deepcopy(self.map)
        visible = []
        x, y = self.position[0], self.position[1]
        r = len(_map)
        c = len(_map[0])
        __map = deepcopy(_map)

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
                    continue
                if __map[x + dx][y + dy] == '1':
                    for pos in DARK_CELL[(dx, dy)]:
                        if x + pos[0] < 0 or x + pos[0] >= r or y + pos[1] < 0 or y + pos[1] >= c:
                            continue
                        __map[x + pos[0]][y + pos[1]] = 'D'

        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
                    continue
                if __map[x + dx][y + dy] != 'D' and __map[x + dx][y + dy] != '1':
                    visible.append((x + dx, y + dy))
        return visible
    
    def checkSeekerInVision(self):
        _map = deepcopy(self.map)
        x, y = self.position[0], self.position[1]
        r = len(_map)
        c = len(_map[0])
        __map = deepcopy(_map)

        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
                    continue
                if __map[x + dx][y + dy] == '1':
                    for pos in DARK_CELL[(dx, dy)]:
                        if x + pos[0] < 0 or x + pos[0] >= r or y + pos[1] < 0 or y + pos[1] >= c:
                            continue
                        __map[x + pos[0]][y + pos[1]] = 'D'

        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
                    continue
                if __map[x + dx][y + dy] == '3':
                    return (x + dx, y + dy)
        return None
 
    def Move(self, dir):
        r = len(self.map)
        c = len(self.map[0])
        
        x, y = self.position
        x += dir[0]
        y += dir[1]
        
        if x < 0 or x >= r or y < 0 or y >= c:
            return False

        if self.map[x][y] == '1' or self.map[x][y] == '2' or self.map[x][y] == '3':
            return False
        else:
            self.map[x][y] = '0'

            tmp = self.map[self.position[0]][self.position[1]]
            self.map[self.position[0]][self.position[1]] = self.map[x][y]
            self.map[x][y] = tmp
        self.position = (x, y)

    def CalcDist(self, start, dest):
        r = len(self.map)
        c = len(self.map[0])

        visited = set()
        dist = dict()
        q = Queue(0)
        q.put(start)
        dist[start] = 0
        visited.add(start)
        while not q.empty():
            u = q.get()
            for dir in DIRECTION.LIST_DIR:
                if u[0] + dir[0] < 0 or u[0] + dir[0] >= r or u[1] + dir[1] < 0 or u[1] + dir[1] >= c:
                    continue 
                v = (u[0] + dir[0], u[1] + dir[1])
                if self.map[v[0]][v[1]] == '1':
                    continue
                if v not in visited:
                    visited.add(v)
                    dist[v] = dist[u] + 1
                    if v == dest:
                        return dist[v]
                    q.put(v)  
        return 0

    def Escape(self):
        r = len(self.map)
        c = len(self.map[0]) 
        seeker_pos = self.checkSeekerInVision()        
        if seeker_pos:
            best_dir = None
            max_dist = self.CalcDist(self.position, seeker_pos)
            for dir in DIRECTION.LIST_DIR:
                x = self.position[0] + dir[0]
                y = self.position[1] + dir[1]
                if x < 0 or x >= r or y < 0 or y >= c:
                    continue
                if self.map[x][y] == '1' or self.map[x][y] == '2' or self.map[x][y] == '3':
                    continue
                dist = self.CalcDist((x, y), seeker_pos)

                if dist >= max_dist:
                    max_dist = dist
                    best_dir = dir

            if best_dir == None:
                return False
            self.Move(best_dir)
            if self.id == 4:
                print(self.position)
        return True

    def generate_random_pos(self, width, length):
        list_pos = list()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                pos = (self.position[0] + i, self.position[1] + j)
                if (pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < length) and self.map[pos[0]][pos[1]] == '0':
                    list_pos.append(pos)
        
        if not list_pos:
            return(self.position)
        return (list_pos[random.randint(0, len(list_pos) - 1)])

    # # L3
    # def move(self, map):
    #     valid_moves = []
    #     seeker_pos = (-1, -1)
    #     for dx in range(-2, 2):
    #         for dy in range(-2, 2):
    #             if map[self.x + dx][self.y + dy] == 3:
    #                 seeker_pos = (self.x + dx, self.y + dy)
    #             if dx == 0 or abs(dx) == 2 or dy == 0 or abs(dy) == 2:
    #                 continue
    #             new_x = self.x + dx
    #             new_y = self.y + dy
    #             if 0 <= new_x < map.width and 0 <= new_y < map.length and map[new_x][new_y] == 0: # ? Can 2 hiders move/in the same? 
    #                 valid_moves.append((new_x, new_y))

    #     max_distance = 0
    #     best_moves = []
    #     if seeker_pos != (-1, -1):
    #         for move in valid_moves:
    #             distance = abs(move[0] - seeker_x) + abs(move[1] - seeker_y)
    #         if distance > max_distance:
    #             max_distance = distance
    #             best_moves = [move]
    #         elif distance == max_distance:
    #             best_moves.append(move)
        
    #     if best_moves:
    #         new_x, new_y = random.choice(best_moves)
    #         self.x, self.y = new_x, new_y
    
    # # L4 ?hiders move then can be wherever?
    # def moveObstacles(self, map):
    #     pushable_obstacles = []
    #     for dx in range(-2, 2):
    #         for dy in range(-2, 2):
    #             new_pos_x, new_pos_y = (self.x + dx, self.y + dy)
    #             if 0 <= new_pos_x < map.width and 0 <= new_pos_y < map.length and map[new_pos_x][new_pos_y] == 1:
    #                 pushable_obstacles.append(new_pos_x, new_pos_y)

    #     # random, no algorithm yet
    #     if pushable_obstacles:
    #         obstacle_pos_x, obstacle_pos_y = random.choice(pushable_obstacles)
    #         for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    #             new_obstacle_pos_x, new_obstacle_pos_y = (obstacle_x + dx, obstacle_y + dy)
    #             if 0 <= new_obstacle_pos_x < map.width and 0 <= new_obstacle_pos_y < map.length and map[new_obstacle_pos_x][new_obstacle_pos_y] == 0:
    #                 map[obstacle_pos_x][obstacle_pos_y] = 0
    #                 map[new_obstacle_pos_x][new_obstacle_pos_y] = map[obstacle_pos_x][obstacle_pos_y]
    #                 return