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
a = int(input('\nSelect [int] from above: '))-1
# Check for valid user input
while a not in range(len(datasets)):
    a = int(input(f'Invalid entry. Enter an integer from 1 to {len(datasets)}: '))-1
# Inform user of verified data selection
print()
print(f'Selected Data: {datasets[a]}')
print()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Prepare for a future data selection change
filename = []
for d in range(len(datasets)):
    filename.append(relative_path+datasets[d])

# Assign selection to begin analysis
filename_a = relative_path+datasets[a]

# Read tsv data and assign to a Pandas DataFrame
data = []
for d in range(len(datasets)):
    # Read each file into a Pandas DataFrame object
    df = pd.read_csv(filenames[d], delimiter='\t', names = header_names)
    # Set dtype of 'scan#' column to int32
    df = df.astype({'scan#':int})
    data.append(df)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
data_a = pd.read_csv(filename, delimiter='\t', names = header_names)
# Set dtype of scan# column to int32
data_a = data_a.astype({'scan#':int})
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Count the number of motor positions targeted in each scan
num_m1steps = []
num_m2steps = []
for d in range(len(datasets)):
    m1steps = len(datas[d]['motor-target_1'].value_counts())
    m2steps = len(datas[d]['motor-target_2'].value_counts())
    num_m1steps.append(m1steps)
    num_m2steps.append(m2steps)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Count the number of motor positions targeted in each scan
num_m1steps_a = len(data_a['motor-target_1'].value_counts())
num_m2steps_a = len(data_a['motor-target_2'].value_counts())
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify # of complete scans performed
scan_info = []
num_scans = []
complete = []
for d in range(len(datasets)):
    scan_info.append(datas[d]['scan#'].value_counts().sort_index())
    num_scans.append(len(scan_info[d]))
    complete.append(num_m1steps[d]*num_m2steps[d])
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify # of complete scans performed
scan_info_a = data_a['scan#'].value_counts().sort_index()
num_scans_a = len(scan_info)
complete_a = num_m1steps_a*num_m2steps_a
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
complete_scans = []
incomplete_scans = []
sigfigs = 3
# Identify all incomplete scans
for d in range(len(datasets)):
    for scan in range(num_scans[d]):
        if scan_info[d][scan] < complete[d]:
            incomplete_scans.append(scan)
        elif scan_info[d][scan] == complete[d]:
            complete_scans.append(scan)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Requirements for complete scan
print(f'Complete scans have at least {num_m1steps_a*num_m2steps_a:,} measurements.\n')
print('scan# complete%')
display(round((data_a['scan#'].value_counts().sort_index()/(complete))*100, sigfigs-1))
print()
complete_scans_a = []
incomplete_scans_a = []
# Identify incomplete scans
for scan in range(num_scans_a):
    if scan_info_a[scan] < complete_a:
        incomplete_scans_a.append(scan)
    elif scan_info_a[scan] == complete_a:
        complete_scans_a.append(scan)
