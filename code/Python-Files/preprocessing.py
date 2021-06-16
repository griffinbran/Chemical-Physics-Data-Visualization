#!/usr/bin/env python
# coding: utf-8

# Data Manipulation, Wrangling & Analysis Library 
import pandas as pd
# Multi-Dimensional Arrays and Matrices Library
import numpy as np
from IPython.display import display
# Import physical constants such as the speed of light
import scipy.constants as consts

from jupyter_dash import JupyterDash
from jupyterthemes import jtplot
#jtplot.style(theme='solarizedd', context='notebook', ticks=True, grid=False)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
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

# Read tsv data and assign to a Pandas DataFrame
data = pd.read_csv('../../data/trial_output05.tsv', delimiter='\t', names = header_names)

# Set dtype of scan# column to int32
data = data.astype({'scan#':int})
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify # of complete scans performed
scan_info = data['scan#'].value_counts().sort_index()
num_scans = len(scan_info)
complete = max(scan_info)
complete_scans = []
incomplete_scans = []

# Count the number of measurements taken in each scan
num_m1steps = len(data['motor-target_1'].value_counts())
# Count the number of measurements taken in each scan
num_m2steps = len(data['motor-target_2'].value_counts())

# Requirements for complete scan
print(f'Complete scans have {num_m1steps*num_m2steps:,} measurements!\n')

print('scan# complete%')
display(round((data['scan#'].value_counts().sort_index()/(num_m1steps*num_m2steps))*100, 2))
print()

# Identify incomplete scans
for scan in range(num_scans):
    if scan_info[scan] != complete:
        incomplete_scans.append(scan)
    elif scan_info[scan] == complete:
        complete_scans.append(scan)
print(f'INCOMPLETE scan#: {incomplete_scans}')
print(f'COMPLETE scan#:   {complete_scans}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# No errors identified in 45,628 measurements!
# An error may consist of a communication error b/w motor & acquisition computer
# Motors will be reinitialized, and the scan is restarted
data['#errors'].value_counts()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor_1 Description
print(f'Motor-1 Targets: \n')

# Pre-Processing
m1_positions = sorted(data['motor-target_1'].unique())

# Determine the range of Motor_1 positions
m1_position_min = m1_positions[0]
m1_position_max = m1_positions[-1]
m1_position_range = round(m1_position_max - m1_position_min,3)

print(f'        Min: {m1_position_min}[mm]\n        Max: {m1_position_max}[mm]\n        Range: {m1_position_range}[mm]')

# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m1steps}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Display Motor-2 Description
print(f'Motor-2 Targets: \n')

# Pre-Processing
m2_positions = sorted(data['motor-target_2'].unique())

# Determine the range of Motor_1 positions
m2_position_min = m2_positions[0]
m2_position_max = m2_positions[-1]
m2_position_range = round(m2_position_max - m2_position_min, 3)

print(f'        Min: {m2_position_min}[mm]\n        Max: {m2_position_max}[mm]\n        Range: {m2_position_range}[mm]')

# Display the number of measurements taken in each scan
print(f'\tNo. of Steps: {num_m2steps}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Step-size for Delay Axis-1: Round for sigfigs
sigfigs = 3
nl = '\n'
step1_space = round(m1_position_range/num_m1steps, sigfigs)

# Time, in femtoseconds[fs], it takes light to travel twice the distance 'step_1'
# One femtosecond in [seconds]:
fs = 1E-15
# One thousand
K = int(1E3)
# Speed of light in [meters/second]
c = consts.c
# Laser travels twice the motor distance
twice = 2

step1_time = round((step1_space*twice / (c*K))/fs, 1)
range_T = step1_time*num_m1steps

print(f'Motor-1 Step-Size:   {step1_space}[mm]  =>  ~ {step1_time}[fs]')
print(f'Pump-Probe Time-Delay "T" Range:  ~{range_T:,}[fs]')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Step-size for Delay Axis-2: Round for sigfigs
sigfigs = 3
step2_space = round(m2_position_range/num_m2steps, sigfigs)

# Time [femtoseconds] it takes light to travel twice the distance 'step_2'
step2_time = round( (step2_space*twice/(c*K))/fs, 1)
range_tau = step2_time*num_m2steps

print(f'Motor-2  Step-Size:   {step2_space}[mm]  =>   ~ {step2_time}[fs]')
print(f'Drive-Probe Time-Delay "TAU" Range: ~{range_tau:,}[fs]')
print(f'Drive-Probe Time-Delay "$\tau$" Range: ~{range_tau:,}[fs]')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Identify range of signal amplitudes
data_cols = [col_name for col_name in data if 'data_channel' in col_name]
signal_df = data[data_cols]

# WARNING: Dropping columns in signal_df will remove those channels from the figure display
nchannels = len(signal_df.columns)

# Identify the max and min signal strength
v_min = min(signal_df.min())
v_max = max(signal_df.max())

print(f'Minimum: {v_min}\nMaximum: {v_max}')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
signal_mins = []
signal_maxs = []
for col in signal_df.columns:
    signal_mins.append(round(min(signal_df[col]),4))
    signal_maxs.append(round(max(signal_df[col]),4))
print(f'Signal Minimums by channel: {signal_mins}')
print(f'Signal Maximums by channel: {signal_maxs}')
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
import plotly.express as px
colors = px.colors.qualitative.Plotly
print(colors)
