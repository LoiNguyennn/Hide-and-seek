import random

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# L1
class Hider:
    def __init__(self, position):
        self.position = position

    def announce(self, map):
        pos_x = self.position.x + random.randint(-1, 1)
        pos_y = self.position.y + random.randint(-1, 1)

        if pos_x < 0:
            pos_x = 0
        if pos_y < 0:
            pos_y = 0
        if pos_x > map.width - 1:
            pos_x = map.width - 1
        if pos_y > map.length - 1:
            pos_y = map.length - 1
        
        return Position(pos_x, pos_y)

    # L3
    def move(self, map):
        valid_moves = []
        seeker_pos = (-1, -1)
        for dx in range(-2, 2):
            for dy in range(-2, 2):
                if map[self.x + dx][self.y + dy] == 3:
                    seeker_pos = (self.x + dx, self.y + dy)
                if dx == 0 or abs(dx) == 2 or dy == 0 or abs(dy) == 2:
                    continue
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < map.width and 0 <= new_y < map.length and map[new_x][new_y] == 0: # ? Can 2 hiders move/in the same? 
                    valid_moves.append((new_x, new_y))

        max_distance = 0
        best_moves = []
        if seeker_pos != (-1, -1):
            for move in valid_moves:
                distance = abs(move[0] - seeker_x) + abs(move[1] - seeker_y)
            if distance > max_distance:
                max_distance = distance
                best_moves = [move]
            elif distance == max_distance:
                best_moves.append(move)
        
        if best_moves:
            new_pos = random.choice(best_moves)
            self.position = new_pos
    
    # L4 ?hiders move then can be wherever?
    def moveObstacles(self, map):
        pushable_obstacles = []
        for dx in range(-2, 2):
            for dy in range(-2, 2):
                new_pos = (self.x + dx, self.y + dy)
                if 0 <= new_pos.x < map.width and 0 <= new_pos.y < map.length and map[new_pos.x][new_pos.y] == 1:
                    pushable_obstacles.append(new_pos)

        # random, no algorithm yet
        if pushable_obstacles:
            obstacle_pos = random.choice(pushable_obstacles)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_obstacle_pos = (obstacle_x + dx, obstacle_y + dy)
                if 0 <= new_obstacle_pos.x < map.width and 0 <= new_obstacle_pos.y < map.length and map[new_obstacle_pos.x][new_obstacle_pos.y] == 0:
                    map[obstacle_pos.x][obstacle_pos.y] = 0
                    map[new_obstacle_pos.x][new_obstacle_pos.y] = map[obstacle_pos.x][obstacle_pos.y]
                    return