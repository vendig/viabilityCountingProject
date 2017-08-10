
import numpy as np
import math
import scipy
from scipy import signal
import sys
from detect_peaks import detect_peaks



class Viability():
    def __init__(self):
        '''Initializing variables of a class Viability.'''

        self.dictViab = {}
        self.displayingData = {}
        #self.maxChamberLen = self.numMinutes * self.samplingRate * 60
        self.maxChamberLen = 3*250*60
        #self.maxChamberLen = 5


    def initDict(self, numChamber=list(), numModul=list()):
        '''
        Initializing a dictionary.

        Parameters
        ----------
        numChamber : list
                Number of chambers, etc. used are chambers 1 and 4,
                then numChamber = [1, 4]
        numModul : list
                Number of demodulators, etc. used is demodulator
                0, then numModul = [0]

        Returns
        -------
        dictionary
                Structure of dictionary follows the structure:

                  demodulator0:
                    "chamber0" : {
                            "x": array([0,...,0]),
                           "y": array([0,...,0]),
                           "count":np.array([]),
                           "arrayHPF":np.array([]),
                           "viabR":np.array([0,...,0]),
                           "time":np.array([0,...,0]),
                           "PSDnum": np.array([]),
                           "countR":np.array([0,...,0]),
                           "countIndex":np.array([0,...,0])

                           }, #each array of length maxChamberLen
                    ...
                    ...
                    "chamber1" : {
                            "x": array([0,...,0]),
                           "y": array([0,...,0]),
                           "count":np.array([]),
                           "arrayHPF":np.array([]),
                           "viabR":np.array([0,...,0]),
                           "time":np.array([0,...,0]),
                           "PSDnum":np.array([]),
                           "countR":np.array([0,...,0]),
                           "countIndex":np.array([0,...,0])
                           }, #each array of length maxChamberLen
                    {
                    "diod" : np.array([]),
                    "ePair" : np.array([]),
                    "timestamp" : np.array([]),
                    "chamberlen":np.array([0, 0, ..., 0]),
                    "chamberlenViabR":np.array([0, 0, ...,0]),
                    "chamberlenCountR":np.array([0, 0, ..., 0]), #length n7
                    "demodullen":np.array([0])
                    }

                demodulator1:
                    etc.
        '''
        #addinf one because we start counting from zero,
        #so if we have 0, 1, 2 chambers we have three chambers
        maxNumChamber = max(numChamber) + 1

        for i in numModul:
            self.dictViab.update({"demodulator" + str(i):{}})

        for key, elem in self.dictViab.items():
            #one per modulator
            self.dictViab[key].update({
                                        "diod": np.zeros(self.maxChamberLen),
                                       "ePair": np.zeros(self.maxChamberLen),
                                       "timestamp": np.zeros(self.maxChamberLen),
                                       "chamberlen":np.zeros(maxNumChamber),
                                       "chamberlenViabR":np.zeros(maxNumChamber),
                                       "chamberlenCountR":np.zeros(maxNumChamber),
                                       "demodullen":np.zeros(1)
                                       })

            for i in numChamber:
                self.dictViab[key].update({"chamber" + str(i):
                                            {
                                            "x": np.zeros(self.maxChamberLen),
                                             "y":np.zeros(self.maxChamberLen),
                                             "count":np.array([]),
                                             "viabR":np.zeros(self.maxChamberLen),
                                             "arrayHPF":np.array([]),
                                             "PSDnum":np.array([]),
                                             "time":np.zeros(self.maxChamberLen),
                                             "countR":np.zeros(self.maxChamberLen),
                                             "countIndeces":np.zeros(self.maxChamberLen)

                                             }
                                                })



    def DataForDisplaying(self, numChamber=list(), numModul=list()):
        """
        Initializing a dictionary.

        Function stores data of a dictionary ´dictViab´, accessed by keys
        "time", "count" and "PSDnum" into a dictionary named ´displayingData´.

        Parameters
        ----------
        numChamber : list
                Number of chambers
        numModul : list
                Number of demodulators

        Returns
        -------
        dictionary named ´displayingData´
                Structure of a dictionary follows the structure:

                    demodulator0:
                        "chamber0" : {
                               "PSDnum": np.array([]),
                               "count":np.array([]),
                               "time":np.array([])
                               }
                        ...
                        ...
                        "chambern" : {
                               "PSDnum": np.array([]),
                               "count":np.array([]),
                               "time":np.array([])
                               }


        """

        self.displayingData = {}

        for i in numModul:
            self.displayingData.update({"demodulator"+str(i):{}})

        for key, elem in self.displayingData.items():

            for i in numChamber:
                self.displayingData[key].update({"chamber"+str(i):{"count":np.array([]),
                                                          "PSDnum":np.array([]),
                                                          "time":np.array([])}})




    def peakDetection(self):
        """
        This is a documentation copied from a file detect_peaks.py

        Detect peaks in data based on their amplitude and other features.

        Parameters
        ----------
        x : 1D array_like
            data.
        mph : {None, number}, optional (default = None)
            detect peaks that are greater than minimum peak height.
        mpd : positive integer, optional (default = 1)
            detect peaks that are at least separated by minimum peak distance (in
            number of data).
        threshold : positive number, optional (default = 0)
            detect peaks (valleys) that are greater (smaller) than `threshold`
            in relation to their immediate neighbors.
        edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
            for a flat peak, keep only the rising edge ('rising'), only the
            falling edge ('falling'), both edges ('both'), or don't detect a
            flat peak (None).
        kpsh : bool, optional (default = False)
            keep peaks with same height even if they are closer than `mpd`.
        valley : bool, optional (default = False)
            if True (1), detect valleys (local minima) instead of peaks.
        show : bool, optional (default = False)
            if True (1), plot data in matplotlib figure.
        ax : a matplotlib.axes.Axes instance, optional (default = None).

        Returns
        -------
        ind : 1D array_like
            indeces of the peaks in `x`.

        """
        indexes = detect_peaks(countR, mph=None, mpd=1, threshold=0, edge='rising',
                                    kpsh=False, valley=False, show=False, ax=None)


    def peakDataStoringDict(self, mph=None, mpd=1, threshold=0, edge='rising',
                                    kpsh=False, valley=False, show=False,
                                    ax=None, numChamber=list()):
        """
        Function calls a function for detecting peaks and
        stores data in a dictionary.

        Function applies a function for a  detection of peaks
        to a data stored in a dictionary ´dictViab´ under key
        "countR". Number of peaks is stored in a dictionary ´dictViab´
        under a key "count" and indeces of peaks are stored under a
        key "countIndeces"

        Parameters
        ----------
        numChamber : list
            Number of chambers which are used.

        Returns
        -------
        None, but it updates a dictionary ´dictViab´ with number of peaks.
        """
        for demodulator in self.dictViab.keys():

            for i in numChamber:

                #if there is no data in "countR", then 0 is added to "count"
                if self.dictViab[demodulator]["chamberlenCountR"][i] > 0:

                    countR = self.dictViab[demodulator]["chamber" + str(i)]["countR"]

                    indeces = detect_peaks(countR, mph=None, mpd=1, threshold=0, edge='rising',
                                    kpsh=False, valley=False, show=False, ax=None)

                    #storing number of peaks into a dictionary under a key "count"
                    self.dictViab[demodulator]["chamber" + str(i)]["count"] = np.array([len(indeces)])

                    #calling function for storing indeces of peaks into a dictionary
                    self.insertCountIndecesDict(i=i, indeces=indeces, demodulator=demodulator)

                else:
                    self.dictViab[demodulator]["chamber" + str(i)]["count"] = np.array([0])




    def insertCountIndecesDict(self, i, indeces, demodulator):
        """
        Function inserts into a dictionary
        indeces of the peaks.

        Example
        -------
        dataForPeakDetection = np.array([0, 1, 8, 2, 1])
        dataDetectedPeak = 8
        indecesDetectedPeak = 2

        """
        self.dictViab[demodulator]["chamber" + str(i)]["countIndeces"] = indeces


    def getSliceIndex(self, ePair):
        '''
        Function detect the change of a number.

        Takes `ePair` and returns breakpoints and number of
        activated electrodes at breakpoints.

        Parameters
        ----------
        ePair: numpy array, positive int
            A function dioToElectrodePair(self, dio), calculates from ´diod´,
            which is received from an impedance device, an´ePair´.

        Returns
        -------
        list
            idx: containing the index of the breakpoints.
                A 'breakpoint' is where the value in the array changes.
        list
            num: containing the values of ´ePair´ at the breakpoints.

        Example
        -------
                Input:
                    ePair = np.array([1, 2, 2, 5])
                Output:
                    idx = [0, 2]
                    num = [1, 2, 5]
        '''
        idx = list() #this is a temporal
        num = list() #this is a temporal

        for i, j in enumerate(ePair):
            if i in range(len(ePair)-1) and ePair[i] != ePair[i+1]:
                idx.append(i)
                num.append(ePair[i])

        #append the length of the sequence for the last number
        idx.append(len(ePair)-1)
        num.append(ePair[-1])


        return(idx, num)

    def numToChamber(self, num):
        """
        Function gives numbers of chambers.

        Function converts ´num´ to a chamber number and it
        is true that duplet of numbers represent the same chamber;
        etc. 0, 1 equals to chamber number 0, num = [2, 3] equals to
        chamber number 1.

        Example
        -------
            num = [0, 1, 17, 18]
            chamber numbers = [0, 0, 9, 9]


        """
        numberChamberList = list()

        #calculating from ´num´, number of chamber
        for i in num:
                numberChamberList.append(int(np.floor(i / 2)))

        return numberChamberList



    def getR(self, data_x, data_y, elem, start, multiplier=1000):
        """
        Calculating impedance out of data, received from an impedance device.

        Function which calculates an impedance out of x, named as ´data_x´
        and y, named ´data_y´ got from an impedance device.

        Parameters
        ----------
        data_x : np.array
            Array received from an impedance device, presenting a real part of
            impedance.
        data_y : numpy array
            Array received from an impedance device, presenting an imaginatory
            part of an impedance.
        elem :
            A value of list named ´ídx´.
        start :
            Start with zero and increase for ´elem´.

        Returns
        -------
        numpy array
            R : impedance

        """

        R = (np.sqrt((data_x[start:(elem+1)])**2 +
                     (data_y[start:(elem+1)])**2))*multiplier

        return R


    def InsertNumDictData_x(self, data_x, demodulator,
                             numberChamberList, idx1, startIndex,
                                stopIndex, start, elem):

        """
        Function inserts data into a dictionary.

        Function inserts ´data_x´ slices into a corresponding demodulator
        and chamber.

        """
        #replacing the length of zeros inside key "x" ´

        self.dictViab[demodulator]["chamber" + str(numberChamberList[idx1])]["x"][startIndex:stopIndex]=\
            data_x[start:(elem+1)]


    def InsertNumDictData_y(self, data_y, demodulator, numberChamberList, idx1, startIndex,
                            stopIndex, start, elem):
        """
        Function inserts data into a dictionary.

        Function inserts ´data_x´ slices into a corresponding demodulator
        and chamber.

        """
        #replacing the length of zeros inside key "x" ´
        self.dictViab[demodulator]["chamber" + str(numberChamberList[idx1])]["y"][startIndex:stopIndex]=\
            data_y[start:(elem+1)]


    def InsertNumDictDataViabR(self, data_x, data_y, demodulator, numberChamberList,
                                idx1, startIndexViabR, stopIndexViabR,
                                start, elem):
        """
        Function inserts data into a dictionary.

        Function inserts ´R´ slices into a corresponding demodulator
        and chamber.

        """
        #replacing the length of zeros inside key "viabR" ´
        #if a number of ePair is odd, then R is sliced and stored
        #into key "viabR"

        self.dictViab[demodulator]["chamber" + str(numberChamberList[idx1])]["viabR"][startIndexViabR:stopIndexViabR]=\
            self.getR(data_x, data_y, elem, start, multiplier=1000)


    def updateChamberLenViabR(self, data_x, data_y, start,
                         elem, demodulator, numberChamberList, idx1):
        """
        Function updates a chamber length.

        Function stores the information of a length of a key "viabR"
        inside a dictionary under a key "chamberlengthViabR". It is
        required for correct replacement of zeros inside a dictionary
        with sliced data of a module R.

        """
        #getting R out of data_x and data_y
        R = self.getR(data_x, data_y, elem, start, multiplier=1000)

        #slice length of a slice length of R, which will be stored
        #in viabR
        sliceLength = int(len(R))

        #reading a start index to know where to start replacing zeros
        #it is stored inside key "chamberlenViabR"
        startIndexViabR = int(self.dictViab[demodulator]["chamberlenViabR"][numberChamberList[idx1]])

        #getting stopIndex to know till which zero number should be inserted
        stopIndexViabR = startIndexViabR + sliceLength

        #function inserts numbers at the places of zeros
        self.InsertNumDictDataViabR(data_x, data_y, demodulator, numberChamberList,
                                idx1, startIndexViabR, stopIndexViabR,
                                start, elem)

        #updating a startIndex - where zeros start being replacing.
        #insert stop index inside dictionary, at a place of the right chamber
        self.dictViab[demodulator]["chamberlenViabR"][numberChamberList[idx1]] = stopIndexViabR



    def InsertNumDictDataViabRandCountR(self, data_x, data_y,
                                        start, elem, demodulator,
                                        numberChamberList, idx1, num):

        """
        Function insert slices of R (impedance modulus) inside
        an array for viability calculations "viabR" or
        inside array "countR" for counting purposes.
        """

        #if number of activated ePair is even:
        if num[idx1] % 2 == 0:
            #slices of R are inserted into a key "viabR"
            self.updateChamberLenViabR(data_x, data_y, start,
                         elem, demodulator, numberChamberList, idx1)

        else:
            #otherwise slices of R are inserted into a key "countR"
            self.updateChamberLenCountR(data_x, data_y, start,
                         elem, demodulator, numberChamberList, idx1)


    def InsertNumDictDataCountR(self, data_x, data_y,  demodulator, numberChamberList,
                                startIndexCountR, stopIndexCountR,
                                start, elem, idx1):
        """
        function inserts data into a dictionary.

        function inserts ´R' slices into a corresponding
        demodulator and chamber, depending on electrode activated.
        """

        self.dictViab[demodulator]["chamber" + str(numberChamberList[idx1])]["countR"][startIndexCountR:stopIndexCountR]=\
        self.getR(data_x, data_y, elem, start, multiplier=1000)



    def updateChamberLenCountR(self, data_x, data_y, start,
                         elem, demodulator, numberChamberList, idx1):
        """
        Function updates a chamber length.

        Function updates a chamber length for key "countR",
        which are got from slicing R and are used for counting
        calculations.
        """
        #getting R out of data_x and data_y
        #R_array = self.getR(data_x, data_y, elem, start, multiplier=1000)

        #slice length of a slice length of R, which will be stored
        #in viabR
        sliceLength = int(len(self.getR(data_x, data_y, elem, start, multiplier=1000)))

        #reading a start index to know where to start replacing zeros
        #it is stored inside key "chamberlenViabR"
        startIndexCountR = int(self.dictViab[demodulator]["chamberlenCountR"][numberChamberList[idx1]])

        #getting stopIndex to know till which zero number should be inserted
        stopIndexCountR = startIndexCountR + sliceLength

        #function inserts numbers at the places of zeros
        self.InsertNumDictDataCountR(data_x, data_y,  demodulator, numberChamberList,
                                startIndexCountR, stopIndexCountR,
                                start, elem, idx1)

        #updating a startIndex - where zeros start being replacing.
        #insert stop index inside dictionary, at a place of the right chamber
        self.dictViab[demodulator]["chamberlenCountR"][numberChamberList[idx1]] = stopIndexCountR






    def InsertNumDictDataTime(self, data_timestp, demodulator, numberChamberList,
                                idx1, startIndex, stopIndex,
                                start, elem, clockbase):
        """
        Function inserts data into a dicitonary.

        Function calculates out of ´data_timestp´ time and
        insert it into a dictionary.
        """
        time = self.getTime(data_timestp, demodulator, clockbase)

        #replacing the length of zeros inside key "time"
        self.dictViab[demodulator]["chamber" + str(numberChamberList[idx1])]["time"][startIndex:stopIndex]=\
            time[start:(elem+1)]




    def InsertNumDict(self, data_x, data_y, data_timestp, demodulator, numberChamberList,
                      idx1, startIndex, stopIndex, start, elem, clockbase=210e+6):
        """
        Function inserts numbers at the places of zeros inside a dictionary

        ´data_x´, ´data_y´and ´data_timestp´ are sliced. Zeros are replaced
        with slices inside a dictionary, named ´dictviab´. Slice is placed to
        a corresponding number of chamber under key "demodulator".

        Parameters
        ----------
        data_x : numpy array
            Array received from an impedance device, presenting a real part of
            impedance.
        data_y : numpy array
            Array received from an impedance device, presenting an imaginatory
            part of an impedance.
        data_timestp: numpy array
            Current time of an event that is recorded by an impedance machine.
        demodulator: str
            A key inside a dictionary ´dictViab´

        idx1 : an integer
            an index of a number inside  list ´ídx´.
        startIndex:
            A length of numpy array inside a dictionary withouth counting zeros.
            Can be found inside a key "chamberlen".
        stopIndex:
            It is calculated as ´startIndex´ plus length of slice of ´data_x´.
        start:
            Start with zero and increase for ´elem´.
        elem :
            A value of list named ´ídx´.
        numberChamberList: list
            List of numbers of chambers.

        Returns
        -------
            None but an updated dictionary, where zeros inside keys "x", "y" and "time"
               yre replaced by slices of ´data_x´, ´data_y´ and calculation of time.

        """
        #replacing the length of zeros inside key "x" ´
        self.InsertNumDictData_x(data_x, demodulator, numberChamberList, idx1, startIndex,
                            stopIndex, start, elem)
        #replacing the length of zeros inside key "y"
        self.InsertNumDictData_y(data_y, demodulator, numberChamberList, idx1, startIndex,
                            stopIndex, start, elem)


        #function getTime is called becuase time is needed for slicing
        #time is inserted into a dictionary
        self.InsertNumDictDataTime(data_timestp, demodulator, numberChamberList,
                                idx1, startIndex, stopIndex,
                                start, elem, clockbase)



    def updateChamberLenData_x(self, data_x, start,
                         elem, demodulator, numberChamberList, idx1):
        """
        Function update a dictionary only for x
        """
        #first doing it for data_x and inserting data to key x
        sliceLength = int(len(data_x[int(start):int(elem+1)]))

        #reading a start index to know where to start replacing zeros
        #it is stored inside key "chamberlen"
        startIndex = int(self.dictViab[demodulator]["chamberlen"][numberChamberList[idx1]])

        #getting stopIndex to know till which zero number should be inserted
        stopIndex = startIndex + sliceLength

        #function inserts numbers at the places of zeros
        self.InsertNumDictData_x(data_x, demodulator, numberChamberList,
                      idx1, startIndex, stopIndex, start, elem)

        #updating a startIndex - where zeros start being replacing.
        #insert stop index inside dictionary, at a place of the right chamber
        self.dictViab[demodulator]["chamberlen"][numberChamberList[idx1]] = stopIndex



    def updateChamberLen(self, data_x, data_y, data_timestp, start,
                         elem, demodulator, numberChamberList, idx1,
                          clockbase=210e+6):
        """
        It updates the key "chamberlen" inside a dictionary with the length of a
        chamber's number of values, not including the last zeros.

        Function calculates from where to where in an array of zeros under a key
        "x" zeros need to be replaced by slice ´data_x´. It can be used for slices
        of ´data_y´, as their arrays are of the same length.

        Parameters
        ----------
        data_x : numpy array
            Array received from an impedance device, presenting a real part of
            impedance.
        data_y : numpy array
            Array received from an impedance device, presenting an imaginatory
            part of an impedance.
        data_timestp: numpy array
            Current time of an event that is recorded by an impedance machine.
        start:
            Start with zero and increase for ´elem´.
        elem :
            A value of list named ´ídx´.
        demodulator: str
            A key inside a dictionary ´dictViab´
        idx1 : an integer
            an index of a number inside  list ´ídx´.
        numberChamberList: list
            List of numbers of chambers.

        Returns
        -------
            None, but a key "chamberlen" inside dictionary ´dictViab´is
            updated with a startIndex, which correspond to a length of a
            chamber's number of values, not including the last zeros.
        """

        #first doing it for data_x and inserting data to key x
        sliceLength = int(len(data_x[start:(elem+1)]))

        #reading a start index to know where to start replacing zeros
        #it is stored inside key "chamberlen"
        startIndex = int(self.dictViab[demodulator]["chamberlen"][numberChamberList[idx1]])

        #getting stopIndex to know till which zero number should be inserted
        stopIndex = startIndex + sliceLength

        #function inserts numbers at the places of zeros
        self.InsertNumDict(data_x, data_y, data_timestp, demodulator, numberChamberList,
                      idx1, startIndex, stopIndex, start, elem,  clockbase)

        #updating a startIndex - where zeros start being replacing.
        #insert stop index inside dictionary, at a place of the right chamber
        self.dictViab[demodulator]["chamberlen"][numberChamberList[idx1]] = stopIndex


    def insertNumDictModulTimestamp(self, data_timestp, demodulator,
                            startIndexDemodul, stopIndexDemodul):

        """
        Function update a dictionary with an array. Replacing zeros
        with numbers.

        function inserts into a dictionary 'dictViab' under key "timestamp"
        data.
        """
        self.dictViab[demodulator]["timestamp"][startIndexDemodul
                     :stopIndexDemodul] = data_timestp



    def insertNumDictModulDiod(self, data_diod, demodulator,
                            startIndexDemodul, stopIndexDemodul):

        """
        Function update a dictionary with an array. Replacing zeros
        with numbers.

        function inserts into a dictionary 'dictViab' under key "diod"
        data.
        """
        self.dictViab[demodulator]["diod"][startIndexDemodul
                     :stopIndexDemodul] = data_diod



    def insertNumDictModulEpair(self, data_epair, demodulator,
                            startIndexDemodul, stopIndexDemodul):
        """
        Function update a dictionary with an array. Replacing zeros
        with numbers.

        function inserts into a dictionary 'dictViab' under key "ePair"
        data.
        """
        self.dictViab[demodulator]["ePair"][startIndexDemodul
                     :stopIndexDemodul] = data_epair




    def insertNumInDemodul(self, data_timestp, data_diod, data_epair, demodulator):
        """
        Update a dictionary with a nonsliced data.

        Function replaces zeros with a nonsliced data inside a dictionary under
        a key dictViab[demodulator] but not inside different chambers under key
        dictViab[demodulator][number of chamber].

        Parameters
        ----------
        data_timestamp : numpy array
            Current time of an event that is recorded by an impedance machine.
        data_diod : numpy array
            Got from an impedance machine, digital input output data
        data_epair : numpy array
            It contains a range of numbers from 0 to a number of chambers.
            It is calculated from ´data_diod´.
        demodulator :  str
            A key inside a dictionary ´dictViab´

         Returns
         -------
            None, but it updates a dictionary under keys "demodulator"
            "timestamp", "diod" and "ePair".

        """
        #"chamberlen" includes the length of the "timestamp", "diod" and other
        #placed inside demodulator but not inside chambers
        startIndexDemodul = int(self.dictViab[demodulator]["demodullen"])

        stopIndexDemodul = int(len(data_timestp) + startIndexDemodul)

        #inserting data timestamp at the places of zeros inside ´dictViab´,
        #under key -  [demodulator]["timestamp"]
        self.insertNumDictModulTimestamp(data_timestp, demodulator,
                                    startIndexDemodul, stopIndexDemodul)

        #because the lengths of diod and epair is the same as for timestamp
        #the same start and stop index can be used for diod and epair
        self.insertNumDictModulDiod(data_diod, demodulator,
                                    startIndexDemodul, stopIndexDemodul)


        self.insertNumDictModulEpair(data_epair, demodulator,
                                     startIndexDemodul, stopIndexDemodul)

        #updating "demodulllen"
        self.dictViab[demodulator]["demodullen"] = np.array([stopIndexDemodul])



    def updateDict(self, data_diod, data_timestp, demodulator, data_x, data_y, clockbase=210e+6):
        '''
        Function inserts data into a dictionary.

        Function converts digital input output data (diod) into electrode pair (epair).
        Then converts as well epair into a chamber number. Then replaces zeros by data
        inside a coresponding chamber and demodulator and updates a length of data inside
        each array.

        Parameters
        ----------
        data_diod: numpy array
            Got from an impedance machine, digital input output data.
        data_timestamp : numpy array
            Current time of an event that is recorded by an impedance machine.
        demodulator: str
            A key inside a dictionary ´dictViab´.
        data_x : numpy array
            Array received from an impedance device, presenting a real part of
            impedance.
        data_y : numpy array
            Array received from an impedance device, presenting an imaginatory
            part of an impedance.

        Returns
        -------
            None but a dictionary ´dictViab´ is updated.
        '''

        #calling a function that returns epair
        data_epair = self.dioToElectrodePair(data_diod)

        #converting list of epair to np.array
        data_epair = np.array(data_epair)

        #inserting data inside demodulator without slicing and placing in chambers
        self.insertNumInDemodul(data_timestp, data_diod, data_epair, demodulator)

        #get idx and num from ePair
        (idx, num) = self.getSliceIndex(data_epair)

        #from num converting to chamber number
        numberChamberList = self.numToChamber(num)

        start=0

        for idx1,elem in enumerate(idx):

            #updating  a dictionary with
            self.updateChamberLen(data_x, data_y, data_timestp, start,
                                  elem, demodulator, numberChamberList, idx1,
                                  clockbase)

            #updating a dictionary with slices that will be stored in countR and viabR
            self.InsertNumDictDataViabRandCountR(data_x, data_y,
                                        start, elem, demodulator,
                                        numberChamberList, idx1, num)


            start = elem + 1




    def getTime(self, data_timestp, demodulator, clockbase=210e+6):
        """
        Converting data_timestamp to time.

        Parameters
        ----------
        data_timestp : numpy array
            Current time of an event that is recorded by an impedance device.
        demodulator : str
            A key inside a dictionary ´dictViab´.

        Returns
        -------
        float number
            time


        """

        time =  ((data_timestp - self.dictViab[demodulator]["timestamp"][0])
                            / clockbase)

        return time


    def getFs(self, demodulator, clockbase=210e+06):
        """
        calculating sampling frequency out of timestamp got from a device"""

        Fs = clockbase / ((self.dictViab[demodulator]["timestamp"][4] -
                           self.dictViab[demodulator]["timestamp"][0]) -
                           (self.dictViab[demodulator]["timestamp"][3] -
                            self.dictViab[demodulator]["timestamp"][0]))
        return Fs


    def dioToElectrodePair(self, dio):
        ''' HF2 DIO lines are stored in a 32 bit number cut relevant bits and
            switch order DIO24 - Pin8 ... DIO20 - Pin12 so MSB in Arduino is
            LSB for HF2 return decimal number from the cut 5 bits
        '''
        return [ int(format(int(i), '032b')[7:12][::-1], 2) for i in dio]



    def getHPFData(self, coef_lowpass, numChamber):
        """
        Function apply a low-pass filter to data and subtract them from
        non filtered data.

        High-pass fitlered data are obtained by subtracting lowpass filtered data
        from non filtered data (impedance modulus - R)

        Parameters:
        -----------
        coef_lowpass: numpy array
            coefficients of a filter

        numChamber: list
            number of chambers

        Returns:
            None but update a dictionary named ´dictViab´ by storing data
            under a key "arrayHPF". In case there is not enough data it
            prints "Not enough data".

        """



        for key in self.dictViab.keys():
            for i, e in enumerate(self.dictViab[key]["chamberlenViabR"]):

                if self.dictViab[key]["chamberlenViabR"][i] >= len(coef_lowpass):

                    lowpassFilteredData = np.convolve(coef_lowpass,
                                 self.dictViab[key]["chamber" + str(i)]["viabR"][int(0):int(e)],
                                     mode='valid')

                    self.dictViab[key]["chamber" + str(i)]["arrayHPF"] = \
                    self.dictViab[key]["chamber" + str(i)]["viabR"][math.ceil(len(coef_lowpass)/2)
                    : math.ceil(len(lowpassFilteredData))
                    + math.ceil(len(coef_lowpass)/2)] - lowpassFilteredData
                else:
                    print("Not enough data")



    def getPSDNum(self, numChamber=list(), clockbase=210e+06):
        """
        Function calculates a power spectral density number.

        Function calculates out of high-pass filtered data from 1-5 Hz,
        which are stored in a dictionary ´dictViab´ power spectral density
        number. In case data are not in a range of 1-5 Hz, a key
        "PSDnum" inside a dictionary ´dictViab´ will stay empty.

        Parameters
        ----------
        numChamber : list
            Number of chambers which are used.

        Return
        ------
        None but an updated dictionary ´dictViab´ with an updated
        key "PSDnum".
         """


        # exctracting data psd from 1-5 Hz
        #extracting indexis of frequencies in range of 1 to 5 Hz
        try:
            for demodulator in self.dictViab.keys():

                ##should be activated while getting data
                #Fs = self.getFs(demodulator, clockbase)
                Fs=250
                for i in numChamber:

                    index_list = list()

                    freq,psd = scipy.signal.periodogram(
                            self.dictViab[demodulator]["chamber" + str(i)]["arrayHPF"], fs = Fs)


                    for index, x in np.ndenumerate(freq):
                        if freq[index] > 1 and freq[index] < 5:
                            index_list.append(index[0])


                    psd[index_list]

                    #integrating data to get psd number

                    psd_number = np.trapz(psd[index_list], dx = freq[2]-freq[1])


                    #setting psd_number inside a dictionary
                    self.dictViab[demodulator]["chamber" + str(i)]["PSDnum"] = np.array([psd_number])

                     #emtying index_list
                    del index_list[:]
        except IndexError:
            pass


    def removingZerosNonSlicedData(self):
        """
        Function removes zeros from the endings of the arrays.

        Function removes zeros from the endings of the arrays inside
        dictionary ´dictViab´. It removes zeros from
        endings of keys "timestamp", "diod" and "ePair".

        """
        #removing zeros from keys "timestamp", "diod", "epair".

        for demodulator in self.dictViab.keys():
            self.dictViab[demodulator]["timestamp"]= \
                   np.delete(self.dictViab[demodulator]["timestamp"],
                          np.s_[self.dictViab[demodulator]["demodullen"]::])

            self.dictViab[demodulator]["diod"]=\
                    np.delete(self.dictViab[demodulator]["diod"],
                          np.s_[self.dictViab[demodulator]["demodullen"]::])

            self.dictViab[demodulator]["ePair"]=\
                    np.delete(self.dictViab[demodulator]["ePair"],
                          np.s_[self.dictViab[demodulator]["demodullen"]::])



    def removingZerosSlicedData(self, numChamber=list()):
        """
        Function removes zeros from the endings of the arrays.

        Function removes zeros from keys "x", "y", time".

        """
        for demodulator in self.dictViab.keys():
            for i in numChamber:
                self.dictViab[demodulator]["chamber" + str(i)]["x"]= \
                        np.delete(self.dictViab[demodulator]["chamber" + str(i)]["x"],
                              np.s_[int(self.dictViab[demodulator]["chamberlen"][i])::])

                self.dictViab[demodulator]["chamber" + str(i)]["y"]= \
                        np.delete(self.dictViab[demodulator]["chamber" + str(i)]["y"],
                              np.s_[int(self.dictViab[demodulator]["chamberlen"][i])::])


                self.dictViab[demodulator]["chamber" + str(i)]["time"]= \
                        np.delete(self.dictViab[demodulator]["chamber" + str(i)]["time"],
                              np.s_[int(self.dictViab[demodulator]["chamberlen"][i])::])




    def removingZerosViabRCountR(self, numChamber=list()):
        """
        Function removes zeros from the ending of the arrays.

        Function removes zeros from a dictionary ´dictViab´
        with keys "viabR" and "countR".

        """
        for demodulator in self.dictViab.keys():
            for i in numChamber:
                self.dictViab[demodulator]["chamber" + str(i)]["viabR"]= \
                        np.delete(self.dictViab[demodulator]["chamber" + str(i)]["viabR"],
                              np.s_[int(self.dictViab[demodulator]["chamberlenViabR"][i])::])


                self.dictViab[demodulator]["chamber" + str(i)]["countR"]= \
                        np.delete(self.dictViab[demodulator]["chamber" + str(i)]["countR"],
                              np.s_[int(self.dictViab[demodulator]["chamberlenCountR"][i])::])




    def removingZeros(self, numChamber=list()):
        """
        Function removes zeros from the endings of the arrays.

        Function removes zeros from the endings of the arrays inside
        dictionary ´dictViab´. Should be called before storing file of data.

        Parametrs
        ---------

        """
        #removing zeros from "timestamp", "diod", "epair"
        self.removingZerosNonSlicedData()

        #removing zeros from "time", "x", "y", "count"
        self.removingZerosSlicedData(numChamber)

        #removing zeros from "viabR" and "countR"
        self.removingZerosViabRCountR(numChamber)




    def storingData(self, numChamber=list()):

        """
        Function stores data in a permanent dictionary.

        Function stores time, count which is obtained from a number of parazites
        passed through electrode and PSD number into a dictionary ´displayingData´.

        Parameters
        ----------
        numChamber: list
                Number of chambers

        Returns
        -------
            None
        """
        #for timestamp storing only a first number
        for demodulator in self.displayingData.keys():
            for i in numChamber:

                self.displayingData[demodulator]["chamber" + str(i)]["count"] = \
                    np.concatenate((self.displayingData[demodulator]["chamber" + str(i)]["count"],
                       self.dictViab[demodulator]["chamber" + str(i)]["count"]), axis=0)

                self.displayingData[demodulator]["chamber" + str(i)]["PSDnum"] = \
                    np.concatenate((self.displayingData[demodulator]["chamber" + str(i)]["PSDnum"],
                       self.dictViab[demodulator]["chamber" + str(i)]["PSDnum"]), axis=0)


                self.displayingData[demodulator]["chamber" + str(i)]["time"] = \
                     np.concatenate((self.displayingData[demodulator]["chamber" + str(i)]["time"],
                        np.array([self.dictViab[demodulator]["chamber" + str(i)]["time"][0]])), axis=0)






















