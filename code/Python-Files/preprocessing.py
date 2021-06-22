#!/usr/bin/env python
# coding: utf-8

# IMPORTS
import os
# Data Manipulation, Wrangling & Analysis Library 
import pandas as pd
# Multi-Dimensional Arrays and Matrices Library
import numpy as np
from IPython.display import display
# Import physical constants such as the speed of light
import scipy.constants as consts
# Support for Jupyter Lab
from jupyter_dash import JupyterDash
from jupyterthemes import jtplot
#jtplot.style(theme='solarizedd', context='notebook', ticks=True, grid=False)

# Identify column names for new DataFrame
header_names = ['#errors',
                'scan#', 
                'motor-target_1', # Motor-1 targeted motor position
                'motor-target_2', # Motor-2 targeted motor position
                'motor-actual_1', # Motor-1 actual recorded position
                'motor-actual_2', # Motor-2 actual recorded position
                'data_channel_0', 
                'data_channel_1', 
                'data_channel_2',
                'data_channel_3',
                'data_channel_4',
                'data_channel_5',
                'data_channel_6',
                'data_channel_7']

# Assign relative path
relative_path = '../../../UTPS-Data/'
# List of files in relative path directory
datasets = os.listdir(relative_path)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
print('Available Data:\n')
# Display options and prompt user selection
for d in range(len(datasets)):
    print(f'[{d+1}] {datasets[d]}')
f = int(input('\nSelect [int] from above: '))-1
# Check for valid user input
while f not in range(len(datasets)):
    f = int(input(f'Invalid entry. Enter an integer from 1 to {len(datasets)}: '))-1
# Inform user of verified data selection
print()
print(f'Selected Data: {datasets[f]}')
print()
active_data = datasets[f]
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Assign 'data', a list of DataFrames, for all 'files' dpdn menu
filename = []
for d in range(len(datasets)):
    filename.append(relative_path+datasets[d])
# Assign selection to begin analysis
filename_f = relative_path+datasets[f]
# Read tsv data and assign to a Pandas DataFrame
data = []
for d in range(len(datasets)):
    # Read each file into a Pandas DataFrame object
    df = pd.read_csv(filename[d], delimiter='\t', names = header_names)
    # Set dtype of 'scan#' column to int32
    df = df.astype({'scan#':int})
    data.append(df)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Assign the 'data_f' DataFrame for initial app loading
data_f = pd.read_csv(filename_f, delimiter='\t', names = header_names)
# Set dtype of scan# column to int32
data_f = data_f.astype({'scan#':int})
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Count the number of motor positions targeted in each scan for 'files' dpdn menu
num_m1steps = []
num_m2steps = []
for d in range(len(datasets)):
    m1steps = len(data[d]['motor-target_1'].value_counts())
    m2steps = len(data[d]['motor-target_2'].value_counts())
    num_m1steps.append(m1steps)
    num_m2steps.append(m2steps)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Count the number of motor positions targeted in each scan for initial app loading
num_m1steps_f = len(data_f['motor-target_1'].value_counts())
num_m2steps_f = len(data_f['motor-target_2'].value_counts())
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Characterize experiment scans performed for 'files' dpdn menu
scan_info = []
num_scans = []
complete = []
for d in range(len(datasets)):
    # Scan Info stores the number of measurements taken during each scan
    scan_info.append(data[d]['scan#'].value_counts().sort_index())
    # Num Scans is the total number of measurements recorded, in each scan, in each dataset (each file)
    num_scans.append(len(scan_info[d]))
    # Complete is a list of integers defining the minimum # of measurements required, in each dataset, for an individual scan to be considered complete
    complete.append(num_m1steps[d]*num_m2steps[d])
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Characterize experiment scans performed for initial app loading
# Scan Info stores the number of measurements taken during each scan
scan_info_f = data_f['scan#'].value_counts().sort_index()
# Num Scans is the total number of measurements recorded, in each scan, in each dataset (each file)
num_scans_f = len(scan_info)
# Complete is a list of integers defining the minimum # of measurements required, in each dataset, for an individual scan to be considered complete
complete_f = num_m1steps_f*num_m2steps_f
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify all complete & incomplete scans for 'files' dpdn menu
complete_scans = []
incomplete_scans = []
sigfigs = 3
for d in range(len(datasets)):
    # Create an empty list element for each dataset loaded
    complete_scans.append([])
    incomplete_scans.append([])
    for scan in range(num_scans[d]):
        if scan_info[d][scan] < complete[d]:
            incomplete_scans[d].append(scan)
        elif scan_info[d][scan] >= complete[d]:
            complete_scans[d].append(scan)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Requirements for complete scan
