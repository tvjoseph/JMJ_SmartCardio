'''
JMJPFU
13-Jan-2020
This is the driver program for the Smart Cardio Train program

Lord bless this attempt of yours
'''

import argparse
import sys
from configparser import ConfigParser
from Processing import SmartLoading
import json
import ntpath
import os
import re

print('Lord bless this attempt of yours')

print('Starting the configuration steps')

########### Configuration Arguments module #######################

# Defining the argument parsers and configuration files
ap = argparse.ArgumentParser()
ap.add_argument('--configfile',required=True,help='This is the path to the configuration file')
args = ap.parse_args()

# Getting the configuration in place

print('System arguments path',sys.argv)

sys_arguments = sys.argv
default_cfg = ConfigParser()
default_cfg.read(sys_arguments[2])

############## Data Loading and Processing module

sl = SmartLoading(default_cfg)

# Process 1 : Getting the edf_processing list and the information file

edffilePaths,edfInfofile = sl.rawLoader()

# Process 2 : Starting a loop to go through all the edffiles
## Empty containers for the data and labels
ecg_label = []
ecg_data = []

## Starting a for loop for getting all the details from the edf file
for edffilePath in edffilePaths:
    # Getting the complete path of the edf files and the edf file information from the function edfinfoReader()
    edf_list, edfInfo = sl.edfinfoReader(edffilePath, edfInfofile)
    #### @@@@ Change the list of edf_list to take all the files in the list
    for filename in edf_list[0:1]:
        # The below extracts the last component of the path which is the file name with extension .edf
        baseFilename = ntpath.basename(filename)
        # Based on the base file name extract relevant information from the information file
        edfDetails = edfInfo.loc[edfInfo['EDF'] == baseFilename]
        # Ensure that the details extracted about the edfile are not none . Based on the details extract the details of signal
        if len(edfDetails) == 0:
            continue
        # Reading the edf signals using a new function edfRead()
        sig, sigSamps = sl.edfRead(filename, edfDetails)
        print('Edf Signals read from the raw data',sigSamps.shape)
        print('Shape of the signals',sig)
        if(sig is None or sigSamps is None):
            continue
        # Get the path of the annotations
        annotPath = default_cfg.get('datafiles','annot_info')
        # Get the relevant file name and add it with the file path to get the complete path of the annotation file
        ann_file_name = annotPath + edfDetails['Annotation'].values[0]
        # Get the category also
        category = edfDetails['Category'].values[0]
        # Getting the annotations and the annotation files
        peaks, annotations = sl.makeEcgdata(ann_file_name)

        print(len(peaks),len(annotations))
        print('10 Peaks ',peaks[0:10])
        print('10 annotations',annotations[0:10])



