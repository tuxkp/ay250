from random import uniform
from math import sqrt
from time import time

number_of_darts = 1000000
mode = "PARALLEL"

def throwRandomDarts(number_of_darts_thrown):
	number_of_darts_in_circle = 0
	for n in range(number_of_darts):
		x,y = uniform(0,1), uniform(0,1)
		if sqrt((x - 0.5)**2 + (y - 0.5)**2) <= 0.5:
			number_of_darts_in_circle += 1
	return number_of_darts_in_circle

def approxPi(number_of_darts_thrown):
	number_of_darts_in_circle = throwRandomDarts(number_of_darts)
	pi_approx = 4 * number_of_darts_in_circle / float(number_of_darts)
	return pi_approx

start_time = time()
pi_approx = approxPi(number_of_darts)
end_time = time()
execution_time = end_time - start_time


if mode == "SERIAL":
	print ("-----------Serial-----------")
	print ("Pi Approximation:", pi_approx)
	print ("Number of Darts:", number_of_darts)
	print ("Execution Time (s):", execution_time)
	print ("Darts Thrown per Second:", number_of_darts/execution_time)


elif mode == "MULTI":
	print ("-----------Multiprocessing-----------")
	from multiprocessing import Pool
	with Pool(5) as p:
		start_time = time()
		pi_approx = p.map(approxPi,[number_of_darts,number_of_darts,number_of_darts,number_of_darts,number_of_darts])
		end_time = time()
		execution_time = end_time - start_time
	print ("Pi Approximation:", pi_approx)
	print ("Number of Darts:", number_of_darts)
	print ("Execution Time (s):", execution_time)
	print ("Darts Thrown per Second:", number_of_darts/execution_time)


elif mode == "PARALLEL":
	print ("-----------ipcluster-----------")
	from ipyparallel import Client
	rc = Client()
	dv = rc[:]
#	results = dv.map_sync(lambda n : approxPi(n), [number_of_darts, number_of_darts,number_of_darts,number_of_darts])
	results = dv.map_sync(2 + 4, range(4))
	print (results)




