'''
JMJPFU
13-Jan-2020
This is the processing module for the smart Cardio project

Lord bless this attempt of yours
'''

print('Lord is my Shepherd there is nothing I shall want')

'''
""" preprocess ecg data as config file
        Parameters
        ----------
        args : argparse parameters, required
            arguments when start this program

        Returns
        -------
        input_data : list(tuple)
            return transform ecg data and category number
        input_label : list(tuple)
            return label for ecg data
    """
    EDF_FILE_PATHS = json.loads(args.config.get('ecg', 'edf_file_path'))
    EDF_INFO_FILE = args.config.get('ecg', 'edf_info_file')


'''

############ Importing necesasry library files
import pandas as pd
import json
import os
import ntpath
import pyedflib
import numpy as np
import traceback
import re


class SmartLoading:

    def __init__(self,configfile):
        print('Inside the smart processing module')
        self.config = configfile
        self.beatAnots = ["N", "L", "R", "B", "A", "a", "J", "S", "e", "j", "n", "V", "r", "E", "!", "F", "/", "f", "Q", "?"]

    def edfinfoReader(self,edffilepath,edfInfofile):
        # This function is to read the information of the edf's from the input file
        edf_list = []
        for(path,dir,files) in os.walk(edffilepath):
            for indfile in files:
                # Splitting the path of the file name to get the extension
                ext = os.path.splitext(indfile)[-1]
                # Checking whether all files are of form .edf
                if ext == '.edf':
                    edf_list.append(path + '/' + indfile)

        edfInfo =pd.read_csv(edfInfofile,sep=(','))

        return edf_list , edfInfo

    def edfRead(self,edffile,edfInfo):
        # This function takes the edf file and reads its contents based on the info file
        try:
            # Read the signals from the file using the library EdfReader
            sig = pyedflib.EdfReader(edffile)
            # Creating a list within the signals to store the channel names
            sig.sig_labels = []
            # Get the channel information from the information files
            chan1_name = self.config.get('ecgInfo','chan1_name')
            chan2_name = self.config.get('ecgInfo', 'chan2_name')
            # Appending the signal values to the list
            sig.sig_labels.append(edfInfo[chan1_name].values[0])
            sig.sig_labels.append(edfInfo[chan2_name].values[0])
            print('These are the signal labels',sig.sig_labels)
            inscopeLeads = self.config.get('ecgInfo','inscopeLeads')
            # if the channel values are in the allowed lead values then proceed with processing the signal
            if (sig.sig_labels[0] in inscopeLeads or sig.sig_labels[1] in inscopeLeads):
                # Get the total number of signal channels
                sigNum = sig.signals_in_file
                # Create a container to collect the signals. sig.getNsamples gives the number of singnals in each channel
                # This is given in the form [651600 651600]
                sigSamps = np.zeros((sigNum,sig.getNSamples()[0]))
                print('Shape of the signal dataframe',sigSamps.shape)
                # Read the signals into the container
                for i in np.arange(sigNum):
                    if sig.sig_labels[i] in inscopeLeads:
                        # Reading the signals into the container
                        sigSamps[i,:] = sig.readSignal(i)
                    else:
                        print('Not allowed leads')
                        sigSamps = None

            return sig,sigSamps
        except:
            print('This is in case of exceptions')
            tb = traceback.format_exc()
            print(tb)
        finally:
            print('The signals are closed here')
            sig.close()


    def rawLoader(self):
        # Getting the path for the edf files and the info file
        edffilePaths = list(self.config.get('datafiles','ecg_filepath').split(' '))
        edfInfofile = self.config.get('datafiles','ecg_info')
        return edffilePaths,edfInfofile
    def annotationReader(self):
        # This function is to read the annotation of the signals from the file
        return None

    def makeEcgdata(self,anot_fileName):

        # Make empty containers to store the peak signal position and the annotations
        peaks = []
        annotations = []
        # Read the annotation files
        anotations =open(anot_fileName,'r')
        anotLines = anotations.readlines()

        # Checking the first record of the annotation if it is time stamp or not
        row1 = re.split("\s+", anotLines[0])
        if(row1[1] == 'Time'):
            anotLines.pop(0)

        # Proceeding with reading the annotations

        for rows in anotLines:
            # Splitting the signal details
            temp = re.split("\s+", re.sub("[,\t]", " ", rows).strip())
            # Checking if the signal details have the required number of components
            if(len(temp) > 5):

                if(temp[2] not in self.beatAnots):
                    print('This input is a non beat annotation: {}'.format(temp[2]))
                    continue
                peaks.append(temp[1])
                annotations.append(temp[2])


        return peaks,annotations





