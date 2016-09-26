from random import uniform
from math import sqrt
from time import time

number_of_darts = 200000
number_of_darts_in_circle = 0
start_time = time()

for n in range(number_of_darts):
    x,y = uniform(0,1), uniform(0,1)
    if sqrt((x - 0.5)**2 + (y - 0.5)**2) <= 0.5:
            number_of_darts_in_circle +=1
end_time = time()

execution_time = end_time - start_time

pi_approx = 4 * number_of_darts_in_circle / float(number_of_darts)

print "Pi Approximation: ", pi_approx
print "Number of Darts: ", number_of_darts
print "Execution Time (s): ", execution_time
print "Darts Thrown per Second: ", number_of_darts/execution_time

