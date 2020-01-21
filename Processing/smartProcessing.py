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


class SmartLoading:

    def __init__(self,configfile):
        print('Inside the smart processing module')
        self.config = configfile

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
                # Create a container for collect the signals. sig.getNsamples gives the number of singnals in each channel
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

        # Starting a for loop to loop over the edf files

        ecg_label = []
        ecg_data = []
        for edffilePath in edffilePaths:
            # Getting the completet path of the edf files and the edf file information from the function edfinfoReader()
            edf_list, edfInfo = self.edfinfoReader(edffilePath,edfInfofile)
            for filename in edf_list[0:1]:
                # The below extracts the last component of the path which is the file name with extension .edf
                baseFilename = ntpath.basename(filename)
                # Based on the base file name extract relevant information from the information file
                edfDetails =edfInfo.loc[edfInfo['EDF'] == baseFilename]
                # Ensure that the details extracted about the edfile are not none . Based on the details extract the details of signal
                if len(edfDetails) == 0:
                    continue
                # Reading the edf signals using a new function edfRead()

                sig,sigSamps = self.edfRead(filename,edfDetails)









        return sig,sigSamps

