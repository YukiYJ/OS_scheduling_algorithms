class Hole:
	def __init__(self,id,size):
		self.id = id
		self.size = size
		self.rem_space = size
		self.jobs = []
		self.base = 0

class Job:
	def __init__(self,id,size):
		self.id = id
		self.size = size

class Segment:
	def __init__(self,id,base,limit):
		self.id = id
		self.base = base
		self.limit = limit