class Seeker:
	def __init__(self, num_hiders_left, position):
		self.num_hiders_left = num_hiders_left
		self.position = position
	
	def Move(self, DIR):
		x, y = self.position
		x += DIR[0]
		y += DIR[1]
		self.position = (x, y)
	
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