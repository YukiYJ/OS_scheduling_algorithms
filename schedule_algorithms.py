#!/usr/local/bin/python3

from event import *
from asyncio import Queue

schedule = []

def init():
	
	arrival_queue = []
	"""
	arrival_queue.append(Event(1,10,0,3))
	arrival_queue.append(Event(2,8,1,1))
	arrival_queue.append(Event(3,4,3,6))
	arrival_queue.append(Event(4,8,6,8))
	arrival_queue.append(Event(5,10,10,4))
	"""
	# For testing:
	"""
	arrival_queue.append(Event(1,8,0,5))
	arrival_queue.append(Event(2,5,1,7))
	arrival_queue.append(Event(3,3,2,2))
	arrival_queue.append(Event(4,1,3,8))
	arrival_queue.append(Event(5,7,4,4))
	"""

	arrival_queue.append(Event(1,9,0,4))
	arrival_queue.append(Event(2,5,1,7))
	arrival_queue.append(Event(3,2,2,2))
	arrival_queue.append(Event(4,3,3,7))
	arrival_queue.append(Event(5,6,4,4))
	arrival_queue.sort(key = lambda x: x.arrival_t)
	return arrival_queue

def remaining_time_compare(a,b):
	if a.burst_t < b.burst_t:
		return -1
	elif a.burst_t > b.burst_t:
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

def print_result(arrival_queue):
	decision_count = 0
	print("Total time: " + str(len(schedule)))
	for i in range(len(schedule)):
		if (schedule[i] == -1):
			print("_",end="")
		else:
			print(schedule[i],end="")
		if (i+1) % 5 == 0:
			print(" ",end="")
	print()
	for i in range(len(schedule)-1):
		if (schedule[i+1] != schedule[i]):
			print("^",end="")
			decision_count += 1
		else:
			print(" ",end="")
		if (i+1) % 5 == 0:
			print(" ",end="")
	print(" " + str(decision_count) + " decisions")
	print()

	wait_list = []
	tr_list = []
	resp_list = []

	print("Pid\tBurst\tArr\tPrior\tWait\tTR\tResp\tInteractivity")
	for i in range(len(arrival_queue)):
		event = arrival_queue[i]
		last = len(schedule) - 1
		while(True):
			if schedule[last] == event.id:
				break
			last -= 1
		tr = last - event.arrival_t + 1
		wait = tr - event._duration_

		progress = 0
		index = 0
		while (progress < event._duration_ / 2.):
			if (schedule[index] == event.id):
				progress += 1
			index += 1
		if (event._duration_ % 2 != 0):
			resp = index - 0.5
		else:
			resp = index
		resp = resp - event.arrival_t

		wait_list.append(wait)
		tr_list.append(tr)
		resp_list.append(resp)

		print(str(arrival_queue[i].id)+"\t"+str(arrival_queue[i]._duration_)+"\t"+str(arrival_queue[i].arrival_t),end="")
		print("\t"+str(arrival_queue[i].priority)+"\t"+str(wait)+"\t"+str(tr)+"\t"+str(resp)+ "\t" + str(float(event._duration_ + 1)/tr))
	print("Avg." + "\t\t\t\t" + str(sum(wait_list)/len(wait_list)) + "\t" + str(sum(tr_list)/len(tr_list)) + "\t" + str(sum(resp_list)/len(resp_list)))



# This implementation assumes the newly arrived task
# comes before the finishing task
def RR(arrival_queue,q): # q stands for quantum
	current_t = 0
	arrival_queue_head = 0
	run_queue = []

	already_run = 0
	while (True):
		if arrival_queue_head == len(arrival_queue) and len(run_queue) == 0:
			break
		if arrival_queue_head < len(arrival_queue) and current_t >= arrival_queue[arrival_queue_head].arrival_t:
			run_queue.append(arrival_queue[arrival_queue_head])
			arrival_queue_head+=1
		current_t+=1
		if (len(run_queue) == 0):
			schedule.append(-1)
		else:
			if (already_run < q):
				schedule.append(run_queue[0].id)
				run_queue[0].burst_t -= 1
				already_run += 1
				if (run_queue[0].burst_t == 0):
					already_run = 0
					run_queue.pop(0)
					continue
				if (already_run == q):
					already_run = 0
					run_queue.append(run_queue.pop(0))
				
	return schedule

def SRT(arrival_queue):
	current_t = 0
	arrival_queue_head = 0
	run_queue = []
	while (True):
		if arrival_queue_head < len(arrival_queue) and current_t >= arrival_queue[arrival_queue_head].arrival_t:
			run_queue.append(arrival_queue[arrival_queue_head])
			run_queue = sorted(run_queue, key = compare_wrapper(remaining_time_compare))
			arrival_queue_head+=1
		if (len(run_queue) == 0 ):
			schedule.append(-1)
		else:
			schedule.append(run_queue[0].id)
			run_queue[0].burst_t -= 1
			if (run_queue[0].burst_t == 0):
				run_queue.pop(0)
		current_t+=1
		
		if arrival_queue_head == len(arrival_queue) and len(run_queue) == 0:
			break
	return schedule

def priority_with_premption(arrival_queue,option):
	current_t = 0
	arrival_queue_head = 0
	run_queue = []
	if option == "linux":
		reverse_flag = False
	elif option == "win":
		reverse_flag = True

	while (True):
		if arrival_queue_head < len(arrival_queue) and current_t >= arrival_queue[arrival_queue_head].arrival_t:
			run_queue.append(arrival_queue[arrival_queue_head])
			run_queue = sorted(run_queue, key = lambda x: x.priority, reverse = reverse_flag)
			arrival_queue_head+=1
		if (len(run_queue) == 0):
			schedule.append(-1)
		else:
			schedule.append(run_queue[0].id)
			run_queue[0].burst_t -= 1
			if (run_queue[0].burst_t == 0):
				run_queue.pop(0)
		current_t+=1
		
		if arrival_queue_head == len(arrival_queue) and len(run_queue) == 0:
			break
	return schedule

if __name__ == '__main__':
	arrival_queue = init()
	RR(arrival_queue,3)
	print_result(arrival_queue)

