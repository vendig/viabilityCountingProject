# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 13:56:48 2017

@author: User
"""


import numpy as np
import scipy.io as sio
import math
import time
from scipy import signal
from viability import Viability

#generator of data is imported from this file
#it mimic the behaviour of an impedance device
import genDataVendi
#for printing nicely a dictionary
import pprint




COEF_LOWPASS_FILE='C:\\Users\\User\\Documents\\PYTHON\\PROJECTS_1\\project_repo\\numlowpass_filter.csv'


#change a directory of a lowpass filter coefficients inside
#getCoefLowpass() function!!!!
#instead of COEF_LOWPASS_FILE write another directory of coefficients

def getCoefLowpass():
    """function reads the coefficients from file `COEF_LOWPASS_FILE`
       and returns an np.array of coefficients.

       Args:
           none

       Returns:
           np.array(coefficients)
    """
    b = list()
    with open (COEF_LOWPASS_FILE) as CSV:
    	for line in CSV:
    		line = line.strip()
    		line = line.split(",")

    		for elem in line:
    			elem = float(elem)
    			b.append(elem)
    coef_lowpass = np.array(b)
    return coef_lowpass



def batchUpdateDict(num_iterations, num_demodulators, num_chambers,
                    arraySize, maxElectrodePair, maxDemod, Viability_test1):
    """function randomly generates data for different demodulators, update and returns
       a dictionary named ´dictViab´.

       Args:
           * num_iteartions: number of cycles of data generated for each module
           * num_demodulators: number of demodulators for which data are
                                generated. etc. if demodulators number 3 and 5
                                are used, then it is written as num_demodulators = [3, 5],
                                order is not important.
           * num_chambers: number of chambers. Example can be the same as for num_demodulators.
           * Viability_test1: an instance created from a class Viability.

       Returns:
           * an updated dictionary named ´dictViab´
    """

    for i in range(num_iterations):


        #generate data and returns ´data´ dictionary
        #generator is imported from a file named ´genDataVendi´
        #when using it change a file directory
        data = genDataVendi.DataGen(arraySize, maxElectrodePair, maxDemod)


        #acessing data from a dictionary named ´data´
        for key in data.keys():
            data_x = data[key]['x']
            data_y = data[key]['y']
            data_timestp = data[key]['timestamp']
            data_diod = data[key]['dio']




            for n in num_demodulators:
              #updating a dictionary named ´dictViab´ with information about
              #diod, timestamp, ePair, viabR, countR, time
              Viability_test1.updateDict(data_diod=data_diod, data_timestp=data_timestp,
                                       demodulator="demodulator" + str(n), data_x=data_x,
                                       data_y=data_y,
                                       clockbase=210e+6)


    return Viability_test1.dictViab



if __name__ == '__main__':


    #choosing a number of demodulators and chambers
    num_demodulators = [0]
    num_chambers = [1, 2]
    #determining which electrodes should be activated
    maxElectrodePair = [3, 2, 5]
    #how long are arrays generated with a generator at one iteration
    arraySize = 100
    #how many times generator is called
    num_iterations = 100


    #get the coefficients
    coef_lowpass = getCoefLowpass()

    # #creating instance of a class and initialization of a dictionary
    Viability_test1 = Viability()
    #initialization of a temporar dictionary
    Viability_test1.initDict(numChamber=num_chambers,
                             numModul=num_demodulators)

    #initialization of a constant dictionary
    Viability_test1.DataForDisplaying(numChamber=num_chambers, numModul=num_demodulators)

    # #iterating over ´data, updating and returning dictionary named ´dictViab´.
    Viability_test1.dictViab = batchUpdateDict(num_iterations, num_demodulators,
                                               num_chambers, arraySize,
                                              maxElectrodePair, maxDemod=num_demodulators,
                                              Viability_test1=Viability_test1)
                                              #Viability_test1 is an instance of a class

    #before calculating HPF, PSD and peak detection,
    #zeros should be removed from the endings of the array inside a dictionary ´dictViab´
    Viability_test1.removingZeros(numChamber=num_chambers)

    #peaks of a data inside a key "countR" are detected and stored inside a key "count",
    Viability_test1.peakDataStoringDict(mph=None, mpd=1, threshold=0, edge='rising',
                                    kpsh=False, valley=False, show=False,
                                    ax=None, numChamber=num_chambers)

    #data are filtered
    Viability_test1.getHPFData(coef_lowpass=coef_lowpass, numChamber=num_chambers)

    #PSD number is calculated
    Viability_test1.getPSDNum(numChamber=num_chambers)

    #PSD number, count (number of peaks detected) and time are stored inside a constant
    #dictionary named ´displayingData´
    Viability_test1.storingData(numChamber=num_chambers)

    #temporary dictionay is printed
    pp = pprint.PrettyPrinter(indent=2)
    print(pp.pprint(Viability_test1.dictViab))

    #after a cycle a temporar dictionary is emptied of all data
    Viability_test1.dictViab = {}

    #a constant dicitonary is printed
    print(pp.pprint(Viability_test1.displayingData))

