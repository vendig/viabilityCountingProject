import numpy as np
import random
import scipy as sp


def DataGen(arraySize, maxElectrodePair=list(), maxDemod=list()):
	"""
	data generator, which generate a diciotnary with
	number of demodulators and chambers chosen by a user.
	"""

	data = {}

	# 1-6 demodulators
	#for demod in range(sp.random.randint(0,maxDemod)):
	for demod in maxDemod:

		key = '/dev10/demods/%s/sample' % demod

		data[key] = {}

		data[key]['x']         = sp.random.random (             arraySize )
		data[key]['y']         = sp.random.random (             arraySize )
		data[key]['frequency'] = sp.random.randint( 100, 50e6 , arraySize )
		data[key]['timestamp'] = sp.random.randint( 0  , 2**31, arraySize )
		data[key]['dio']       = sp.array([int("{0:032b}".format(int("{0:05b}".format(i)[::-1],
        	2)<<20), 2) for i in [maxElectrodePair[random.randint(0, len(maxElectrodePair)-1)] for
			k in range(arraySize)]])

	return data





if __name__ == '__main__':
	#testing a random function
	# electrodePair = [1, 2, 4, 0]
	# arraySize = 3
	# num_to_select = 2

	# print([electrodePair[random.randint(0, len(electrodePair)-1)] for
	# 	i in range(arraySize)])
	data = DataGen(arraySize=5, maxElectrodePair=[2, 4], maxDemod=[0, 3])
	print(data)