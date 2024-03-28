from queue import Queue
from queue import PriorityQueue
from copy import deepcopy

class Seeker:
	def __init__(self, num_hiders_left, position, map):
		self.num_hiders_left = num_hiders_left
		self.position = position
		self.map = map
		self.visited = []
		self.seen = []
	
	def evaluate(self, x, y):
		ret = (abs(self.position[0] - x) + abs(self.position[1] - y)) - self.checkVisionXY(x, y)
		#if the position is hider, return 0
		if self.map[x][y] == '2':
			return 0
		if self.checkVisionXY(x, y) == 0:
			ret = 100000
		return ret
	
	def greedySearch(self):
		# return the next position to go
		# if there is a hider in vision, go to that position
		# else, go to the position that has the most not visited position in vision
		_map = self.map
		r = len(_map)
		c = len(_map[0])
		visible = self.checkVision()
		#return if there is a hider in vision
		hider = self.checkHiderInVision()
		if len(hider) > 0:
			return hider[0]
		min_evaluate = 100000
		next_pos = self.position

		for dir in DIRECTION.LIST_DIR:
			x, y = self.position
			x += dir[0]
			y += dir[1]
			if x < 0 or x >= r or y < 0 or y >= c:
				continue
			if _map[x][y] == '2':
				print("Hider in next position")
				return (x, y)
			#return the position that has the min evaluate value
			if _map[x][y] == '0':
				evaluate = self.evaluate(x, y)
				if evaluate < min_evaluate:
					min_evaluate = evaluate
					next_pos = (x, y)
		if next_pos == self.position:
			#choose the not visited position that has the minimum evaluate value
			for i in range(r):
				for j in range(c):
					if _map[i][j] == '0':
						evaluate = self.evaluate(i, j)
						if evaluate < min_evaluate:
							min_evaluate = evaluate
							next_pos = (i, j)
		return next_pos
	
	def dpBitmask(self):
		_map = deepcopy(self.map)
		schedule = self.Scheduling()
		start = len(schedule) + 1
		r = len(_map)
		c = len(_map[0])

		# Initialize dp array with larger initial values
		dp = [[float('inf')] * (len(schedule) + 2) for _ in range(1 << len(schedule))]

		# Initialize dp array
		for i in range(0, len(schedule)):
			dp[1 << i][i] = self.GoToXY(self.position, schedule[i])
		# Initialize traceback array
		traceback = [[-1] * (len(schedule) + 2) for _ in range(1 << len(schedule))]

		# Preprocess the dist array
		dist = []
		for i in range(0, len(schedule)):
			dist.append([])
			for j in range(0, len(schedule)):
				dist[i].append(self.GoToXY(schedule[i], schedule[j]))
		# Calculate dp bitmask every position visit once, don't visit start position
		for mask in range(0, 1 << len(schedule)):
			print("Mask: ", mask)
			for i in range(0, len(schedule)):
				if (mask >> i) & 1:
					for j in range(0, len(schedule)):
						if (mask >> j) & 1:
							if (dp[mask][i] > dp[mask ^ (1 << i)][j] + dist[j][i]):
								dp[mask][i] = dp[mask ^ (1 << i)][j] + dist[j][i]
								traceback[mask][i] = j
		# Print distance matrix
		for i in range(0, len(schedule)):
			for j in range(0, len(schedule)):
				print(dist[i][j], end = " ")
			print()
		# Print dp matrix
		for i in range(0, len(schedule)):
			for j in range(0, len(schedule)):
				print(dp[i][j], end = " ")
			print()
		# Print traceback matrix
		for i in range(0, 1<<len(schedule) - 1):
			for j in range(0, len(schedule)):
				print(traceback[i][j], end = " ")
			print()
			


		
			
	def markSeen(self):
		# mark all position in vision as seen
		_map = deepcopy(self.map)
		x, y = self.position
		r = len(_map)
		c = len(_map[0])
		for dx in range(-2, 3):
			for dy in range(-2, 3):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if _map[x + dx][y + dy] == '1':
					for pos in DARK_CELL[(dx, dy)]:
						if x + pos[0] < 0 or x + pos[0] >= r or y + pos[1] < 0 or y + pos[1] >= c:
							continue
						_map[x + pos[0]][y + pos[1]] = 'D'
		for dx in range(-3, 4):
			for dy in range(-3, 4):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if _map[x + dx][y + dy] == '0':
					self.seen.append((x + dx, y + dy))

		
	def checkVision(self):
		_map = deepcopy(self.map)
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
						if x + pos[0] < 0 or x + pos[0] >= r or y + pos[1] < 0 or y + pos[1] >= c:
							continue
						__map[x + pos[0]][y + pos[1]] = 'D'

		for dx in range(-3, 4):
			for dy in range(-3, 4):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if __map[x + dx][y + dy] == '0':
					visible.append((x + dx, y + dy))
		return visible
	
	def checkHiderInVision(self):
		_map = deepcopy(self.map)
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
						if x + pos[0] < 0 or x + pos[0] >= r or y + pos[1] < 0 or y + pos[1] >= c:
							continue
						__map[x + pos[0]][y + pos[1]] = 'D'

		for dx in range(-3, 4):
			for dy in range(-3, 4):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if __map[x + dx][y + dy] == '2':
					visible.append((x + dx, y + dy))
		return visible

	def checkVisionXY(self, x, y):
		#return the number of not visited position in vision of (x, y)
		_map = deepcopy(self.map)
		num_not_seen = 0
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
		for dx in range(-3, 4):
			for dy in range(-3, 4):
				if x + dx < 0 or x + dx >= r or y + dy < 0 or y + dy >= c:
					continue
				if __map[x + dx][y + dy] == '0' and (x + dx, y + dy) not in self.seen:
					num_not_seen += 1
		return num_not_seen
	
	def GoToXY(self, start, goal):
    # go from start to goal, return path from start to goal
		_map = deepcopy(self.map)
		r = len(_map)
		c = len(_map[0])

		path = []
		q = Queue(0)
		q.put(start)
		par = {
			start: (-1, -1)
		}
		visited = {
			start: True
		}
		while not q.empty():
			u = q.get()
			for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Assuming DIRECTION.LIST_DIR is not available
				v = (u[0] + dir[0], u[1] + dir[1])
				if v[0] < 0 or v[0] >= r or v[1] < 0 or v[1] >= c:
					continue
				if _map[v[0]][v[1]] == '0' or _map[v[0]][v[1]] == '2':
					if v not in visited:
						visited[v] = True
						par[v] = u
						q.put(v)
						if v == goal:
							while v != (-1, -1):
								path.append(v)
								v = par[v]
							path.reverse()
							return len(path)
		return len(path)


	def GoTo(self, position):
		# go to position, return path from current pos to destination pos
		_map = deepcopy(self.map)
	
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

	def Scheduling(self):
		_map = deepcopy(self.map)
		r = len(_map)
		c = len(_map[0])

		visible_pos = dict()
		pq = PriorityQueue(0)
		for i in range(r):
			for j in range(c):
				if _map[i][j] == 'x' or _map[i][j] == '1':
					continue
				if _map[i][j] == '0':
					backup_pos = self.position
					self.position = (i, j) # fake
					visible = self.checkVision()
					self.position = backup_pos
					pq.put( ( -1 * len(visible), (i,j) ) )
					visible_pos[(i, j)] = visible
		schedule = []
		while not pq.empty():
			num_visible, pos = pq.get()
			if _map[pos[0]][pos[1]] == 'x':
				continue
			schedule.append(pos)
			for i, j in visible_pos[pos]:
				_map[i][j] = 'x'
		
		return schedule

	def Go4Checking(self):
		schedule = self.Scheduling()
		for target in schedule:
			path = self.GoTo(target)
			for pos in path:
				print(pos)
				self.Move((pos[0] - self.position[0], pos[1] - self.position[1]))

	def Move(self, DIR):
		r = len(self.map)
		c = len(self.map[0])
		
		x, y = self.position
		x += DIR[0]
		y += DIR[1]
		
		if x < 0 or x >= r or y < 0 or y >= c:
			return False

		if self.map[x][y] == '2':
			self.map[self.position[0]][self.position[1]] = '0'
			self.num_hiders_left -= 1
		else:
			self.map[self.position[0]][self.position[1]], self.map[x][y] = self.map[x][y], self.map[self.position[0]][self.position[1]]
		self.position = (x, y)
		self.markSeen()


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

