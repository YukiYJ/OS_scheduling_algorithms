#!/usr/local/bin/python3

from hole import *
from asyncio import Queue

rejected = []
total = 0
jobs = []
holes = []
segments = []
logical_addresses = [(0,303),(1,384),(2,77),(3,789),(4,123),(5,99),(6,88)]

def init():
	global total
	total = 1000
	holes = []
	arrival_queue = []
	global rejected
	rejected = []
	holes.append(Hole(1,321))
	holes.append(Hole(2,222))
	holes.append(Hole(3,123))

	arrival_queue.append(Job(1,77))
	arrival_queue.append(Job(2,33))
	arrival_queue.append(Job(3,81))
	arrival_queue.append(Job(4,62))
	arrival_queue.append(Job(5,70))
	arrival_queue.append(Job(6,21))
	arrival_queue.append(Job(7,99))
	arrival_queue.append(Job(8,59))
	arrival_queue.append(Job(9,81))
	arrival_queue.append(Job(10,72))
	arrival_queue.append(Job(11,19))
	arrival_queue.append(Job(12,50))
	
	"""
	# For testing:
	holes.append(Hole(1,200))
	holes.append(Hole(2,400))
	holes.append(Hole(3,600))
	holes.append(Hole(4,300))

	arrival_queue.append(Job(1,280))
	arrival_queue.append(Job(2,180))
	arrival_queue.append(Job(3,320))
	arrival_queue.append(Job(4,400))
	arrival_queue.append(Job(5,120))
	arrival_queue.append(Job(6,160))
	"""

	return holes,arrival_queue

def segment_compare(a,b):
	if a.base <= b.base:
		return -1
	elif a.base > b.base:
		return 1

def segment_init():
	global total
	global segments
	global holes
	global jobs
	jobs = []
	holes = []
	segments = []

	total = 8192

	segments.append(Segment(0,2432,304))
	segments.append(Segment(1,1111,456))
	segments.append(Segment(2,4334,987))
	segments.append(Segment(3,5678,321))
	segments.append(Segment(4,3901,135))
	segments.append(Segment(5,3011,345))
	segments.append(Segment(6,0,1111)) # OS reserved
	segments.append(Segment(7,6789,1403)) # OS reserved
	segments = sorted(segments,key = compare_wrapper(segment_compare))

	for i in range(len(segments) - 1):
		holes.append(Hole(i,segments[i+1].base - (segments[i].base + segments[i].limit)))
		holes[i].base = segments[i].base + segments[i].limit

	jobs.append(Job(0,212))
	jobs.append(Job(1,388))
	jobs.append(Job(2,93))
	# jobs.append(Job(3,987)) # Omit the shared segment
	jobs.append(Job(4,281))
	jobs.append(Job(5,456))
	jobs.append(Job(6,99))


def remaining_space_compare(a,b):
	if a.rem_space < b.rem_space:
		return -1
	elif a.rem_space > b.rem_space:
		return 1
	else:
		if a.id <= b.id:
			return -1
		else:
			return 1


def compare_wrapper(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def print_result():
	global total
	used = 0
	for i in range(len(holes)):
		used += holes[i].size - holes[i].rem_space
		print("Hole \\#" + str(holes[i].id) + ": " ,end="",)
		for job in holes[i].jobs:
			print(str(job.id) + " ",end="")
		print( "("+ str(holes[i].rem_space) + " out of " + str(holes[i].size) + " remaining) \\\\")
	print("Rejected: ",end="")
	for job in rejected:
		print(str(job.id) + " ",end="")
	print("\\\\")
	used += total - sum(h.size for h in holes)
	print("Used: " + str(used) + "  Total: " + str(total) + "  " + str(round(100. * used / total,1)) + "\\%\\\\")

def print_jobs():
	for i in range(len(jobs)):
		print("#" + str(jobs[i].id) + " size: " + str(jobs[i].size))

def first_fit(holes,jobs):
	for i in range(len(jobs)):
		fit_flag = False
		for h in holes:
			if (h.rem_space >= jobs[i].size):
				temp = jobs[i]
				# print(str(logical_addresses[temp.id]) + " @" + str(logical_addresses[temp.id][1] + h.base + h.size - h.rem_space))
				print(str(temp.id) + " & " + str(h.base + h.size - h.rem_space) + " & " + str(temp.size) + "\\\\")
				h.rem_space -= jobs[i].size
				h.jobs.append(jobs[i])
				fit_flag = True
				break
		if (fit_flag == False):
			rejected.append(jobs[i])

def best_fit(holes,jobs):
	for i in range(len(jobs)):
		holes = sorted(holes, key = compare_wrapper(remaining_space_compare))

		fit_flag = False
		for h in holes:
			if (h.rem_space >= jobs[i].size):
				temp = jobs[i]
				#print(str(logical_addresses[temp.id]) + " @" + str(logical_addresses[temp.id][1] + h.base + h.size - h.rem_space))
				print(str(temp.id) + " & " + str(h.base + h.size - h.rem_space) + " & " + str(temp.size) + "\\\\")
				h.rem_space -= jobs[i].size
				h.jobs.append(jobs[i])
				fit_flag = True
				break
		if (fit_flag == False):
			rejected.append(jobs[i])

def worst_fit(holes,jobs):
	for i in range(len(jobs)):
		holes = sorted(holes, key = compare_wrapper(remaining_space_compare),reverse = True)

		fit_flag = False
		for h in holes:
			if (h.rem_space >= jobs[i].size):
				temp = jobs[i]
				#print(str(logical_addresses[temp.id]) + " @" + str(logical_addresses[temp.id][1] + h.base + h.size - h.rem_space))
				print(str(temp.id) + " & " + str(h.base + h.size - h.rem_space) + " & " + str(temp.size) + "\\\\")
				h.rem_space -= jobs[i].size
				h.jobs.append(jobs[i])
				fit_flag = True
				break
		if (fit_flag == False):
			rejected.append(jobs[i])

def print_hole_info():
	for i in range(len(holes)):
		print("Hole #" + str(holes[i].id) + " Base: " + str(holes[i].base) + " Size: " + str(holes[i].size))

if __name__ == '__main__':
	# For question 3
	print("First:")
	segment_init()
	first_fit(holes,jobs)
	print_result()
	print_hole_info()
	print("====================================================")
	print("Best:")
	segment_init()
	best_fit(holes,jobs)
	print_result()
	print_hole_info()
	print("====================================================")
	print("Worst:")
	segment_init()
	worst_fit(holes,jobs)
	print_result()
	print_hole_info()
	print("====================================================")
	"""
	# For question 2:
	holes, jobs = init()
	print_jobs()
	print("First:")
	first_fit(holes,jobs)
	print_result()
	print("====================================================")
	holes, arrival_queue = init()
	print("Best:")
	best_fit(holes,jobs)
	print_result()
	print("====================================================")
	holes, arrival_queue = init()
	print("Worst:")
	worst_fit(holes,jobs)
	print_result()
	"""
	# Optimal:
	# 57 excess cannot be satisfied, is it possible to leave out just the size 59 job?