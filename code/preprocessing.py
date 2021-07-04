#!/usr/bin/env python

# IMPORTS:
import os
import pandas as pd # Data Manipulation, Wrangling & Analysis Library
import numpy as np # Multi-Dimensional Arrays and Matrices Library
import scipy.constants as consts # Import physical constants such as the speed of light

# CONSTANTS
sigfigs = 3 # Supports readability & proper time conversion
twice = 2 # Laser travels twice the motor distance
fs = 1E-15 # One femtosecond in [seconds]
K = int(1E3) # One thousand
c = consts.c # Speed of light: 299792458.0[meters/second]

# COLUMN NAMES FOR NEW Pandas DataFrame
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
#relative_path = '../../UTPS-Data/'
relative_path = '../data/'

# List of files in relative path directory
datasets = os.listdir(relative_path)

# Determine which file 'f' to analyze
print('Available Data:\n')
# Display options and prompt user selection
for d in range(len(datasets)):
    print(f'[{d}] {datasets[d]}')

# Assign selection to begin analysis
# f = int(input('\nSelect [int] from above: '))
f = 0

# Check for valid user input
#while f not in range(len(datasets)):
#    f = int(input(f'Invalid entry. Enter an integer from 0 to {len(datasets)}: '))
# Inform user of verified data selection
#print(f'\nSelected Data: [{f}] {datasets[f]}\n')

# DISPLAY DATASET SUMMARY
print('Data Synopsis:\n')
active_data = datasets[f]

# Assign 'data', a list of DataFrames, for all 'files' dpdn menu
filename = []
for d in range(len(datasets)):
    filename.append(relative_path+datasets[d])
# Read tsv data and assign to a Pandas DataFrame
data = []
for d in range(len(datasets)):
    # Read each file into a Pandas DataFrame object
    df = pd.read_csv(filename[d], delimiter='\t', names = header_names)
    # Set data type of both 'scan#' & '#errors' columns to int32
    df = df.astype({'scan#':int})
    df = df.astype({'#errors':int})
    data.append(df)
# Count the number of motor positions targeted in each scan for 'files' dpdn menu
num_m1steps = []
num_m2steps = []
# Characterize experiment scans performed for 'files' dpdn menu
scan_info = []
complete = []
num_scans = []
# Identify all complete & incomplete scans for 'files' dpdn menu
complete_scans = []
incomplete_scans = []
# Target Motor Positions
m1_positions = []
m2_positions = []
m1_position_range = []
m2_position_range = []
# Step-size for Delay Axes for 'files' dpdn menu:
step1_space = []
step2_space = []
# Time it takes light to travel the step-size distance
step1_time = []
step2_time = []
range_T = []
range_tau = []
# Characterize data for initial app loading
for d in range(len(datasets)):
    # Count the number of motor positions targeted in each scan for initial app loading
    m1steps = len(data[d]['motor-target_1'].value_counts())
    m2steps = len(data[d]['motor-target_2'].value_counts())
    num_m1steps.append(m1steps)
    num_m2steps.append(m2steps)
    # Complete is a list of integers defining the minimum # of measurements required, in each dataset, for each scan to be considered complete
    complete.append(num_m1steps[d]*num_m2steps[d])
    # Number of measurements taken during each trial scan
    scan_info.append(data[d]['scan#'].value_counts().sort_index())
    # Number of Scans is the total number of times the experiment was repeated in each dataset (each file)
    num_scans.append(len(scan_info[d]))
    # Create an empty list element for each dataset loaded
    complete_scans.append([])
    incomplete_scans.append([])
    # Identify the incomplete scans
    for scan in range(num_scans[d]):
        # Identify the incomplete scans
        if scan_info[d][scan] < complete[d]:
            incomplete_scans[d].append(scan)
        # Identify the complete scans
        elif scan_info[d][scan] >= complete[d]:
            complete_scans[d].append(scan)
    # List of lists: sorted target-positions of delay-axis motors
    m1_positions.append(sorted(data[d]['motor-target_1'].unique() ) )
    m2_positions.append(sorted(data[d]['motor-target_2'].unique() ) )
    # Temporary variables for readability
    m1_position_min = m1_positions[d][0]
    m2_position_min = m2_positions[d][0]
    m1_position_max = m1_positions[d][-1]
    m2_position_max = m2_positions[d][-1]
    # Determine the range of all delay axes
    m1_position_range.append(round(m1_position_max - m1_position_min, sigfigs)) # What is the precision of the delay stage motor?
    m2_position_range.append(round(m2_position_max - m2_position_min, sigfigs)) # precision: 0.001 [mm] or one micron
    # Step-size for Delay Axes: Round for sigfigs
    step1_space.append(round(m1_position_range[d]/num_m1steps[d], sigfigs))
    step2_space.append(round(m2_position_range[d]/num_m2steps[d], sigfigs))
    # Time [femtoseconds] it takes light to travel twice the distance
    step1_time.append(round((step1_space[d]*twice / (c*K))/fs, 1)) # rounded to 3 significant figures (1 decimal)
    step2_time.append(round((step2_space[d]*twice/(c*K))/fs, 1)) # Precision limited by stepx_space, with only 3 sigfigs
    # Range defined for tick labels
    range_T.append(step1_time[d]*num_m1steps[d])
    range_tau.append(step2_time[d]*num_m2steps[d])

    # Display the number of measurements taken in each scan
    print(f'dataset: [{d}] {datasets[d]}')
    print(f'\tNo. of M1 Steps: {num_m1steps[d]}')
    print(f'        \tMin: {m1_position_min}[mm]\n        \tMax: {m1_position_max}[mm]\n        \tStep-Size:  {step1_space[d]}[mm]  =>  ~ {step1_time[d]}[fs]')
    print(f'        \tScan width: {m1_position_range[d]}[mm]  =>  ~ {range_T[d]:,}[fs]\n')
    print(f'\tNo. of M2 Steps: {num_m2steps[d]}')
    print(f'        \tMin: {m2_position_min}[mm]\n        \tMax: {m2_position_max}[mm]\n        \tStep-Size:  {step2_space[d]}[mm]  =>  ~ {step2_time[d]}[fs]')
    print(f'        \tScan Width: {m2_position_range[d]}[mm]  =>  ~ {range_tau[d]:,}[fs]\n')
    print(f'\tNo. of Experimental Scans observed: {num_scans[d]}')

    # Display requirements for complete scan
    print(f'\tComplete scans have at least {complete[d]:,} measurements.\n')
    print(f'\tINCOMPLETE scan#: {incomplete_scans[d]}')
    print(f'\tCOMPLETE scan#:   {complete_scans[d]}\n')

    # An error may consist of a communication error b/w motor & acquisition computer
    # Motors will be reinitialized, and the scan is restarted
    print('\tDAQ Errors:')
    count = 0
    dff = data[d].copy()
    # For each scan, in each data file:
    for scan in dff['scan#'].unique():
        dff_scan = dff[ dff['scan#']==scan ].copy()
        dff_errors = dff_scan['#errors'].copy()
        if (len(dff_errors.unique())>1):
            count+=1
            print(f'\t\tScan-{scan} Measurements')
            error_counts = dff_errors.value_counts().sort_index()
            for e in range(len(error_counts)):
                print(f'\t\t\terror#-{error_counts.index[e]}: {error_counts.values[e]:,}')
            #print()
    if count == 0:
        print('\t\tNone found.')
    print()
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
# END preprocessing.py
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=