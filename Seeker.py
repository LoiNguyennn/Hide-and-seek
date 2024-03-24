from queue import Queue

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
		# mark all position in vision as visited
		
	def checkVision(self, _map):
		# return number of not visited position in vision

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
				if _map[v[0]][v[1]] != '0':
					continue

				if v not in visited:
					visited[v] = True
					par[v] = u
					q.put(v)
					if v == position:
						tmp = _map[self.position[0]][self.position[1]]
						_map[self.position[0]][self.position[1]] = _map[position[0]][position[1]]
						_map[position[0]][position[1]] = tmp
						self.position = position

						while v != (-1, -1):
							path.append(v)
							v = par[v]
						path.reverse()
						return path
		return path

	def Move(self, DIR, _map):
		x, y = self.position
		x += DIR[0]
		y += DIR[1]
		self.position = (x, y)
		self.markSeen(_map)
		if _map[x][y] == '2':
			self.num_hiders_left -= 1
	
	def MoveLeft(self):
		self.Move(DIRECTION.LEFT)
	
	def MoveUp(self):
		self.Move(DIRECTION.UP)
	
	def MoveRight(self):
		self.Move(DIRECTION.RIGHT)
	
	def MoveDown(self):
		self.Move(DIRECTION.DOWN)
	
	def MoveLeftUp(self):
		self.Move(DIRECTION.LEFT_UP)
	
	def MoveRightUp(self):
		self.Move(DIRECTION.RIGHT_UP)

	def MoveLeftDown(self):
		self.Move(DIRECTION.LEFT_DOWN)

	def MoveRightDown(self):
		self.Move(DIRECTION.RIGHT_DOWN)


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