DARK_CELL = {
	(-2, -2): [(-3, -3)],
	(-2, -1): [(-3, -2), (-3, -1)],
	(-1, -2): [(-2, -3), (-1, -3)],
	(-1, -1): [(-2, -2), (-2, -3), (-3, -2), (-3, -3), (-1, -3), (-1, -2), (-2, -1), (-3, -1)],

	(-2, 0): [(-3, -1), (-3, 0), (-3, 1)],
	(-1, 0): [(-2, 0), (-3, 0), (-2, 1), (-3, 1), (-2, -1), (-3, -1), (-3, -2), (-3, 2)],

	(-2, 2): [(-3, 3)],
	(-2, 1): [(-3, 1), (-3, 2)],
	(-1, 2): [(-1, 3), (-2, 3)],
	(-1, 1): [(-2, 2), (-2, 3), (-3, 3), (-3, 2), (-3, 1), (-2, 1), (-1, 2), (-1, 3)],

	(0, 2): [(-1, 3), (0, 3), (1, 3)],
	(0, 1): [(-1, 2), (-1, 3), (0, 2), (0, 3), (1, 2), (1, 3), (-2, 3), (2, 3)],

	(2, 2): [(3, 3)],
	(1, 2): [(1, 3), (2, 3)],
	(2, 1): [(3, 1), (3, 2)],
	(1, 1): [(2, 2), (2, 3), (3, 2), (3, 3), (1, 2), (1, 3), (2, 1), (3, 1)],

	(2, 0): [(3, -1), (3, 0), (3, 1)],
	(1, 0): [(2, -1), (2, 0), (2, 1), (3, -1), (3, 0), (3, 1), (3, -2), (3, 2)],

	(2, -2): [(3, -3)],
	(1, -2): [(1, -3), (2, -3)],
	(2, -1): [(3, -2), (3, -1)],
	(1, -1): [(2, -3), (2, -2), (3, -3), (3, -2), (1, -2), (1, -3), (2, -1), (3, -1)],

	(0, -2): [(-1, -3), (0, -3), (1, -3)],
	(0, -1): [(-1, -2), (0, -2), (1, -2), (-1, -3), (0, -3), (1, -3), (-2, -3), (2, -3)],
}