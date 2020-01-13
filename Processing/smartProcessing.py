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

class SmartLoading:

    def __init__(self):
        print('Inside the smart processing module')

    def rawLoader(self,configfile):
        edffilePath = json.loads(configfile.get('datafiles','ecg_filepath'))
        return edffilePath

