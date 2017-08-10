
#VERY IMPORTANT!!


#BEFORE USING UNITEST INSIDE A vIABILITY CLASS self.maxChamberLen=5 should be
#UNCOMMENTED AND self.maxChamberLen = self.numMinutes * self.samplingRate * 60
#SHOULD BE COMMENTED!!!!!!!!!



import unittest


import numpy as np
import random
import scipy as sp

from ePair_updateDict import initDict
# from ePair_updateDict import initDict2
from ePair_updateDict import getSliceIndex
from ePair_updateDict import myDictConcat
from ePair_updateDict import updateDict
from viability import Viability
import genDataVendi
#from genDataVendi import DataGen

def areArraysEqual(arr1, arr2):
    '''Compare arrays, also allowing for empty arrays
    '''
    if (len(arr1) != len(arr2)):
        return(False)
    #else lengths the same
    if (len(arr1)==1):
        return(arr1==arr2)
    #otherwise
    return(all(arr1==arr2))


#inspiration from
#https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries

def printDiff(val1, val2):
    print('HEREHEREHEREHEREHEREHEREHEREHEREHERE')
    print('key1:')
    print(val1)
    print('key2:')
    print(val2)

def areGenDictsEqual(dict1, dict2, showDiff=False):
    '''Compare dictionaries, and allow for empty arrays to be compared.

       Dictionaries follow the structure:
            demodulator1:
                "1" : {"x": array([...]), "y": array([...])},
                "2" : {"x": array([...]), "y": array([...])},
                ...
                "n" : {"x": array([...]), "y": array([...])},
            demodulator2:
                etc.
    '''
    if (len(dict1)==len(dict2)):
        #now check keys loop through keys - sorted!
        isTheSame = True
        #showDiff = True
        dict1keys = sorted(list(dict1))
        dict2keys = sorted(list(dict2))
        index = 0
        while (isTheSame) & (index < len(dict1)):
            key1 = dict1keys[index]
            key2 = dict2keys[index]
            if (key1 != key2):
                isTheSame = False

                #if (showDiff):

                    #printDiff(key1, key2)

            else:
                #extract values, for readability
                val1 = dict1[key1]
                val2 = dict2[key2]
                if (type(val1) != type(val2)):
                    #types are not the same

                    isTheSame = False
                    #if (showDiff):
                        #printDiff(val1, val2)

                else:
                    #if types are the same, check if dict
                    if ( isinstance(val1, dict) ):
                        #if dict, use recursion
                        isTheSame = areGenDictsEqual(val1, val2)
                    else:
                        #if not dict
                        #check both are arrays with len attribute
                        if (hasattr(val1, "__len__") != hasattr(val2, "__len__")):
                            #have different len attribute, so False
                            isTheSame = False

                            #if (showDiff):
                                #printDiff(val1, val2)

                        else:
                            #both have OR do not have len attribute
                            if (hasattr(val1, "__len__") == True):
                                #array check
                                #are arrays the same length?
                                if (len(val1) != len(val2)):
                                    isTheSame = False
                                    if (showDiff):
                                        printDiff(val1, val2)
                                        print("Hello")
                                        print(key1, key2)
                                        print(val1, val2)
                                else:
                                    isTheSame = all(val1==val2)
                            else:
                                #not array
                                isTheSame = (val1==val2)

            #increase index
            index = index + 1
        #end of while
        return(isTheSame)
    else:
        if(showDiff):
            printDiff(0, 0)
            print("Hello")
        return(False)





