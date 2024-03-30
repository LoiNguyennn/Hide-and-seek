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
			if len(schedule) >= 30:
				return None
			r = len(_map)
			c = len(_map[0])
			n = len(schedule)
			#dp[mask][u] is the minimum cost to reach mask state and end at position u
			dp = [[1000000 for i in range(n)] for j in range(1 << n)]
			par = [[-1 for i in range(n)] for j in range(1 << n)]
			#initialize
			for i in range(n):
				dp[1 << i][i] = self.GoToXY(self.position, schedule[i])
			#initialize dist[i][j] is the distance from i to j
			dist = [[1000000 for i in range(n)] for j in range(n)]
			for i in range(n):
				for j in range(n):
					dist[i][j] = self.GoToXY(schedule[i], schedule[j])
			#dp
			for mask in range(1 << n):
				for u in range(n):
					if (mask & (1 << u)) == 0:
						continue
					for v in range(n):
						if (mask & (1 << v)) == 0:
							continue
						if dp[mask ^ (1 << u)][v] + dist[v][u] < dp[mask][u]:
							dp[mask][u] = dp[mask ^ (1 << u)][v] + dist[v][u]
							par[mask][u] = v
			#find the minimum cost
			min_cost = 1000000
			u = -1
			for i in range(n):
				if dp[(1 << n) - 1][i] < min_cost:
					min_cost = dp[(1 << n) - 1][i]
					u = i
			#find the path
			path = []
			mask = (1 << n) - 1
			while u != -1:
				path.append(u)
				v = par[mask][u]
				mask ^= (1 << u)
				u = v
			path.reverse()
			xy_path = []
			for i in range(n):
				xy_path.append(schedule[path[i]])
			return xy_path	



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
				if _map[i][j] == '1':
					continue
			
				backup_pos = self.position
				self.position = (i, j) # fake
				visible = self.checkVision()
				self.position = backup_pos
				pq.put(( -1 * (( len(visible) + abs(i - r / 2) + abs(j - c / 2) )), (i, j)  ))
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
			tmp = self.map[self.position[0]][self.position[1]]
			self.map[self.position[0]][self.position[1]] = self.map[x][y]
			self.map[x][y] = tmp

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