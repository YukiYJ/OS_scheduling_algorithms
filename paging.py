#!/usr/local/bin/python3

number_of_frame = 4
number_of_pages = 6
access_sequence = [1,2,0,1,4,5,3,1,2,5,1,2,1,2,3,2,1,0,1,2,3,0,2,3]
#access_sequence = [1,2,0,1,4,1,5,3,1,2,5,1,2,1,2,3,2,1,0,1,2,3,0,2,3]
page_table = [None for i in range(number_of_frame)]
fault_count = 0

def FIFO():
	global fault_count
	global page_table
	fault_count = 0
	print("#" + str(0) + "\t" + str(page_table))
	for i in range(len(access_sequence)):
		fault_flag = False
		if access_sequence[i] in page_table:
			pass
		else: # fault
			fault_flag = True
			fault_count += 1
			page_table.pop(0)
			page_table.append(access_sequence[i])
		print("#" + str(i+1) + "\t" + str(page_table),end="")
		if fault_flag:
			print("   <" + str(access_sequence[i]))
		else:
			print("    " + str(access_sequence[i]))
	print("Page faults: " + str(fault_count))

def LRU():
	global fault_count
	global page_table
	fault_count = 0
	print("#" + str(0) + "\t" + str(page_table))
	for i in range(len(access_sequence)):
		fault_flag = False
		if access_sequence[i] in page_table:
			page_table = [page_table.pop(page_table.index(access_sequence[i]))] + page_table
		else: # fault
			fault_flag = True
			fault_count += 1
			page_table.pop(-1)
			page_table = [access_sequence[i]] + page_table
		print("#" + str(i+1) + "\t" + str(page_table),end="")
		if fault_flag:
			print("   <" + str(access_sequence[i]))
		else:
			print("    " + str(access_sequence[i]))

	print("Page faults: " + str(fault_count))

def find_most_far_away(sequence, start, page_table):
	max_distance = None
	most_far_away = None
	for page_number in page_table:
		if (page_number == None):
			return None
		i = start + 1
		distance = 0
		while(i < len(sequence)):
			distance += 1
			i += 1
			if sequence[i-1] == page_number:
				break

		if (max_distance == None) or (distance > max_distance):
			max_distance = distance
			most_far_away = page_number
	return most_far_away



def optimal():
	global page_table
	global fault_count
	print("#" + str(0) + "\t" + str(page_table))

	for i in range(len(access_sequence)):
		fault_flag = False
		if access_sequence[i] in page_table:
			pass
		else: # fault
			fault_flag = True
			fault_count += 1
			most_far_away = find_most_far_away(access_sequence,i,page_table)
			page_table[page_table.index(most_far_away)] = access_sequence[i]

		print("#" + str(i+1) + "\t" + str(page_table),end="")
		if fault_flag:
			print("   <" + str(access_sequence[i]))
		else:
			print("    " + str(access_sequence[i]))
	print("Page faults: " + str(fault_count))




if __name__ == '__main__':
	#FIFO()
	#LRU()
	optimal()
	
