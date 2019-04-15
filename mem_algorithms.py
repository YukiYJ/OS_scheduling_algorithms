#!/usr/local/bin/python3

from hole import *
from asyncio import Queue

rejected = []


def init():
	
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
	arrival_queue.append(Job(9,80))
	arrival_queue.append(Job(10,72))
	arrival_queue.append(Job(11,19))
	arrival_queue.append(Job(12,50))

	return holes,arrival_queue

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
	total = 0
	used = 0

	for i in range(len(holes)):
		used += holes[i].size - holes[i].rem_space
		total += holes[i].size
		print("Hole #" + str(holes[i].id) + ": " + str(holes[i].rem_space) + "/" + str(holes[i].size))
		for job in holes[i].jobs:
			print(str(job.id) + " ",end="")
		print()
		print("Rejected:")
	for job in rejected:
		print(str(job.id) + " ",end="")
	print()
	print("Used: " + str(used) + "  Total: " + str(total) + "  " + str(round(100. * used / total,1)) + "%")

def first_fit(holes,jobs):
	for i in range(len(jobs)):
		fit_flag = False
		for h in holes:
			if (h.rem_space >= jobs[i].size):
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
				h.rem_space -= jobs[i].size
				h.jobs.append(jobs[i])
				fit_flag = True
				break
		if (fit_flag == False):
			rejected.append(jobs[i])

if __name__ == '__main__':
	holes, arrival_queue = init()
	print("First:")
	first_fit(holes,arrival_queue)
	print_result()
	print("====================================================")
	holes, arrival_queue = init()
	print("Best:")
	best_fit(holes,arrival_queue)
	print_result()
	print("====================================================")
	holes, arrival_queue = init()
	print("Worst:")
	worst_fit(holes,arrival_queue)
	print_result()