print(f'Complete scans have at least {num_m1steps_f*num_m2steps_f:,} measurements.\n')
print('scan# complete%')
display(round((data_f['scan#'].value_counts().sort_index()/(complete_f))*100, sigfigs-1))
print()
complete_scans_f = []
incomplete_scans_f = []
# Identify incomplete scans for initial app loading
for scan in range(num_scans_f):
    if scan_info_f[scan] < complete_f:
        incomplete_scans_f.append(scan)
    elif scan_info_f[scan] >= complete_f:
        complete_scans_f.append(scan)
print(f'INCOMPLETE scan#: {incomplete_scans_f}')
print(f'COMPLETE scan#:   {complete_scans_f}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# An error may consist of a communication error b/w motor & acquisition computer
# Motors will be reinitialized, and the scan is restarted
for d in range(len(datasets)):
    data[d]['#errors'].value_counts()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# For initial app loading
data_f['#errors'].value_counts()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor_1 Description for 'files' dpdn menu
m1_positions = []
m2_positions = []
m1_position_range = []
m2_position_range = []
for d in range(len(datasets)):
    # Creates a list of sorted lists of motor target-positions
    m1_positions.append(sorted(data[d]['motor-target_1'].unique() ) )
    m2_positions.append(sorted(data[d]['motor-target_2'].unique() ) )
    # Determine the range of all delay axes
    m1_position_min = m1_positions[d][0]
    m2_position_min = m2_positions[d][0]
    m1_position_max = m1_positions[d][-1]
    m2_position_max = m2_positions[d][-1]
    m1_position_range.append(round(m1_position_max - m1_position_min, sigfigs))
    m2_position_range.append(round(m2_position_max - m2_position_min, sigfigs))
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor_1 Description for initial app loading
print()
print(f'Motor-1 Targets: \n')
m1_positions_f = sorted(data_f['motor-target_1'].unique())
# Determine the range of Motor_1 positions
m1_position_min_f = m1_positions_f[0]
m1_position_max_f = m1_positions_f[-1]
m1_position_range_f = round(m1_position_max_f - m1_position_min_f, sigfigs)
print(f'        Min: {m1_position_min_f}[mm]\n        Max: {m1_position_max_f}[mm]\n        Range: {m1_position_range_f}[mm]')
# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m1steps_f}\n')
# Display Motor-2 Description
print(f'Motor-2 Targets: \n')
# Pre-Processing
m2_positions_f = sorted(data_f['motor-target_2'].unique())
# Determine the range of Motor_1 positions
m2_position_min_f = m2_positions_f[0]
m2_position_max_f = m2_positions_f[-1]
m2_position_range_f = round(m2_position_max_f - m2_position_min_f, sigfigs)
print(f'        Min: {m2_position_min_f}[mm]\n        Max: {m2_position_max_f}[mm]\n        Range: {m2_position_range_f}[mm]')
# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m2steps_f}\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Round to display significant figures
sigfigs = 3
# Laser travels twice the motor distance
twice = 2
# New line
nl = '\n'
# Time, in femtoseconds[fs], it takes light to travel twice the distance
# One femtosecond in [seconds]:
fs = 1E-15
# One thousand
K = int(1E3)
# Speed of light in [meters/second]
c = consts.c
# Step-size for Delay Axes for 'files' dpdn menu:
step1_space = []
step2_space = []
step1_time = []
step2_time = []
range_T = []
range_tau = []
for d in range(len(datasets)):
    # Step-size for Delay Axes: Round for sigfigs
    step1_space.append(round(m1_position_range[d]/num_m1steps[d], sigfigs))
    step2_space.append(round(m2_position_range[d]/num_m2steps[d], sigfigs))
    # Time [femtoseconds] it takes light to travel twice the distance
    step1_time.append(round((step1_space[d]*twice / (c*K))/fs, 1))
    step2_time.append(round((step2_space[d]*twice/(c*K))/fs, 1))
    # Range defined for tick labels
    range_T.append(step1_time[d]*num_m1steps[d])
    range_tau.append(step2_time[d]*num_m2steps[d])
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Step-size for Delay Axes: Round for sigfigs for initial app loading
step1_space_f = round(m1_position_range_f/num_m1steps_f, sigfigs)
step2_space_f = round(m2_position_range_f/num_m2steps_f, sigfigs)
# Time [femtoseconds] it takes light to travel twice the distance
step1_time_f = round((step1_space_f*twice / (c*K))/fs, 1)
step2_time_f = round((step2_space_f*twice/(c*K))/fs, 1)
# Time [femtoseconds] it takes light to travel twice the distance
range_T_f = step1_time_f*num_m1steps_f
range_tau_f = step2_time_f*num_m2steps_f
print(f'Motor-1 Step-Size:   {step1_space_f}[mm]  =>  ~ {step1_time_f}[fs]')
print(f'Motor-2 Step-Size:   {step2_space_f}[mm]  =>  ~ {step2_time_f}[fs]\n')
print(f'Pump-Probe  Time-Delay "T"   Range: ~{range_T_f:,}[fs]')
print(f'Drive-Probe Time-Delay "TAU" Range: ~{range_tau_f:,}[fs]\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify range of signal amplitudes for 'files' dpdn menu
signal_df = []
nchannels = []
for d in range(len(datasets)):
    data_cols = [col_name for col_name in data[d] if 'data_channel' in col_name]
    signal_df.append(data[d][data_cols])
    # WARNING: Dropping columns in signal_df will remove those channels from the figure display
    nchannels.append(len(signal_df[d].columns))
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify range of signal amplitudes for initial app loading
data_cols_f = [col_name for col_name in data_f if 'data_channel' in col_name]
signal_df_f = data_f[data_cols_f]
# WARNING: Dropping columns in signal_df will remove those channels from the figure display
nchannels_f = len(signal_df_f.columns)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify the max and min signal strength
v_min_f = min(signal_df_f.min())
v_max_f = max(signal_df_f.max())
print(f'Signal Min: {v_min_f}\nSignal Max: {v_max_f}\n')
signal_mins_f = []
signal_maxs_f = []
for col in signal_df_f.columns:
    signal_mins_f.append(round(min(signal_df_f[col]),4))
    signal_maxs_f.append(round(max(signal_df_f[col]),4))
print(f'Signal Minimums by channel: {signal_mins_f}')
print(f'Signal Maximums by channel: {signal_maxs_f}\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Initialize a list of dictionaries for mapping experimental scans to columns for each file in data repo
data_dict = []
for d in range(len(datasets)):
    # Set-up lists to store delay scan DataFrames for each channel (0-7)
    data_to_plot = []
    # Average all scans together
    data_mean = data[d].groupby(['motor-target_1', 'motor-target_2']).mean()
    # data_to_plot
    for channel in range(nchannels[d]):
        # Append data for each channel
        data_to_plot.append(data_mean['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
        # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
        data_to_plot[channel].columns = data_to_plot[channel].columns.droplevel(0)
    # Initialize 'data dictionary' to keep track of all complete scans and the average of all scans(A.K.A 'data_mean')
    data_dict.append({'scan_avg':data_to_plot})
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set-up lists to store delay scan DataFrames for each channel (0-7)
data_to_plot_f = []

# Average all scans together
data_mean_f = data_f.groupby(['motor-target_1', 'motor-target_2']).mean()

# data_to_plot
for channel in range(nchannels_f):
    # Append data for each channel
    data_to_plot_f.append(data_mean_f['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
    
    # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
    data_to_plot_f[channel].columns = data_to_plot_f[channel].columns.droplevel(0)
    
# Initialize 'data dictionary' to keep track of all complete scans and the average of all scans(A.K.A 'data_mean')
data_dict_f = {'scan_avg':data_to_plot_f}
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
for d in range(len(datasets)):
    # Now append each individual complete scan
    for scan in complete_scans[d]:
        dummy_scan_list = []
        data_scan = data[d][data[d]['scan#']==scan].copy()
        data_scan = data_scan.groupby(['motor-target_1', 'motor-target_2']).mean().copy()
        
        for channel in range(nchannels[d]):
            # Append data for each channel
            dummy_scan_list.append(data_scan['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
            # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
            dummy_scan_list[channel].columns = dummy_scan_list[channel].columns.droplevel(0)
        # Append scan to data_dict
        data_dict[d]['scan#'+str(scan)] = dummy_scan_list
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Now append each individual complete scan
for scan in complete_scans_f:
    dummy_scan_list = []
    data_scan = data_f[data_f['scan#']==scan].copy()
    data_scan = data_scan.groupby(['motor-target_1', 'motor-target_2']).mean().copy()
    
    for channel in range(nchannels_f):
        # Append data for each channel
        dummy_scan_list.append(data_scan['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
        # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
        dummy_scan_list[channel].columns = dummy_scan_list[channel].columns.droplevel(0)
    # Append scan to data_dict
    data_dict_f['scan#'+str(scan)] = dummy_scan_list
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# END preprocessing.py
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
