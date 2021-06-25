#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# IMPORTS:

# Library containing component classes for HTML tags
import dash_html_components as html
# Bootstrap components for Dash to customise CSS theme & grid layout
import dash_bootstrap_components as dbc
import dash_core_components as dcc # Library of dashboarding components
import preprocessing as pp
#=======================================================================================================================================================
# App layout:
# 1. Dash-Bootstrap Components(i.e. rows, cols, dropdown menus, radioItems, tabs etc.)
# 2. Any HTML needed in there (i.e Div, H1)
#=======================================================================================================================================================
layout1 = dbc.Container([
    dbc.Row([
        dbc.Col(
            # Add a title(H1) on the webpage aligned to the center of the page
            html.H2(['Ultrafast Transient Polarization Spectroscopy', dbc.Badge('UTPS', className='ml-1')]), width={'size': 'auto', 'order': 'last', 'offset': 0},
        ),
        dbc.Col(
            # Adds button for dynamic callback to make subplot
            html.Div([ dbc.Button('Subplots', id='add_graph', n_clicks=0, outline = False, size='sm') ] ), width={'size': 'auto', 'order': 2, 'offset': 0},
            ),
        # Dataset Dropdown Column
        dbc.Col([
            dcc.Store(id='memory-data', storage_type='memory'),
            #dbc.Label( 'filename:', id='datasets1', size='sm', html_for='files1'),
            dbc.DropdownMenu(id = 'files', children = [
                dbc.DropdownMenuItem(d, id = f'filename{idx}', active=(d==pp.datasets[0])) for idx, d in enumerate(pp.datasets)
                ],
                label='Data ', bs_size="sm", direction='down',
                ),
            #dbc.FormText(f'Available Data', color='secondary'),
            ], width={'size':'auto', 'order':'first'} # END of dbc.Col children = [ datasets, files, filename{idx} ]
        ) # END of COL
    ]),
    # All graphs/components go into this empty list: 'children'
    html.Div(id='container', children=[])
    ], fluid=True) # END of app.layout(...)
#=======================================================================================================================================================
#=======================================================================================================================================================
#=======================================================================================================================================================
#!/usr/bin/env python
# coding: utf-8

# IMPORTS
import os
import pandas as pd # Data Manipulation, Wrangling & Analysis Library 
import numpy as np # Multi-Dimensional Arrays and Matrices Library
import scipy.constants as consts # Import physical constants such as the speed of light

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
f = 0
active_data = datasets[f]
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

# Count the number of motor positions targeted in each scan for 'files' dpdn menu
num_m1steps = [], num_m2steps = []
for d in range(len(datasets)):
    m1steps = len(data[d]['motor-target_1'].value_counts())
    m2steps = len(data[d]['motor-target_2'].value_counts())
    num_m1steps.append(m1steps)
    num_m2steps.append(m2steps)

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

# Identify all complete & incomplete scans for 'files' dpdn menu
complete_scans = []
incomplete_scans = []
# Round to display significant figures
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

# An error may consist of a communication error b/w motor & acquisition computer
# Motors will be reinitialized, and the scan is restarted
for d in range(len(datasets)):
    data[d]['#errors'].value_counts()

# Display Motor_1 Description for 'files' dpdn menu
m1_positions = [], m2_positions = []
m1_position_range = [], m2_position_range = []
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

# Time, in femtoseconds[fs], it takes light to travel twice the distance
twice = 2 # Laser travels twice the motor distance
fs = 1E-15 # Conversion: 1[fs] to [secs]
K = int(1E3) # One thousand
c = consts.c # Speed of light in [meters/second]

# Step-size for Delay Axes for 'files' dpdn menu:
step1_space = [], step2_space = []
step1_time = [], step2_time = []
range_T = [], range_tau = []
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

# Identify range of signal amplitudes for 'files' dpdn menu
signal_df = []
nchannels = []
for d in range(len(datasets)):
    data_cols = [col_name for col_name in data[d] if 'data_channel' in col_name]
    signal_df.append(data[d][data_cols])
    # WARNING: Dropping columns in signal_df will remove those channels from the figure display
    nchannels.append(len(signal_df[d].columns))

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

for d in range(len(datasets)):
    # Now append each individual complete scan
    for scan in complete_scans[d]:
        dummy_scan_list = []
        data_scan = data[d][data[d]['scan#']==scan].copy()
        data_scan = data_scan.groupby(['motor-target_1', 'motor-target_2']).mean().copy()
        # 
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
