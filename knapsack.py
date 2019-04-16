#!/usr/local/bin/python3


def knapsack_f(x,y,z,s):
	all_results = []
	for i in range(10):
		for j in range(10):
			for k in range(10):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	return all_results

def knapsack_g(x,y,z,s):
	all_results = []
	for i in range(int(s/x) + 1):
		for j in range(int(s/y) + 1):
			for k in range(int(s/z) + 1):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	return all_results

def knapsack_h(x,y,z,s):
	all_results = []
	for i in range(1,10):
		for j in range(1,10):
			for k in range(1,10):
				total = i * x + j * y + k * z
				if (total <= s):
					all_results.append([i,j,k,total])
	all_results.sort(key = lambda x: x[3], reverse = True)
	return all_results



if __name__ == '__main__':
	print(knapsack_f(17,25,43,233)[0])
	print(knapsack_f(31,41,52,666)[0])
	print(knapsack_f(27,42,51,899)[0])
	print()
	print(knapsack_g(17,25,43,233)[0])
	print(knapsack_g(31,41,52,666)[0])
	print(knapsack_g(27,42,51,899)[0])
	print()
	print(knapsack_h(17,25,43,233)[0])
	print(knapsack_h(31,41,52,666)[0])
	print(knapsack_h(27,42,51,899)[0])


