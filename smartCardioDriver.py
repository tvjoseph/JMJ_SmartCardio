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

# Getting the edf_processing list and the information file

edf_list,edfInfo = sl.rawLoader()
print('Edf total list',len(edf_list))
print(edfInfo.head(3))