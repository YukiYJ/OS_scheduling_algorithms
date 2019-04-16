#!/usr/local/bin/python3

number_of_frame = 3
number_of_pages = 6
access_sequence = [1,2,0,1,4,5,3,1,2,5,1,2,1,2,3,2,1,0,1,2,3,0,2,3]
page_table = [-1 for i in range(number_of_frame)]
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
			print("   <")
		else:
			print()
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
			print("   <")
		else:
			print()

	print("Page faults: " + str(fault_count))


if __name__ == '__main__':
	# LRU()
	FIFO()