class DictTests(unittest.TestCase):
    def test_areArraysEqual1(self):
        '''Testing `areArraysEqual` function
            Two arrays are equal - should be true
        '''
        arr1 = np.array([0.3, 0.2, 4])
        arr2 = np.array([0.3, 0.2, 4])
        self.assertEqual(areArraysEqual(arr1, arr2), True)


    def test_areArraysEqual2(self):
        '''Testing `areArraysEqual` function
           Two arrays are NOT equal - should be false
        '''
        arr1 = np.array([1, 2, 4])
        arr2 = np.array([1, 2, 3])
        self.assertEqual(areArraysEqual(arr1, arr2), False)


    def test_areArraysEqual3(self):
        '''Testing `areArraysEqual` function
           Two arrays both empty - should be true
        '''
        arr1 = np.array([])
        arr2 = np.array([])
        self.assertEqual(areArraysEqual(arr1, arr2), True)
    #-----------------------------------------------------------------#


    def test_areGenDictsEqual1(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, simple, the same
        '''
        dict1 = {'x': 1, 'y': 2}
        dict2 = {'x': 1, 'y': 2}
        self.assertEqual(areGenDictsEqual(dict1, dict2), True)


    def test_areGenDictsEqual2(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, simple, different
        '''
        dict1 = {'x': 1, 'y': 2}
        dict3 = {'x': 1, 'y': 3}
        self.assertEqual(areGenDictsEqual(dict1, dict3), False)


    def test_areGenDictsEqual3(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, simple, with arrays, the same
        '''
        dict4 = {'x': 1, 'y': np.array([1, 2])}
        dict5 = {'x': 1, 'y': np.array([1, 2])}
        self.assertEqual(areGenDictsEqual(dict4, dict5), True)


    def test_areGenDictsEqual4(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, simple, with arrays, different
        '''
        dict4 = {'x': 1, 'y': np.array([1, 2])}
        dict6 = {'x': 1, 'y': np.array([1, 3])}
        self.assertEqual(areGenDictsEqual(dict4, dict6), False)


    def test_areGenDictsEqual5(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, complex, with subdicts, the same
        '''
        dict7 = {'x': 1, 'y': {'z': 2, 'a': {'b': 4, 'c': 5} }, 'd': 6  }
        dict8 = {'x': 1, 'y': {'z': 2, 'a': {'b': 4, 'c': 5} }, 'd': 6  }
        self.assertEqual(areGenDictsEqual(dict7, dict8), True)


    def test_areGenDictsEqual6(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, complex, with subdicts, different
        '''
        dict7 = {'x': 1, 'y': {'z': 2, 'a': {'b': 4, 'c': 5} }, 'd': 6  }
        dict9 = {'x': 1, 'y': {'z': 2, 'a': {'b': 4, 'c': 7} }, 'd': 6  }
        self.assertEqual(areGenDictsEqual(dict7, dict9), False)


    def test_areGenDictsEqual7(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, complex, with subdicts, the same, with arrays
        '''
        dict10 = {'x': 1, 'y': {'z': 2, 'a': {'b': np.array([7, 8, 9]), 'c': 5} }, 'd': 6  }
        dict11 = {'x': 1, 'y': {'z': 2, 'a': {'b': np.array([7, 8, 9]), 'c': 5} }, 'd': 6  }
        self.assertEqual(areGenDictsEqual(dict10, dict11), True)


    def test_areGenDictsEqual8(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, complex, with subdicts, different, with arrays
        '''
        dict10 = {'x': 1, 'y': {'z': 2, 'a': {'b': np.array([7, 8, 9]), 'c': 5} }, 'd': 6  }
        dict12 = {'x': 1, 'y': {'z': 2, 'a': {'b': np.array([7, 3, 9]), 'c': 5} }, 'd': 6  }
        self.assertEqual(areGenDictsEqual(dict10, dict12), False)


    def test_areGenDictsEqual9(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, one empty array, one not
        '''
        dict21 = {'x': 1, 'y': np.array([])}
        dict22 = {'x': 1, 'y': np.array([1])}
        self.assertEqual(areGenDictsEqual(dict21, dict22), False)


    def test_areGenDictsEqual10(self):
        '''Testing `areGenDictsEqual` function
           Two dicts, both empty arrays
        '''
        dict23 = {'x': 1, 'y': np.array([])}
        dict24 = {'x': 1, 'y': np.array([])}
        self.assertEqual(areGenDictsEqual(dict23, dict24), True)
    #-----------------------------------------------------------------#


    def test_areDemDictsEqual1(self):
        '''Testing `areDemDictsEqual` function
           Two dicts, both empty arrays
        '''
        dict25 = {'dem1': {'1': {'x': np.array([10]), 'y': np.array([])},
            '2': {'x': np.array([8, 8]), 'y': np.array([])},
            '3': {'x': np.array([7]), 'y': np.array([])}}}

        dict26 = {'dem1': {'1': {'x': np.array([10]), 'y': np.array([])},
            '2': {'x': np.array([8, 8]), 'y': np.array([])},
            '3': {'x': np.array([7]), 'y': np.array([])}}}

        #self.assertEqual(areDemDictsEqual(dict25, dict26), True)
        self.assertEqual(areGenDictsEqual(dict25, dict26), True)

    def test_areDemDictsEqual2(self):
        '''Testing `areDemDictsEqual` function
           Two dicts, both empty arrays
           Must return False
           dem1, x, contains 10/nothing
        '''
        dict27 = {'dem1': {'1': {'x': np.array([10]), 'y': np.array([])},
            '2': {'y': np.array([]), 'x': np.array([8, 8])},
            '3': {'x': np.array([7]), 'y': np.array([])}}}

        dict28 = {'dem1': {'1': {'x': np.array([]), 'y': np.array([])},
            '3': {'y': np.array([]), 'x': np.array([7])},
            '2': {'x': np.array([8, 8]), 'y': np.array([])}}}

        #self.assertEqual(areDemDictsEqual(dict27, dict28, show=True), False)
        self.assertEqual(areGenDictsEqual(dict27, dict28), False)


    def test_areDemDictsEqual3(self):
        '''Testing `areDemDictsEqual` function
           Two dicts, both empty arrays
        '''
        dict29 = {'dem1': {'1': {'x': np.array([]), 'y': np.array([])},
            '2': {'x': np.array([]), 'y': np.array([])},
            '3': {'x': np.array([]), 'y': np.array([])}}}

        dict29b = {'dem1': {'1': {'x': np.array([]), 'y': np.array([])},
            '2': {'x': np.array([]), 'y': np.array([])},
            '3': {'x': np.array([]), 'y': np.array([])}}}

        #self.assertEqual(areDemDictsEqual(dict29, dict29b), True)
        self.assertEqual(areGenDictsEqual(dict29, dict29b), True)

    def test_areDemDictsEqual4(self):
        '''Testing `areDemDictsEqual` function
           Two dicts, both empty arrays
        '''
        dict30 = {'dem1': {'1': {'x': np.array([]), 'y': np.array([])},
            '2': {'x': np.array([]), 'y': np.array([])},
            '3': {'x': np.array([]), 'y': np.array([1])}}}

        dict31 = {'dem1': {'1': {'x': np.array([]), 'y': np.array([])},
            '2': {'x': np.array([]), 'y': np.array([])},
            '3': {'x': np.array([]), 'y': np.array([2])}}}

        #self.assertEqual(areDemDictsEqual(dict30, dict31), False)
        self.assertEqual(areGenDictsEqual(dict30, dict31), False)
    #-----------------------------------------------------------------#

class OtherTests(unittest.TestCase):


    def test_initDict4(self):
        """
        testing whether a dictionaries are the same.
        Number of zeros inside array is 5 (changed in a Viability class).
        """

        v = Viability()
        numChamber = 0
        v.initDict(numChamber=[0], numModul=[0])
        data = v.dictViab
        L =5
        dataSoln1 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber + 1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1),
                        "demodullen":np.zeros(1),


                        }
                    }
        #print(v.dictViab["demodulator0"]["chamber0"]["countR"])
        #print("")

        #print(dataSoln1)

        self.assertEqual(areGenDictsEqual(data, dataSoln1), True)
#     #---------------------------------------------------------------

    def test_initDict5(self):
        """
        testing more chambers and demodulators
        """

        v = Viability()
        #adding number of chambers
        numChamber = [0, 1]
        v.initDict(numChamber=[0, 1], numModul=[3, 0])
        data = v.dictViab
        L = 5
        dataSoln2 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },
                        "chamber1": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(max(numChamber) + 1),
                        "chamberlenViabR":np.zeros(max(numChamber) + 1),
                        "chamberlenCountR":np.zeros(max(numChamber) + 1),
                        "demodullen":np.zeros(1),

                        },
                    "demodulator3":

                       {"chamber0": {
                               "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },
                        "chamber1": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(max(numChamber) + 1),
                        "chamberlenViabR":np.zeros(max(numChamber) + 1),
                        "chamberlenCountR":np.zeros(max(numChamber) + 1),
                        "demodullen":np.zeros(1),


                        }
                    }
        #print(v.dictViab)


        #print(dataSoln2)
        self.assertEqual(areGenDictsEqual(data, dataSoln2), True)

#     #--------------------------------------------------------------
    def test_dataForDisplaying(self):
        """
        testing whether dictionary which is permanent is ok
        """

        v = Viability()
        numChamber = [5, 1]
        v.DataForDisplaying(numChamber=[5, 1], numModul=[3, 0])
        data = v.displayingData
        L = 5
        dataSoln3 = {"demodulator0":

                       {"chamber1": {
                                "count":np.array([]),
                                "PSDnum":np.array([]),
                                "time":np.array([])
                                },


                        "chamber5": {
                                "count":np.array([]),
                                "PSDnum":np.array([]),
                                "time":np.array([])
                                }

                        },


                    "demodulator3":

                       {"chamber1": {
                               "count":np.array([]),
                                "PSDnum":np.array([]),
                                "time":np.array([])
                            },
                        "chamber5": {
                                "count":np.array([]),
                                "PSDnum":np.array([]),
                                "time":np.array([])
                            }
                        }
                    }

        self.assertEqual(areGenDictsEqual(data, dataSoln3), True)

#     #----------------------------------------------------------------
    def test_getSliceIndex1(self):
        """
        testing whether slices indexes are working
        """
        v = Viability()
        ePair = np.array([0, 1, 1])

        #run function
        (idx, num) = v.getSliceIndex(ePair)

        #expected result
        idxSoln = [0, 2]
        numSoln = [0, 1]

        bothCorrect  = (  (idx==idxSoln) & (num==numSoln)  )

        #check
        self.assertEqual(bothCorrect, True)
#     #-----------------------------------------------------------
    def test_getSliceIndex2(self):
        """
        testing more complicated examples
        """
        v = Viability()
        ePair = np.array([0, 1, 1, 0, 6, 6, 7])

        #run function
        (idx, num) = v.getSliceIndex(ePair)

        #expected result
        idxSoln = [0, 2, 3, 5, 6]
        numSoln = [0, 1, 0, 6, 7]

        bothCorrect  = (  (idx==idxSoln) & (num==numSoln)  )

        #check
        self.assertEqual(bothCorrect, True)

#     #-------------------------------------------------------------
    def test_insertNumDictData_x(self):
        """
        testing whether insertion of numbers
        inside a dictionary work

        """
        data_x = np.array([1, 2, 2])
        numberChamberList = [0, 2, 1]
        idx1 = 0
        startIndex = 0
        stopIndex = 1
        start = 0
        elem = 0
        L = 5
        numChamber = 0
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictData_x(data_x=data_x,
            demodulator="demodulator0",
            numberChamberList = numberChamberList,
            startIndex=startIndex, idx1 = idx1,
            stopIndex=stopIndex, start=start, elem=elem)



        dataSoln5 = {"demodulator0":

                       {"chamber0": {
                                "x":np.array([1,0, 0, 0, 0]),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber + 1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1),
                        "demodullen":np.zeros(1)

                        }
                    }

        #print(data)
        self.assertEqual(areGenDictsEqual(data, dataSoln5), True)

# #-------------------------------------------------------
    def test_InsertNumDictData_x2(self):
        """
        testing whether insertion of numbers
        inside a dictionary work with different
        start and stop index and start and elem.

        """
        data_x = np.array([1, 2, 2])
        numberChamberList = [1]
        num = [2, 2, 1]
        idx1 = 0
        startIndex = 0
        stopIndex = 2
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        v = Viability()
        v.initDict(numChamber= [1] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictData_x(data_x=data_x,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, startIndex=startIndex,
            stopIndex=stopIndex, start=start, elem=elem)



        dataSoln6 = {"demodulator0":

                       {"chamber1": {
                                "x":np.array([2,2, 0, 0, 0]),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber + 1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1),
                        "demodullen":np.zeros(1)

                        }
                    }


        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# #--------------------------------------------------------
    def test_insertNumDictData_y1(self):
        """
        testing whether insertion of numbers
        inside a dictionary work

        """
        data_y = np.array([1, 2, 2])
        numChamberList = [1]
        num = [2, 2, 1]
        idx1 = 0
        startIndex = 0
        stopIndex = 2
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        v = Viability()
        v.initDict(numChamber= [1] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictData_y(data_y=data_y,
            demodulator="demodulator0", numberChamberList=numChamberList,
            idx1=idx1, startIndex=startIndex,
            stopIndex=stopIndex, start=start, elem=elem)



        dataSoln7 = {"demodulator0":

                       {"chamber1": {
                                "x":np.zeros(L),
                                "y":np.array([2,2, 0, 0, 0]),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.zeros(L),
                                "time":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber + 1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1),
                        "demodullen":np.zeros(1)

                        }
                    }


        self.assertEqual(areGenDictsEqual(data, dataSoln7), True)

# #------------------------------------------------------------------

    def test_updateChamberLenData_x1(self):
        """
        testing whether key "chamberlen" is correctly updated
        """
        data_x = np.array([1, 2, 2])
        numChamberList = [1]
        num = [2, 2, 1]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        v = Viability()
        v.initDict(numChamber= [1] , numModul=[0])
        data = v.dictViab
        v.updateChamberLenData_x(data_x=data_x,
                demodulator="demodulator0", numberChamberList=numChamberList,
                idx1=idx1, start=start, elem=elem)


        dataSoln7 = {"demodulator0":

                           {"chamber1": {
                                    "x":np.array([2,2, 0, 0, 0]),
                                    "y":np.zeros(L),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.zeros(L),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                                },


                            "diod": np.zeros(L),
                            "ePair": np.zeros(L),
                            "timestamp": np.zeros(L),
                            "chamberlen":np.array([0, 2]),
                            "demodullen":np.zeros(1),
                            "chamberlenViabR":np.zeros(numChamber + 1),
                            "chamberlenCountR":np.zeros(numChamber + 1),


                            }
                        }

        #print(data)
        self.assertEqual(areGenDictsEqual(data, dataSoln7), True)

# -----------------------------------------------------------------------
    def test_updateChamberLen(self):

        """
        Function test a function ´updateChamberLen´ with
        data_x, data_y, data_timestp
        """
        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        data_timestp = np.array([0, 10, 5])
        num = [9, 2, 1]
        numChamberList = [3]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 3
        v = Viability()
        v.initDict(numChamber= [3] , numModul=[0])
        data = v.dictViab
        v.updateChamberLen(data_x=data_x, data_y=data_y, data_timestp = data_timestp,
                demodulator="demodulator0", numberChamberList=numChamberList,
                idx1=idx1, start=start, elem=elem, clockbase=2)


        dataSoln7 = {"demodulator0":

                           {"chamber3": {
                                    "x":np.array([2,2, 0, 0, 0]),
                                    "y":np.array([2,4, 0, 0, 0]),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.array([5, 2.5, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                                },


                            "diod": np.zeros(L),
                            "ePair": np.zeros(L),
                            "timestamp": np.array([0,0, 0, 0, 0]),
                            "chamberlen":np.array([0, 0, 0, 2]),
                            "demodullen":np.zeros(1),
                            "chamberlenViabR":np.zeros(numChamber + 1),
                            "chamberlenCountR":np.zeros(numChamber + 1),



                            }
                        }
        #print(data)

        self.assertEqual(areGenDictsEqual(data, dataSoln7), True)
    #--------------------------------------------------------------

    def test_getR(self):
        """
        testing whether a conversion of data_x and data_y
        to R(modul of impedance) works
        """
        v = Viability()
        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        start = 1
        elem = 2
        R = v.getR(data_x, data_y, elem, start, multiplier=1000)

        RSoln = np.array([(2*np.sqrt(2)*1000), np.sqrt(20)*1000])

        self.assertEqual(areArraysEqual(R, RSoln), True)

# #----------------------------------------------------------

    def test_getTime(self):
        """
        test whether a timestamp conversion to time
        is correct
        """
        data_timestp = np.array([1, 2, 3])
        v = Viability()

        #initializing a dictionary
        v.initDict(numChamber= [3] , numModul=[0])

        #inserting in a ´demodulator0´ inside a key "timestamp"
        #on a first position a number
        v.dictViab["demodulator0"]["timestamp"][0] = 2
        time = v.getTime(data_timestp, demodulator="demodulator0",
                     clockbase=2)

        #writing what result is expected
        TimeSoln = np.array([-0.5, 0, 0.5])

        self.assertEqual(areArraysEqual(time, TimeSoln), True)


#     #---------------------------------------------------------
    def test_insertNumDict(self):
        """
        testing whether ´data_x´, ´data_y´ and ´data_timestp´
        are correctly inserted into a dicitonary and time is
        correctly calculated as well as viabR
        """

        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        data_timestp = np.array([1, 2, 3])
        num = [2, 2, 1]
        numChamberList = [1]
        idx1 = 0
        startIndex = 0
        stopIndex = 2
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        v = Viability()
        v.initDict(numChamber= [1] , numModul=[0])
        v.dictViab["demodulator0"]["timestamp"][0] = 2
        data = v.dictViab
        v.InsertNumDict(data_x=data_x, data_y=data_y,
            data_timestp = data_timestp,
            demodulator="demodulator0", numberChamberList=numChamberList,
            idx1=idx1, startIndex=startIndex,
            stopIndex=stopIndex, start=start, elem=elem, clockbase=2)



        dataSoln6 = {"demodulator0":

                       {"chamber1": {
                                "x":np.array([2, 2, 0, 0, 0]),
                                "y":np.array([2, 4, 0, 0, 0]),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([0, 0, 0, 0, 0]),
                                "time":np.array([0, 0.5, 0, 0, 0]),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)

                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.array([2,0, 0, 0, 0]),
                        "chamberlen":np.array([0, 0]),
                        "demodullen":np.zeros(1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)



                        }
                    }

        #print(data)

        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# #     #-----------------------------------------------------------------------------
    def test_updateChamberLen1(self):
        """
        testing whether data are inserted correctly into a dictionary
        and if chamberlen is updated correctly
        """
        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        data_timestp = np.array([1, 2, 3])
        num = [2, 2, 1]
        numChamberList= [1]
        idx1 = 0
        startIndex = 0
        stopIndex = 2
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        v = Viability()
        v.initDict(numChamber= [1] , numModul=[0])
        v.dictViab["demodulator0"]["timestamp"][0] = 2
        data = v.dictViab
        v.updateChamberLen(data_x=data_x, data_y=data_y,
            data_timestp = data_timestp,
            demodulator="demodulator0", numberChamberList=numChamberList,
            idx1=idx1, start=start, elem=elem, clockbase=2)

        dataSoln7 = {"demodulator0":

                       {"chamber1": {
                                "x":np.array([2, 2, 0, 0, 0]),
                                "y":np.array([2, 4, 0, 0, 0]),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([0, 0, 0, 0, 0]),
                                "time":np.array([0, 0.5, 0, 0, 0]),
                                "PSDnum":np.array([]),
                                "countR":np.zeros(L),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.array([2,0, 0, 0, 0]),
                        "chamberlen":np.array([0, 2]),
                        "demodullen":np.zeros(1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)

                        }
                    }



        self.assertEqual(areGenDictsEqual(data, dataSoln7), True)

# # #-----------------------------------------------------------------
    def test_insertNumDictModulTimestamp(self):
        """
        checking whether timestamp is inserted correctly inside a dictionary.
        Be careful - ´data_timestp´ is not sliced.
        """
        data_timestp = np.array([2, 3])
        num = [4, 2, 1]
        numChamberList = [2]
        idx1 = 0
        startIndexDemodul = 0
        stopIndexDemodul = 2
        start = 1
        elem = 2
        L = 5
        numChamber = 2
        v = Viability()
        v.initDict(numChamber= [2] , numModul=[0, 1])
        data = v.dictViab
        v.insertNumDictModulTimestamp(data_timestp=data_timestp,
                        startIndexDemodul=startIndexDemodul,
                        stopIndexDemodul=stopIndexDemodul,
                        demodulator="demodulator1")

        dataSoln8 = {"demodulator0":

                       {"chamber2": {
                                "x":np.array([0,0, 0, 0, 0]),
                                    "y":np.zeros(L),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.zeros(L),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.array([0, 0, 0, 0, 0]),
                        "chamberlen":np.array([0, 0, 0]),
                        "demodullen":np.zeros(1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)

                        },
                    "demodulator1":

                       {"chamber2": {
                                "x":np.array([0, 0, 0, 0, 0]),
                                    "y":np.zeros(L),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.zeros(L),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.array([2, 3, 0, 0, 0]),
                        "chamberlen":np.array([0, 0, 0]),
                        "demodullen":np.zeros(1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)

                        }
                    }
        #print(data)
        self.assertEqual(areGenDictsEqual(data, dataSoln8), True)

# # #-----------------------------------------------------------------
    def test_insertNumInDemodul(self):
        """
        testing whether ´diod´, ´timestamp´and ´ePair´ are correctly
        inserted into a dictionary.
        """
        data_timestp = np.array([2, 3])
        data_diod = np.array([0, 1])
        data_epair = np.array([5, 10])

        L = 5
        numChamber = 2
        v = Viability()
        v.initDict(numChamber= [2] , numModul=[0, 1])
        data = v.dictViab
        v.insertNumInDemodul(data_timestp=data_timestp, data_diod=data_diod,
                            data_epair=data_epair,
                            demodulator="demodulator1")

        dataSoln9 = {"demodulator0":

                       {"chamber2": {
                                "x":np.array([0, 0, 0, 0, 0]),
                                    "y":np.zeros(L),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.zeros(L),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.array([0, 0, 0, 0, 0]),
                        "chamberlen":np.array([0, 0, 0]),
                        "demodullen":np.zeros(1),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)

                        },
                    "demodulator1":

                       {"chamber2": {
                                "x":np.array([0, 0, 0, 0, 0]),
                                    "y":np.zeros(L),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.zeros(L),
                                    "time":np.zeros(L),
                                    "PSDnum":np.array([]),
                                    "countR":np.zeros(L),
                                    "countIndeces":np.zeros(L)
                            },


                        "diod": np.array([0, 1, 0, 0, 0]),
                        "ePair": np.array([5, 10, 0, 0, 0]),
                        "timestamp": np.array([2, 3, 0, 0, 0]),
                        "chamberlen":np.array([0, 0, 0]),
                        "demodullen":np.array([2]),
                        "chamberlenViabR":np.zeros(numChamber + 1),
                        "chamberlenCountR":np.zeros(numChamber + 1)
                       },
                    }

        self.assertEqual(areGenDictsEqual(data, dataSoln9), True)



# #--------------------------------------------------------

    def test_HPFfunction(self):
        """
        testing whether high pass filter works as it should
        """
        L = 5
        v = Viability()
        v.initDict(numChamber= [0, 1] , numModul=[0])
        data = v.dictViab
        data_diod = np.array([16777216,  8388608, 8388608, 16777216, 16777216])
        data_timestamp = np.array([2, 3, 2, 3, 2])
        data_x = np.array([1, 2, 2, 1, 1])
        data_y = np.array([2, 2, 4, 1, 1])
        coef_lowpass = np.array([1, 1])
        v.updateDict(data_diod=data_diod, data_timestp=data_timestamp,
            demodulator="demodulator0", data_x=data_x, data_y=data_y,
            clockbase = 2)
        v.getHPFData(coef_lowpass=coef_lowpass, numChamber=None)


    #     #expected data_epair = np.array([1, 2, 2, 1, 1])
            #numberChamberList = [0, 1, 0]
    #     # num = [1, 2, 1]
    #     # idx = [0, 2, 4]
    #     # idx1 = [0, 1, 2]
    #     # elem =  [0, 2, 4]


        dataSoln10 = {"demodulator0":

                           {"chamber1": {
                                    "x":np.array([2, 2, 0, 0, 0]),
                                    "y":np.array([2, 4, 0, 0, 0]),
                                    "count":np.array([]),
                                    "arrayHPF":np.sqrt(20)*1000 - np.convolve(coef_lowpass,
                                 v.dictViab["demodulator0"]["chamber1"]["viabR"][0:2],
                                     mode='valid'),
                                    "viabR":np.array([np.sqrt(8)*1000, np.sqrt(20)*1000, 0, 0, 0]),
                                    "time":np.array([0.5, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "countR":np.array([0, 0, 0, 0, 0]),
                                    "countIndeces":np.zeros(L)

                                },

                            "chamber0": {
                                    "x":np.array([1, 1, 1, 0, 0]),
                                    "y":np.array([2, 1, 1, 0, 0]),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([0,0,0, 0, 0]),
                                    "time":np.array([0, 0.5, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "countR":np.array([np.sqrt(5)*1000, np.sqrt(2)*1000, np.sqrt(2)*1000, 0, 0]),
                                    "countIndeces":np.zeros(L)
                                },



                            "diod": np.array([16777216, 8388608, 8388608, 16777216, 16777216]),
                            "ePair": np.array([1, 2, 2, 1, 1]),
                            "timestamp": np.array([2, 3, 2, 3, 2]),
                            "chamberlen":np.array([3, 2]),
                            "demodullen":np.array([5]),
                            "chamberlenViabR":np.array([0, 2]),
                            "chamberlenCountR":np.array([3, 0 ])


                            }

                        }

        #print(data)

        self.assertEqual(areGenDictsEqual(data, dataSoln10, showDiff=True), True)


# # #---------------------------------------------------------------
    def test_storingData(self):
        """
        testing whether dictionary storing data works correctly
        """

        L = 5
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        v.DataForDisplaying(numChamber= [0] , numModul=[0])
        data = v.dictViab
        dataDisplaying = v.displayingData
        data_diod = np.array([16777216, 16777216])
        data_timestamp = np.array([2, 3])
        data_x = np.array([1, 2])
        data_y = np.array([2, 2])
        coef_lowpass = np.array([1, 1])
        viabR = np.array([np.sqrt(5)*1000, np.sqrt(8)*1000])
        v.updateDict(data_diod=data_diod, data_timestp=data_timestamp,
                demodulator="demodulator0", data_x=data_x, data_y=data_y,
                clockbase = 2)
        v.storingData(numChamber=[0])

        dataSoln10 = {"demodulator0":


                           {"chamber0": {
                                    "count":np.array([]),
                                    "PSDnum":np.array([]),
                                    "time":np.array([0]),

                                 }
                           }
                    }
        #print(dataDisplaying)
        self.assertEqual(areGenDictsEqual(dataDisplaying, dataSoln10, showDiff=True), True)

# # #-------------------------------------------------------------------------
    def test_numToChamber(self):
        """
        testing whether calcualtion of chamber
        from num is correct
        """
        num = [0, 29, 1, 4, 5]
        v = Viability()
        numChamberList = v.numToChamber(num)

        numChamber = [0, 14, 0, 2, 2]


        #self.assertListEqual(num1, num2, msg=None)

        self.assertEqual(numChamberList, numChamber, msg=None)



# #-----------------------------------------------------------------
class TestsCountRViabR(unittest.TestCase):
    """
    testing whether R is sliced correctly and
    slices are correctly stored in viabR and countR.
    """
    def test_insertNumDictDataViabR(self):
        """
        testing whether data are inserted correctly into
        a dictionary under key "viabR".
        """
        data_x = np.array([1, 2, 2])
        data_y = np.array([0, 1, 1])
        num = [1, 2, 1]
        numberChamberList = [0, 1, 0]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        startIndexViabR = 0
        stopIndexViabR = 2
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictDataViabR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, startIndexViabR=startIndexViabR,
            stopIndexViabR=stopIndexViabR, start=start, elem=elem)



        dataSoln6 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([np.sqrt(5)*1000, np.sqrt(5)*1000,
                                    0, 0, 0]),
                                "countIndeces":np.zeros(L),
                                "time":np.zeros(L),
                                "countR":np.zeros(L),
                                "PSDnum":np.array([])
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber),
                        "chamberlenViabR":np.zeros(numChamber),
                        "chamberlenCountR":np.zeros(numChamber),
                        "demodullen":np.zeros(1)

                        }
                    }


        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)


# # #----------------------------------------------------------
    def test_updateChamberLenviabR(self):
        """
        testing whether chamber length for viability data are updated
        correctly
        """

        data_x = np.array([1, 2, 2, 2])
        data_y = np.array([0, 1, 1, 1])
        num = [1, 2, 1]
        numberChamberList = [0, 1, 0]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        startIndexViabR = 0
        stopIndexViabR = 2
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.updateChamberLenViabR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, start=start, elem=elem)

        data_x = np.array([1, 2, 2, 2])
        data_y = np.array([0, 1, 1, 1])
        start = 3
        elem = 3

        v.updateChamberLenViabR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, start=start, elem=elem)

        dataSoln6 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([np.sqrt(5)*1000, np.sqrt(5)*1000,
                                   np.sqrt(5)*1000, 0, 0]),
                                "time":np.zeros(L),
                                "countR":np.zeros(L),
                                "PSDnum":np.array([]),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber),
                        "chamberlenViabR":np.array([3]),
                        "chamberlenCountR":np.zeros(numChamber),
                        "demodullen":np.zeros(1)

                        }
                    }

        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# # #-----------------------------------------------------------------
    def test_InsertNumDicDataCountR(self):
        """
        testing whether data are correctly inserted into
        a dicitonary "countR"
        """
        data_x = np.array([1, 2, 2])
        data_y = np.array([0, 1, 1])
        num = [1, 2, 1]
        numberChamberList = [0, 1, 0]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        startIndexCountR = 0
        stopIndexCountR = 2
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictDataCountR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, startIndexCountR=startIndexCountR,
            stopIndexCountR=stopIndexCountR, start=start, elem=elem)



        dataSoln6 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([0, 0, 0, 0, 0]),
                                "time":np.zeros(L),
                                "countR":np.array([np.sqrt(5)*1000, np.sqrt(5)*1000,
                                    0, 0, 0]),
                                "PSDnum":np.array([]),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber),
                        "chamberlenViabR":np.zeros(numChamber),
                        "chamberlenCountR":np.zeros(numChamber),
                        "demodullen":np.zeros(1)

                        }
                    }


        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# #---------------------------------------------------------
    def test_updateChamberLenviabR(self):
        """
        testing whether chamber length for viability data are updated
        correctly
        """

        data_x = np.array([1, 2, 2, 2])
        data_y = np.array([0, 1, 1, 1])
        num = [1, 2, 1]
        numberChamberList = [0, 1, 0]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        startIndexCountR = 0
        stopIndexCountR = 2
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.updateChamberLenCountR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, start=start, elem=elem)

        data_x = np.array([1, 2, 2, 2])
        data_y = np.array([0, 1, 1, 1])
        start = 3
        elem = 3

        v.updateChamberLenCountR(data_x=data_x, data_y=data_y,
            demodulator="demodulator0", numberChamberList=numberChamberList,
            idx1=idx1, start=start, elem=elem)

        dataSoln6 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "viabR":np.array([0, 0, 0, 0, 0]),
                                "time":np.zeros(L),
                                "countR":np.array([np.sqrt(5)*1000, np.sqrt(5)*1000,
                                   np.sqrt(5)*1000, 0, 0]),
                                "PSDnum":np.array([]),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber),
                        "chamberlenViabR":np.array([0]),
                        "chamberlenCountR":np.array([3]),
                        "demodullen":np.zeros(1)

                        }
                    }

        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# # #--------------------------------------------------------------
    def test_inesrtNumDictDataViabRandCountR(self):
        """
        testing whether detecting odd and even number is
        correctly executed.
        """
        data_x = np.array([1, 2, 2, 2])
        data_y = np.array([0, 1, 1, 1])
        num = [0, 2, 1]
        numberChamberList = [0, 1, 0]
        idx1 = 0
        start = 1
        elem = 2
        L = 5
        numChamber = 1
        startIndexCountR = 0
        stopIndexCountR = 2
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        v.InsertNumDictDataViabRandCountR(data_x=data_x, data_y=data_y,
                                        start=start, elem=elem,
                                        demodulator="demodulator0",
                                        numberChamberList=numberChamberList,
                                         idx1=idx1, num=num)

        dataSoln6 = {"demodulator0":

                       {"chamber0": {
                                "x":np.zeros(L),
                                "y":np.zeros(L),
                                "count":np.array([]),
                                "arrayHPF":np.array([]),
                                "countR":np.array([0, 0, 0, 0, 0]),
                                "time":np.zeros(L),
                                "viabR":np.array([np.sqrt(5)*1000, np.sqrt(5)*1000,
                                   0, 0, 0]),
                                "PSDnum":np.array([]),
                                "countIndeces":np.zeros(L)
                            },


                        "diod": np.zeros(L),
                        "ePair": np.zeros(L),
                        "timestamp": np.zeros(L),
                        "chamberlen":np.zeros(numChamber),
                        "chamberlenViabR":np.array([2]),
                        "chamberlenCountR":np.array([0]),
                        "demodullen":np.zeros(1)

                        }
                    }



        self.assertEqual(areGenDictsEqual(data, dataSoln6), True)

# # #---------------------------------------------------------------
    def test_updateDict2(self):
        """
        testing whether
        """

        L = 5
        v = Viability()
        v.initDict(numChamber= [0, 1] , numModul=[0])
        data = v.dictViab
        data_diod = np.array([16777216,  8388608, 8388608])
        data_timestamp = np.array([2, 3, 2])
        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        v.updateDict(data_diod=data_diod, data_timestp=data_timestamp,
            demodulator="demodulator0", data_x=data_x, data_y=data_y,
            clockbase = 2)



        # #expected data_epair = np.array([1, 2, 2, 1, 1])
        # # num = [1, 2, 1]
        # # idx = [0, 2, 4]
        # # idx1 = [0, 1, 2]
        # # elem =  [0, 2, 4]


        dataSoln10 = {"demodulator0":

                           {"chamber1": {
                                    "x":np.array([2, 2, 0, 0, 0]),
                                    "y":np.array([2, 4, 0, 0, 0]),
                                    "countR":np.array([0,0,0, 0, 0]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([np.sqrt(8)*1000, np.sqrt(20)*1000, 0, 0, 0]),
                                    "time":np.array([0.5, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "count":np.array([]),
                                    "countIndeces":np.zeros(L)
                                },

                            "chamber0": {
                                    "x":np.array([1, 0, 0, 0, 0]),
                                    "y":np.array([2, 0, 0, 0, 0]),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([0, 0, 0, 0, 0]),
                                    "time":np.array([0, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "countR":np.array([np.sqrt(5)*1000, 0, 0, 0, 0]),
                                    "countIndeces":np.zeros(L)
                                },



                            "diod": np.array([16777216, 8388608, 8388608, 0, 0]),
                            "ePair": np.array([1, 2, 2, 0, 0]),
                            "timestamp": np.array([2, 3, 2, 0, 0]),
                            "chamberlen":np.array([1, 2]),
                            "demodullen":np.array([3]),
                            "chamberlenViabR":np.array([0, 2]),
                            "chamberlenCountR":np.array([1, 0])


                            }

                        }



        self.assertEqual(areGenDictsEqual(data, dataSoln10), True)



# # #--------------------------------------------------
    def test_removingZerosViabRCountR(self):
        """
        zeros are removed from the endings of the arrays
        under keys "viabR" and "countR"

        """
        L = 5
        v = Viability()
        v.initDict(numChamber= [0, 1] , numModul=[0])
        data = v.dictViab
        data_diod = np.array([16777216,  8388608, 8388608])
        data_timestamp = np.array([2, 3, 2])
        data_x = np.array([1, 2, 2])
        data_y = np.array([2, 2, 4])
        v.updateDict(data_diod=data_diod, data_timestp=data_timestamp,
            demodulator="demodulator0", data_x=data_x, data_y=data_y,
            clockbase = 2)

        numChamber = [0, 1]
        v.removingZerosViabRCountR(numChamber)



        # #expected data_epair = np.array([1, 2, 2, 1, 1])
        # # num = [1, 2, 1]
        # # idx = [0, 2, 4]
        # # idx1 = [0, 1, 2]
        # # elem =  [0, 2, 4]


        dataSoln10 = {"demodulator0":

                           {"chamber1": {
                                    "x":np.array([2, 2, 0, 0, 0]),
                                    "y":np.array([2, 4, 0, 0, 0]),
                                    "countR":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([np.sqrt(8)*1000, np.sqrt(20)*1000]),
                                    "time":np.array([0.5, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "count":np.array([]),
                                    "countIndeces":np.zeros(L)
                                },

                            "chamber0": {
                                    "x":np.array([1, 0, 0, 0, 0]),
                                    "y":np.array([2, 0, 0, 0, 0]),
                                    "count":np.array([]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([]),
                                    "time":np.array([0, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "countR":np.array([np.sqrt(5)*1000]),
                                    "countIndeces":np.zeros(L)
                                },



                            "diod": np.array([16777216, 8388608, 8388608, 0, 0]),
                            "ePair": np.array([1, 2, 2, 0, 0]),
                            "timestamp": np.array([2, 3, 2, 0, 0]),
                            "chamberlen":np.array([1, 2]),
                            "demodullen":np.array([3]),
                            "chamberlenViabR":np.array([0, 2]),
                            "chamberlenCountR":np.array([1, 0])


                            }

                        }


        self.assertEqual(areGenDictsEqual(data, dataSoln10), True)

#-------------------------------------------------------------

    def test_peakDataStoringDict(self):
        """
        testing whether data are stored correctly

        """
        L = 5
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        data = v.dictViab
        #putting data to a dictionary under a key "countR"
        v.dictViab["demodulator0"]["chamber0"]["countR"] = np.array([0, 1, 0, 5, 3])
        #data_diod = np.array([16777216,  8388608, 8388608])
        #data_timestamp = np.array([2, 3, 2])
        #data_x = np.array([1, 2, 2])
        #data_y = np.array([2, 2, 4])
        numChamber = [0]
        v.dictViab["demodulator0"]["chamberlenCountR"] = np.array([5])

        v.peakDataStoringDict(mph=None, mpd=2, threshold=0, edge='rising',
                                    kpsh=False, valley=False, show=False,
                                    ax=None, numChamber=numChamber)



        dataSoln10 = {"demodulator0":

                           {"chamber0": {
                                    "x":np.array([0, 0, 0, 0, 0]),
                                    "y":np.array([0, 0, 0, 0, 0]),
                                    "countR":np.array([0, 1, 0, 5, 3]),
                                    "arrayHPF":np.array([]),
                                    "viabR":np.array([0, 0, 0, 0, 0]),
                                    "time":np.array([0, 0, 0, 0, 0]),
                                    "PSDnum":np.array([]),
                                    "count":np.array([2]),
                                    "countIndeces":np.array([1, 3])
                                },



                            "diod": np.array([0, 0, 0, 0, 0]),
                            "ePair": np.array([0, 0, 0, 0, 0]),
                            "timestamp": np.array([0, 0, 0, 0, 0]),
                            "chamberlen":np.array([0]),
                            "demodullen":np.array([0]),
                            "chamberlenViabR":np.array([0]),
                            "chamberlenCountR":np.array([5])


                            }

                        }

        print(data)

        self.assertEqual(areGenDictsEqual(data, dataSoln10), True)


# #--------------------------------------------------------------
    def test_storingData(self):
#         """
#         testing whether dictionary which is permanent is ok
#         """

        L = 5
        v = Viability()
        v.initDict(numChamber= [0] , numModul=[0])
        v.DataForDisplaying(numChamber= [0] , numModul=[0])
        data = v.dictViab
        dataDisplaying = v.displayingData
        data_diod = np.array([16777216, 16777216])
        data_timestamp = np.array([2, 3])
        data_x = np.array([1, 2])
        data_y = np.array([2, 2])
        coef_lowpass = np.array([1, 1])
        viabR = np.array([np.sqrt(5)*1000, np.sqrt(8)*1000])
        v.updateDict(data_diod=data_diod, data_timestp=data_timestamp,
                demodulator="demodulator0", data_x=data_x, data_y=data_y,
                clockbase = 2)
        v.storingData(numChamber=[0])

        dataSoln10 = {"demodulator0":


                           {"chamber0": {
                                    "count":np.array([]),
                                    "PSDnum":np.array([]),
                                    "time":np.array([0]),

                                 }
                           }
                    }
        # print(data)
        # print(dataDisplaying)
        # print("")
        # print(dataSoln10)
        self.assertEqual(areGenDictsEqual(dataDisplaying, dataSoln10), True)

#---------------------------------------------------------------------------
    def test_peakDataStoringDict2(self):
        """

        """


#function is tested but not with unitests, because
#data that are already filtered were used
def getPSDHighPassData():

    #adding highpass filter data into a dictionary
    highpass_filter_data = 'C:\\Users\\User\\Documents\\PYTHON\PROJECTS_1\\filtered_data_highpass.csv'
    highpass_filter = list()
    with open (highpass_filter_data) as CSV:
        for line in CSV:


            line = line.strip()
            line = line.split(" ")
            #print(line)


            for elem in line:
                if elem == "":
                    pass
                else:
                    elem = float(elem)
                    highpass_filter.append(elem)
    data_highpass = np.array(highpass_filter)
    return data_highpass

def get_PSD():
    """
    testing whether function works if
    data from highpass filtered data are imported into a dictionary.

    """
    data_highpass = getPSDHighPassData()
    v = Viability()
    v.initDict(numChamber= [0] , numModul=[0])

    v.dictViab["demodulator0"]["chamber0"]["arrayHPF"] = data_highpass
    v.getPSDNum(numChamber=[0])
    print(type(v.dictViab["demodulator0"]["chamber0"]["PSDnum"]))
    v.DataForDisplaying(numChamber=[0], numModul=[0])
    v.storingData(numChamber=[0])
    print(v.displayingData)





if __name__ == '__main__':

    unittest.main()


