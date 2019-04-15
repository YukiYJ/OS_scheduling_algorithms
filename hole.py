class Hole:

	def __init__(self,id,size):
		self.id = id
		self.size = size
		self.rem_space = size
		self.jobs = []		

class Job:
	def __init__(self,id,size):
		self.id = id
		self.size = size