print(f'INCOMPLETE scan#: {incomplete_scans_a}')
print(f'COMPLETE scan#:   {complete_scans_a}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# An error may consist of a communication error b/w motor & acquisition computer
# Motors will be reinitialized, and the scan is restarted
for d in range(len(datasets)):
    data[d]['#errors'].value_counts()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
data_a['#errors'].value_counts()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor_1 Description
m1_positions = []
m2_positions = []
m1_position_range = []
m2_position_range = []
for d in range(len(datasets)):
    # Creates a list of sorted lists of motor target-positions
    m1_positions.append(sorted(data[d]['motor-target_1'].unique() ) )
    m2_positions.append(sorted(data[d]['motor-target_2'].unique() ) )
    # Determine the range of all delay axes
    m1_position_min = m1_positions[0]
    m2_position_min = m2_positions[0]
    m1_position_max = m1_positions[-1]
    m2_position_max = m2_positions[-1]
    m1_position_range.append(round(m1_position_max - m1_position_min, sigfigs))
    m2_position_range.append(round(m2_position_max - m2_position_min, sigfigs))
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor_1 Description
print()
print(f'Motor-1 Targets: \n')
m1_positions_a = sorted(data_a['motor-target_1'].unique())
# Determine the range of Motor_1 positions
m1_position_min_a = m1_positions_a[0]
m1_position_max_a = m1_positions_a[-1]
m1_position_range_a = round(m1_position_max_a - m1_position_min_a, sigfigs)
print(f'        Min: {m1_position_min_a}[mm]\n        Max: {m1_position_max_a}[mm]\n        Range: {m1_position_range_a}[mm]')
# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m1steps_a}\n')
# Display Motor-2 Description
print(f'Motor-2 Targets: \n')
# Pre-Processing
m2_positions_a = sorted(data_a['motor-target_2'].unique())
# Determine the range of Motor_1 positions
m2_position_min_a = m2_positions_a[0]
m2_position_max_a = m2_positions_a[-1]
m2_position_range_a = round(m2_position_max_a - m2_position_min_a, sigfigs)
print(f'        Min: {m2_position_min_a}[mm]\n        Max: {m2_position_max_a}[mm]\n        Range: {m2_position_range_a}[mm]')
# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m2steps_a}\n')
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
# Step-size for Delay Axes:
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
# Step-size for Delay Axes: Round for sigfigs
step1_space_a = round(m1_position_range_a/num_m1steps_a, sigfigs)
step2_space_a = round(m2_position_range_a/num_m2steps_a, sigfigs)
# Time [femtoseconds] it takes light to travel twice the distance
step1_time_a = round((step1_space_a*twice / (c*K))/fs, 1)
step2_time_a = round((step2_space_a*twice/(c*K))/fs, 1)
# Time [femtoseconds] it takes light to travel twice the distance
range_T_a = step1_time_a*num_m1steps_a
range_tau_a = step2_time_a*num_m2steps_a
print(f'Motor-1 Step-Size:   {step1_space_a}[mm]  =>  ~ {step1_time_a}[fs]')
print(f'Motor-2 Step-Size:   {step2_space_a}[mm]  =>  ~ {step2_time_a}[fs]\n')
print(f'Pump-Probe  Time-Delay "T"   Range: ~{range_T_a:,}[fs]')
print(f'Drive-Probe Time-Delay "TAU" Range: ~{range_tau_a:,}[fs]\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify range of signal amplitudes
signal_df = []
nchannels = []
for d in range(len(datasets)):
    data_cols = [col_name for col_name in data[d] if 'data_channel' in col_name]
    signal_df.append(data[d][data_cols])
    # WARNING: Dropping columns in signal_df will remove those channels from the figure display
    nchannels.append(len(signal_df[d].columns))
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify range of signal amplitudes
data_cols_a = [col_name for col_name in data_a if 'data_channel' in col_name]
signal_df_a = data_a[data_cols_a]
# WARNING: Dropping columns in signal_df will remove those channels from the figure display
nchannels_a = len(signal_df_a.columns)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify the max and min signal strength
v_min = min(signal_df.min())
v_max = max(signal_df.max())

print(f'Signal Min: {v_min}\nSignal Max: {v_max}\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
signal_mins = []
signal_maxs = []
for col in signal_df.columns:
    signal_mins.append(round(min(signal_df[col]),4))
    signal_maxs.append(round(max(signal_df[col]),4))
print(f'Signal Minimums by channel: {signal_mins}')
print(f'Signal Maximums by channel: {signal_maxs}\n')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set-up lists to store delay scan DataFrames for each channel (0-7)
data_to_plot = []

# Average all scans together
data_mean = data.groupby(['motor-target_1', 'motor-target_2']).mean()

# data_to_plot
for channel in range(nchannels):
    # Append data for each channel
    data_to_plot.append(data_mean['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
    
    # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
    data_to_plot[channel].columns = data_to_plot[channel].columns.droplevel(0)
    
# Initialize 'data dictionary' to keep track of all complete scans and the average of all scans(A.K.A 'data_mean')
data_dict = {'scan_avg':data_to_plot}
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
for scan in complete_scans:
    dummy_scan_list = []
    data_scan = data[data['scan#']==scan].copy()
    data_scan = data_scan.groupby(['motor-target_1', 'motor-target_2']).mean().copy()
    
    for channel in range(nchannels):
        # Append data for each channel
        dummy_scan_list.append(data_scan['data_channel_'+str(channel)].reset_index().pivot(index='motor-target_2', columns='motor-target_1'))
        # Rename multi-indexed columns so they are not tuples of the format ('data_channel_x', <motor-target_1>)
        dummy_scan_list[channel].columns = dummy_scan_list[channel].columns.droplevel(0)
    # Append scan to data_dict
    data_dict['scan#'+str(scan)] = dummy_scan_list
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# END preprocessing.py
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
