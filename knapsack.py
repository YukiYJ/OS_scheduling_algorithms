#!/usr/local/bin/python3


def knapsack_f():
	x = 17
	y = 25
	z = 43
	s = 233
	all_results = []
	for i in range(10):
		for j in range(10):
			for k in range(10):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	print(all_results)

def knapsack_g():
	x = 17
	y = 25
	z = 43
	s = 233
	all_results = []
	for i in range(int(s/x) + 1):
		for j in range(int(s/y) + 1):
			for k in range(int(s/z) + 1):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	print(all_results)

def knapsack_h():
	x = 17
	y = 25
	z = 43
	s = 233
	all_results = []
	for i in range(1,10):
		for j in range(1,10):
			for k in range(1,10):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	print(all_results)	



if __name__ == '__main__':
	knapsack_h()