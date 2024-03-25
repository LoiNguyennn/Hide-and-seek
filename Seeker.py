from queue import Queue
from copy import deepcopy

DARK_CELL = {
	(-2, -2): [(-3, -3)],
	(-2, -1): [(-3, -2), (-3, -1)],
	(-1, -2): [(-2, -3), (-1, -3)],
	(-1, -1): [(-2, -2), (-2, -3), (-3, -2), (-3, -3)],

	(-1, 0): [(-2, 0), (-3, 0), (-2, 1), (-3, 1), (-2, -1), (-3, -1)],
	(-2, 0): [(-3, 0)],

	(-2, 1): [(-3, 1), (-3, 2)],
	(-2, 2): [(-3, 3)],
	(-1, 1): [(-2, 2), (-2, 3), (-3, 3), (-3, 2)],
	(-1, 2): [(-1, 3), (-2, 3)],

	(0, 1): [(-1, 2), (-1, 3), (0, 2), (0, 3), (1, 2), (1, 3)],
	(0, 2): [(0, 3)],

	(1, 1): [(2, 2), (2, 3), (3, 2), (3, 3)],
	(1, 2): [(1, 3), (2, 3)],
	(2, 1): [(3, 1), (3, 2)],
	(2, 2): [(3, 3)],

	(1, 0): [(2, -1), (2, 0), (2, 1), (3, -1), (3, 0), (3, 1)],
	(2, 0): [(3, 0)],

	(1, -1): [(2, -3), (2, -2), (3, -3), (3, -2)],
	(1, -2): [(1, -3), (2, -3)],
	(2, -1): [(3, -2), (3, -1)],
	(2, -2): [(3, -3)],

	(0, -1): [(-1, -2), (0, -2), (1, -2), (-1, -3), (0, -3), (1, -3)],
	(0, -2): [(0, -3)],
}

class Seeker:
	def __init__(self, num_hiders_left, position):
		self.num_hiders_left = num_hiders_left
		self.position = position
		self.visited = []

	def makingDecisionLV1(self, _map):
		# choose new position that give the most not visited position in vision
		r = len(_map)
		c = len(_map[0])
		x, y = self.position
		max_cnt = 0
		new_pos = (-1, -1)
		for dir in DIRECTION.LIST_DIR:
			for i in range(1, 1):
				v = (x + i * dir[0], y + i * dir[1])
				if v[0] < 0 or v[0] >= r or v[1] < 0 or v[1] >= c:
					break
				if _map[v[0]][v[1]] != '2':
					return v
				if _map[v[0]][v[1]] != '0':
					break
				if v not in self.visited:
					cnt = self.checkVision(_map)
					if cnt > max_cnt:
						max_cnt = cnt
						new_pos = v
		if new_pos == (-1, -1): 
			for i in range(r):
				for j in range(c):
					if _map[i][j] == '0' and (i, j) not in self.visited:
						cnt = self.checkVision(_map)
						if cnt > max_cnt:
							max_cnt = cnt
							new_pos = (i, j)
		return new_pos
	
	def makingDecisionLV2(self, _map):
		#multiple hiders
		# choose new position that give the most not visited position in vision
		r = len(_map)
		c = len(_map[0])
		x, y = self.position
		max_cnt = 0
		new_pos = (-1, -1)
		for dir in DIRECTION.LIST_DIR:
			for i in range(1, 1):
				v = (x + i * dir[0], y + i * dir[1])
				if v[0] < 0 or v[0] >= r or v[1] < 0 or v[1] >= c:
					break
				if _map[v[0]][v[1]] != '2':
					return v
				if _map[v[0]][v[1]] != '0':
					break
				if v not in self.visited:
					cnt = self.checkVision(_map)
					if cnt > max_cnt:
						max_cnt = cnt
						new_pos = v
		if new_pos == (-1, -1):
			for i in range(r):
				for j in range(c):
					if _map[i][j] == '0' and (i, j) not in self.visited:
						cnt = self.checkVision(_map)
						if cnt > max_cnt:
							max_cnt = cnt
							new_pos = (i, j)
		return new_pos
			
	def markSeen(self, _map):
		pass
		# mark all position in vision as visited
		
	def checkVision(self, _map):
		visible = []
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
						__map[x + pos[0]][y + pos[1]] = 'D'

	
		for dx in range(-3, 4):
			for dy in range(-3, 4):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if __map[x + dx][y + dy] == '0':
					visible.append((x + dx, y + dy)) # including empty cells, walls and hiders	
		return visible

	def GoTo(self, position, _map):
		# go to position, return path from current pos to destination pos
		r = len(_map)
		c = len(_map[0])

		path = []
		q = Queue(0)
		q.put(self.position)
		par = {
			self.position: (-1, -1)
		}
		visited = {
			self.position: True
		}
		while q.not_empty:
			u = q.get()
			for dir in DIRECTION.LIST_DIR:
				v = (u[0] + dir[0], u[1] + dir[1])
				if v[0] < 0 or v[0] >= r or v[1] < 0 or v[1] >= c:
					continue 
				if _map[v[0]][v[1]] == '0' or _map[v[0]][v[1]] == '2':	
					if v not in visited:
						visited[v] = True
						par[v] = u
						q.put(v)
						if v == position:
							while v != (-1, -1):
								path.append(v)
								v = par[v]
							path.reverse()
							return path
		return path

	def Move(self, DIR, _map):
		r = len(_map)
		c = len(_map[0])
		
		x, y = self.position
		x += DIR[0]
		y += DIR[1]
		
		if x < 0 or x >= r or y < 0 or y >= c:
			return False

		_map[self.position[0]][self.position[1]], _map[x][y] = _map[x][y], _map[self.position[0]][self.position[1]]
		self.position = (x, y)

		self.markSeen(_map)
		if _map[x][y] == '2':
			self.num_hiders_left -= 1
	
	def MoveLeft(self, _map):
		self.Move(DIRECTION.LEFT, _map)
	
	def MoveUp(self, _map):
		self.Move(DIRECTION.UP, _map)
	
	def MoveRight(self, _map):
		self.Move(DIRECTION.RIGHT, _map)
	
	def MoveDown(self, _map):
		self.Move(DIRECTION.DOWN, _map)
	
	def MoveLeftUp(self, _map):
		self.Move(DIRECTION.LEFT_UP, _map)
	
	def MoveRightUp(self, _map):
		self.Move(DIRECTION.RIGHT_UP, _map)

	def MoveLeftDown(self, _map):
		self.Move(DIRECTION.LEFT_DOWN, _map)

	def MoveRightDown(self, _map):
		self.Move(DIRECTION.RIGHT_DOWN, _map)


class DIRECTION:
	LEFT = (0, -1)
	UP = (-1, 0)
	RIGHT = (0, 1)
	DOWN = (1, 0)
	
	LEFT_UP = (-1, -1)
	RIGHT_UP = (-1, 1)
	LEFT_DOWN = (1, -1)
	RIGHT_DOWN = (1, 1)

	LIST_DIR = [LEFT, UP, RIGHT, DOWN, LEFT_UP, RIGHT_UP, LEFT_DOWN, RIGHT_DOWN]

# Test GoTo function
# M = [
# 	['1', '1', '0', '0'],
# 	['2', '1', '1', '0'],
# 	['0', '0', '0', '0'],
# 	['0', '0', '1', '0'],
# ]

# s = Seeker(0, (1, 0))
# path = s.GoTo((0, 2), M)

# for i in range(len(M)):
# 	for j in range(len(M[i])):
# 		print(M[i][j], end=' ')
# 	print()
# for pos in path:
# 	print(pos)