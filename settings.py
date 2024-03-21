# global constants
import random

class Map():
    def __init__(self, width: int, length: int):
        self.width, self.length = (width, length)
        self.__map = [[0] * length for _ in range(width)]

    def generate_object(self, top: int, left: int, bottom: int, right: int):
        if top > self.width or left > self.length or bottom > self.width or right > self.length or top > bottom or left > right:
            raise IndexError("The object is out of map's range.")
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                self.__map[i][j] = 1
        if top > 0 and left > 0 and self.__map[top - 1][left - 1] == 1:
            if self.__map[top][left - 1] != 1 or self.__map[top - 1][left] != 1:
                self.__map[top - 1][left] = 1
        if top > 0 and right < self.length - 1 and self.__map[top - 1][right + 1] == 1:
            if self.__map[top][right + 1] != 1 or self.__map[top - 1][right] != 1:
                self.__map[top - 1][right] = 1
        if bottom < self.width - 1 and right < self.length - 1 and self.__map[bottom + 1][right + 1] == 1:
            if self.__map[bottom + 1][right] != 1 or self.__map[bottom][right + 1] != 1:
                self.__map[bottom + 1][right] = 1
        if bottom < self.width - 1 and left > 0 and self.__map[bottom + 1][left - 1] == 1:
            if self.__map[bottom][left - 1] != 1 or self.__map[bottom + 1][left] != 1:
                self.__map[bottom + 1][left] = 1

    def generate_mobs(self, num_hider: int):
        for i in range(num_hider):
            while True:
                col = random.randint(0, self.width - 1)
                row = random.randint(0, self.length - 1)
                if self.__map[col][row] == 0:
                    self.__map[col][row] = 2
                    break
        while True:
            col = random.randint(0, self.width - 1)
            row = random.randint(0, self.length - 1)
            if self.__map[col][row] == 0:
                self.__map[col][row] = 3
                break
    
    def __getitem__(self, position) -> int:
        col, row = position
        return self.__map[col][row]
    
    def __setitem__(self, position, value: int):
        col, row = position
        self.__map[col][row] = value
        
ROW = 10
COL = 25
TILE_SIZE = 30

SCREEN_HEIGHT = ROW * TILE_SIZE
SCREEN_WIDTH = COL * TILE_SIZE

# map
MAP = (
'111111111111111111111111111'
'100000000000000000000000001'
'100000000000000001100000001'
'100000000000000001000000001'
'100000000001000101011111111'
'100000000001000100000020001'
'111111111001000100020000001'
'100000000001000111000000201'
'100030000001000001000200001'
'100000000001000001000000001'
'100000000000000001000000001'
'111111111111111111111111111'
)
MAP = Map(10, 25)
MAP.generate_object(1, 5, 3, 9)
MAP.generate_object(3, 11, 4, 13)
MAP.generate_mobs(4)



            
