#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# IMPORTS:
import dash
import preprocessing as pp
from preprocessing import step1_space, step2_space, step1_time, step2_time, m1_positions, m2_positions, data_dict
from app import app
import layouts as lay

# Data Manipulation, Wrangling & Analysis Library 
import pandas as pd
# Multi-Dimensional Arrays and Matrices Library
import numpy as np
from IPython.display import display

# Figures serialized to JSON & rendered by Plotly.js JavaScript library
import plotly.express as px
import plotly.graph_objects as go

# Make subplots: In this app this is only used to display secondary_y axes
from plotly.subplots import make_subplots

# DAQ simplifies integration of data acquisition & controls into Dash
import dash_daq as daq
# Library of dashboarding components
import dash_core_components as dcc
# Library containing component classes for HTML tags
import dash_html_components as html
# Bootstrap components for Dash to customise CSS theme & grid layout
import dash_bootstrap_components as dbc
# Library for building component interactivity through callbacks
from dash.dependencies import Input, Output, State, ALL, MATCH, ALLSMALLER
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set hmap magnification, fixed ratio
mag_factor = 9
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set positioning & display of dashboard
@app.callback(Output({'type':'new_graph_container', 'index':MATCH}, 'style'),
    Input('add_graph','n_clicks'))
def render_child_div(graph_clicks):
    if (graph_clicks == 0):
        style={'width':'auto', 'outline': 'thin lightgrey solid', 'padding':5} 
    elif (graph_clicks > 0):
        style={'width':'auto', 'outline': 'thin lightgrey solid', 'margin-bottom':10,'margin-right':10, 'padding':5, 'display': 'inline-block'}
    return style
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Add tabs to the dashboard
@app.callback(Output('container', 'children'),

    Input('add_graph', 'n_clicks'),
    State('container', 'children')
    )
def add_subplot(graph_clicks, container_children):
    new_graph = dbc.Container(id={'type':'new_graph_container', 'index': graph_clicks},
        style={},       
        children=[
            # FIRST ROW
            dbc.Row(dbc.Col(dbc.Label('Time-Zero Location'))),
            # SECOND ROW
            dbc.Row([
            #=======================================================================================================================================================
            # Time-overlap Input Fields:
            #=======================================================================================================================================================
            # Style the Dashboard with HTML Div
            dbc.Col(style={'width':185, 'display':'inline-block', 'padding-bottom':0, 'margin-bottom':0}, width = 3,
                children = [
                    dbc.Label( 'Delay Axis 1:', id={'type':'taxis1_container', 'index': graph_clicks}, size='sm', html_for='slct_timeaxis1'),
                    dbc.InputGroup(id = 'm1', children=[
                        dbc.InputGroupAddon('T = 0', addon_type='prepend'),
                        # Add Input Button for Motor-1 Time-0 Selection
                        dbc.Input(id={'type': 'slct_timeaxis1', 'index': graph_clicks},
                            bs_size = 'sm',
                            debounce=False,
                            inputMode = 'numeric',
                            list='motor1_positions',
                            #max = m1_positions[-1],
                            #min = m1_positions[0],
                            name = 'input_t1',
                            persistence = True,
                            persistence_type = 'memory',
                            persisted_props = ['value'],
                            placeholder = 'Pump-Probe',
                            #required = True,
                            step = 0.001, #step1_space, ADD step-size button?
                            type = 'number',
                            value=m1_positions[-1], # None returns error " unsupported operand type(s) for -: 'float' and 'NoneType' "
                        ), # END 'slct_timeaxis1' dcc.Input
                        #dbc.InputGroupAddon('[mm]', addon_type='append'),
                    ], className='mb-0', size='sm'), # END InputGroup
                    dbc.Tooltip(f'Scan Range: [{m1_positions[0]}, {m1_positions[-1]}]', target = 'm1'),
                    dbc.FormText('Pump-Probe Delay', color='secondary'),
                ] # END of dbc.Col_children = [ slct_timeaxis1 ]
            ), # END of dbc.Col <taxis1> 

            # Add Dropdown Menu for Motor-2 Time-0 Selection
            dbc.Col(style={'width':185, 'display':'inline-block', 'margin-left':10}, width = 3,
                children = [
                    dbc.Label( 'Delay Axis 2:', id={'type':'taxis2_container', 'index': graph_clicks}, size='sm', html_for='slct_timeaxis2'),
                    dbc.InputGroup(id = 'm2', children = [
                        dbc.InputGroupAddon('\N{MATHEMATICAL ITALIC SMALL TAU} = 0', addon_type='prepend'),
                        # Add Input Button for Motor-2 TAU-0 Selection
                        dbc.Input(id={'type': 'slct_timeaxis2', 'index': graph_clicks},
                            bs_size = 'sm',
                            debounce=False,
                            inputMode = 'numeric',
                            list = 'motor2_positions',
                            #max = m2_positions[-1],
                            #min = m2_positions[0],
                            name = 'input_t2',
                            persistence = True,
                            persistence_type = 'memory',
                            persisted_props = ['value'],
                            placeholder = 'Drive-Probe',
                            #required = True,
                            step = 0.001, #step2_space, ADD step-size button?
                            type='number',
                            value=m2_positions[-1], # None returns error " unsupported operand type(s) for -: 'float' and 'NoneType' "
                        ),  # END 'slct_timeaxis2' dash-core-components-Input
                        #dbc.InputGroupAddon('[mm]', addon_type='append'),
                    ], className='mb-0', size='sm'), # m-margin, b-bottom
                    dbc.Tooltip(f'Scan Range: [{m2_positions[0]}, {m2_positions[-1]}]', target = 'm2'),
                    dbc.FormText('Drive-Probe Delay', color='secondary'),
                ] # END of dbc.Col children = [ slct_timeaxis2 ]
            ), # END of <taxis2> dbc.Col
            # Dataset Dropdown Column
            dbc.Col([
                dbc.Label( 'filename:', id={'type':'datasets', 'index': graph_clicks}, size='sm', html_for='data-dpdn'),
                dbc.DropdownMenu(
                    children = lay.data_dpdn_items, label='Files', bs_size="sm", direction='down',
                    ),
                dbc.FormText(f'Available Data', color='secondary'),
                ], width={'order':'last'} # END of dbc.Col children = [ datasets, data-dpdn ]
            ) # END of data-dpdn COL
            ]), # END of SECOND ROW
            #=======================================================================================================================================================
            # TABS LAYOUT
            #=======================================================================================================================================================
            # Add tabs to the dashboard
            dbc.Tabs(id={'type': 'tabs', 'index': graph_clicks},
                active_tab='tab-1',
                children=[
                    #===========================================================================================================================================================================
                    # Tab-1 Layout
                    #===========================================================================================================================================================================
                    dbc.Tab(id={'type':'hmap', 'index':graph_clicks}, label='2D Heatmap', tab_id='tab-1', tabClassName='ml-auto', children = [# tab_id(dbc.Tab) == value(dcc.Tab)  tab_style={'margin-top':-10},
                        # FIRST ROW
                        dbc.Row(
                            [
                                # FIRST COL
                                dbc.Col(
                                    # Channel Select Dropdown Menu for TAB-1
                                    dcc.Dropdown(
                                        id={'type': 'slct_channel', 'index': graph_clicks},
                                        options=[{'label': f'Channel {ch}', 'value': ch} for ch in range(pp.nchannels)],
                                        multi=False,
                                        value=0,
                                        clearable = False,
                                        persistence = True,
                                        persistence_type = 'memory',
                                        persisted_props = ['value'],
                                        ),
                                    width=3),
                                # SEC COL
                                dbc.Col(
                                    # Scan Select Dropdown Menu for TAB-1
                                    dcc.Dropdown(
                                        id={'type': 'slct_scan', 'index': graph_clicks},
                                        options=
                                            [
                                                {'label': list(data_dict.keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'), 'value': list(data_dict.keys())[scn]} for scn in range(len(data_dict))
                                            ],
                                        multi=False,
                                        value=list(data_dict.keys())[0],
                                        clearable = False,
                                        persistence = True,
                                        persistence_type = 'memory',
                                        persisted_props = ['value'],
                                    ), # END 'slct_scan' Dropdown
                                width=3), # END 'slct_scan' COL
                            ], justify='start', style={'padding':5}, # END ROW children  'start', 'center', 'end', 'stretch', 'baseline'
                        ), # END FIRST ROW
                        # START SECOND ROW
                        dbc.Row([ # html.Div([
                            # FIRST COL
                            dbc.Col([ # html.Div([
                                # This is where the 2D Heatmap is displayed
                                dcc.Graph(id={'type': '2d_scan_surf', 'index': graph_clicks}, figure={}),
                            #], className='five columns', style={'display':'inline-block', 'vertical-align':'top'}),
                            ], width='auto', align='center'),
                            # SEC COL
                            dbc.Col([ # html.Div([
                                # Slider controls the signal range displayed with colorbar
                                dcc.RangeSlider(id={'type': 'signal_range', 'index': graph_clicks},
                                    marks={},
                                    value=[],
                                    updatemode='drag',
                                    allowCross= False,
                                    included = True,
                                    #dots = True,
                                    tooltip = {'always_visible':False, 'placement':'topLeft'},
                                    vertical=True,
                                    verticalHeight=(pp.num_m2steps*(mag_factor-1)),
                                    persistence = True,
                                    persistence_type = 'memory',
                                    persisted_props = ['value'],),  
                            #], className='two columns', style={'display':'inline-block', 'vertical-align':'top', 'margin-top':-10}),
                            ], width={'size':'auto', 'offset':0}, align='end',),# className='mb-30'),
                        #], className='row', style={'display':'inline-block', 'vertical-align':'top'}),
                        ], justify='center', no_gutters=True),# END TAB-1, ROW-2 
                        # START LAST ROW: Display Options
                        dbc.Row([
                            # FIRST COL
                            dbc.Col([
                                #
                                ####
                                dbc.FormGroup([
                                    dbc.Label('Display Options:', html_for={'type':'slct_x2', 'index': graph_clicks}, width=dict(size='auto'), align = 'center'),
                                    dbc.Col([
                                        # Add Radio Item for Motor-1 Secondary_xaxis Display
                                        dbc.RadioItems(id={'type': 'slct_x2', 'index': graph_clicks},
                                            options=[],
                                            value='x',
                                            inline = True,
                                            persistence = True,
                                            persistence_type = 'session',
                                            persisted_props = ['value'],
                                            style={'padding-bottom':0, 'margin-top':8, 'fontSize':14},
                                            #className = 'mt-40',
                                        ),
                                    ], width='auto'),
                                    dbc.Col([
                                        # Add Radio Item for Motor-2 Secondary_yaxis Display
                                        dbc.RadioItems(id={'type': 'slct_y2', 'index': graph_clicks},
                                            options=[],
                                            value='y',
                                            inline = True,
                                            persistence = True,
                                            persistence_type = 'session',
                                            persisted_props = ['value'],
                                            style={'padding-bottom':0, 'margin-top':8, 'fontSize':14},
                                        )
                                    ], width='auto')
                                ], row=True),
                                ####
                            ]) # END COL
                        ]), # END Last ROW TAB-1
                    ]), # END TAB-1 children, and END dcc.Tab 'hmap'
                    #===========================================================================================================================================================================
                    # Tab-2 Layout
                    #===========================================================================================================================================================================
                    # NEW ROW
                    dbc.Tab(id={'type':'sctr', 'index':graph_clicks}, label='1D Time-Scan' , tab_id='tab-2', tabClassName = 'mt-n50', tab_style={'margin-top': '-50'}, children = [
                        # FormGroup places lineout selection Dropdown menu horizontally inline with a label
                        dbc.Form([
                            dbc.FormGroup([
                                # Add Lineout Selection Label
                                dbc.Label('Select Lineout:', html_for={'type': 'slct_lineout', 'index': graph_clicks}, width=3),#className = 'mr-2',
                                dbc.Col(
                                    dbc.ButtonGroup([
                                        # ROW-1: 'slct_time0' & 'slct_motor1' side-by-side
                                        html.Div([
                                        # Add 1D-Lineout RadioItems at fixed Motor-1(2) Positions
                                            dbc.RadioItems(id={'type': 'slct_time0', 'index': graph_clicks},
                                                className = 'btn-group',
                                                labelClassName = 'btn btn-secondary',
                                                labelCheckedClassName = 'active',
                                                options = [{'label':'Motor-1', 'value': False}, {'label':'Motor-2', 'value': True}],
                                                value=False,
                                                persistence = True,
                                                persistence_type = 'memory',
                                                persisted_props = ['value'],
                                            ), html.Div(id={'type':'time0_radio', 'index':graph_clicks})
                                        ], className = 'radio-group p-10'),
                                        # Tab-2 'slct_lineout' Dropdown Menu
                                        dcc.Dropdown(id={'type':'slct_lineout', 'index':graph_clicks},
                                            multi = False,
                                            #optionHeight = 30,
                                            options = [],
                                            #value = None,
                                            clearable = False,
                                            persistence = True,
                                            persistence_type = 'memory',
                                            persisted_props = ['value'],
                                            style = {'width':'185px', 'fontSize':'15px'},
                                        ), # END 'slct_lineout Dropdown'
                                    ], size='sm', className='p-10'), # END of ButtonGroup
                                width = 'auto', className='p-10'), # END of COL
                            ], row = True, className='p-10'),# END FormGroup, check=True, className='mr-3'), inline=True),
                            #=======================================================================================================================================================
                            # FormGroup places scan(s) selection Dropdown Menu horizontally inline with a label
                            dbc.FormGroup([
                                # Select Scan(s) Multi-Value Dropdown Menu
                                dbc.Label('Select Scan(s):', html_for={'type': 'slct_scans', 'index': graph_clicks}, width=3),#className = 'mr-2',
                                dbc.Col(
                                    # Add scan selection dropdown menu
                                    dcc.Dropdown(id={'type': 'slct_scans', 'index': graph_clicks},
                                        options=[{'label': list(data_dict.keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'),
                                            'value': list(data_dict.keys())[scn]} for scn in range(len(data_dict))],
                                        multi=True,
                                        value=[list(data_dict.keys())[0], list(data_dict.keys())[1], list(data_dict.keys())[-1]],
                                        clearable = True,
                                        placeholder = 'Select a scan to display...',
                                        persistence = True,
                                        persistence_type = 'memory',
                                        persisted_props = ['value'],
                                    ),
                                width = 9),
                        ], row = True, className='pt-10'),# END FormGroup, check=True, className='mr-3'), inline=True),
                            # FormGroup places Channel Checklist horizontally inline with a label
                            dbc.FormGroup([
                                # Add Channel Checklist
                                dbc.Label('Select Channel(s):', html_for={'type': 'bkgnd_color', 'index': graph_clicks}, width=3),#className = 'mr-2',
                                dbc.Col(dbc.Checklist(
                                    id={'type': 'channel_check', 'index': graph_clicks},
                                    inline = True,
                                    switch = True,
                                    options=[{'label': f'{ch}', 'value': ch} for ch in range(pp.nchannels)],
                                    value = [1],
                                    persistence = True,
                                    persistence_type = 'memory',
                                    persisted_props = ['value'],
                                    className = 'mt-2',
                                    ), width = 9, className = 'mt-n10',
                                ), # END COL
                            ], row = True, className = 'mt-n10')# END FormGroup, check=True, className='mr-3'), inline=True),
                        ], className='p-10'), # END Form
                        # Initialize an empty graph object, The 'figure={}' argument is optional, it will hold the app.callback output
                        dcc.Graph(id={'type': '1d_timescan', 'index': graph_clicks}, figure={}),
                        # NEW ROW
                        dbc.Form([dbc.FormGroup([
                            dbc.Label('Display Options:', html_for={'type':'bkgnd_color', 'index': graph_clicks}, width=dict(size='auto'), align = 'center'),
                            # FIRST COL
                            dbc.Col(
                                # Button changes visible axes for space and time
                                dbc.Button( 'Axis Label', id={'type':'axes_bttn', 'index': graph_clicks}, n_clicks=0, outline=True, size='sm'),
                                width='auto'), # className='three columns', style={'display':'inline-block', 'vertical-align':'top'}
                            # SECOND COL
                            dbc.Col([
                                # Modal Button for Legend color picker
                                dbc.Button( 'Legend Color', id={'type':'lgnd_modal_open', 'index': graph_clicks}, n_clicks=0, outline=True, size='sm'),
                                dbc.Modal([
                                    dbc.ModalHeader('Select a Trace:'),
                                    dbc.ModalBody(
                                        dbc.ListGroup(id={'type':'lgnd_modal_list', 'index': graph_clicks}, children=[], flush=True)
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button('Apply Changes', id={'type':'lgnd_modal_close', 'index': graph_clicks}, n_clicks=0, size='sm'),
                                    ),
                                ], id={'type':'lgnd_modal', 'index': graph_clicks}, is_open=False, scrollable=True, size='lg'),
                            ], width='auto'),
                            # THIRD COL
                            dbc.Col(
                                # Grid Lines ON/OFF
                                dbc.Button( 'Grid Lines', id={'type':'grid_bttn', 'index': graph_clicks}, n_clicks=0, outline=True, size='sm'),
                                width='auto'),
                            # FOURTH COL
                            dbc.Col(
                                # Toggle switches background color from black to white
                                daq.ToggleSwitch(id={'type': 'bkgnd_color', 'index': graph_clicks},
                                    label=['Black', 'White'],
                                    value=False,
                                    size = 30,
                                    style={'width':'80px', 'margin-left':10}),
                                width='auto'), # className='three columns', style={'display':'inline-block', 'vertical-align':'top', 'margin-top':2, 'margin-left':109}
                        ]) ], inline=True), # END Form
                        #]) ], form=True, justify='between', align='center', no_gutters=True), # className='row', style={'display':'inline-block', 'vertical-align':'top'}
                    ]), # ] END TAB-2 children, ) END dcc.Tab 'sctr'
                ], # END TABS children
                persistence = True,
                persistence_type = 'memory',
                persisted_props = ['value']
                ), # END dcc.Tabs component
            # Add an 'HTML5 content division element, <div>' w/ the 'Div' wrapper
            html.Div( id={'type': 'tabs-content', 'index': graph_clicks} ),
            # END TABS LAYOUT +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        ] # END 'new_graph' <dbc.Container> children = []
    ) # END 'new_graph' <dbc.Container> 
    container_children.append(new_graph)
    return container_children
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Open/Close Modal to change 1D Lineout (Scatter) line & marker colors
@app.callback(
    Output({'type':'lgnd_modal', 'index':MATCH}, 'is_open'),
    [Input({'type':'lgnd_modal_open', 'index':MATCH}, 'n_clicks'),
    Input({'type':'lgnd_modal_close', 'index':MATCH}, 'n_clicks')],
    State({'type':'lgnd_modal', 'index':MATCH}, 'is_open')
    )
def toggle_modal(nclicks_open, nclicks_close, is_open):
    if nclicks_open | nclicks_close:
        return not is_open
    return is_open
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Chained-Callback determines dropdown options displayed
@app.callback(
    [Output({'type':'slct_lineout', 'index':MATCH}, 'options'),
    Output({'type':'slct_lineout', 'index':MATCH}, 'value'),
    Output({'type':'slct_lineout', 'index':MATCH}, 'placeholder')],
    Input({'type':'slct_time0', 'index':MATCH}, 'value') )
def lineout_options(tau_slctd):
    if tau_slctd:
        options = [ {'label': f'{i} [mm]', 'value': i} for i in m2_positions ]
        value = m2_positions[0]
        placeholder = 'Motor-2 Lineout [mm]'
    else:
        options = [ {'label': f'{i} [mm]', 'value': i} for i in m1_positions ]
        value = m1_positions[0]
        placeholder = 'Motor-1 Lineout [mm]'
        
    return options, value, placeholder
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# List all trace colors and names in legend modal
@app.callback(Output({'type':'lgnd_modal_list', 'index' : MATCH}, 'children'), 
              [Input({'type':'slct_scans', 'index' : MATCH}, 'value'),
              Input({'type':'channel_check', 'index' : MATCH}, 'value')],
              )
def populate_legend_modal_list(scn_slctd, ch_slctd):
    num_traces = len(scn_slctd)*len(ch_slctd)
    trace_items = []
    pop_overs=[]
    ctx = dash.callback_context
    # Hardcoded values: 0 grabs first list element (a stringified dictionary), 9 grabs ninth character in string (the subplot index)
    MATCH_index = int(list(ctx.inputs.keys())[0][9])
    print('MATCH_index', MATCH_index)
    #FF6692 is too similar to other color options in the 'Plotly' (default) color swatch
    color_index = 6
    colors = px.colors.qualitative.Plotly[:color_index] + px.colors.qualitative.Plotly[color_index+1:] 
    num_colors = len(colors)

    for tr in range(num_traces):
        # Unique ID for reference in 'update_1d_timescan' callback
        idx = (100*MATCH_index) + tr + 10
        #name=str(idx)
        color_tr=colors[tr%num_colors]

        trace_items.append(dbc.ListGroupItem(
                dbc.Button(
                    [
                    dbc.Badge(
                        f'Trace {tr}, Subplot Index {MATCH_index}',
                        id={'type':'badge_color', 'index':idx}, 
                        pill=True, 
                        color=color_tr, 
                        className='ml-5'
                        ) # END Badge
                     ], # END Button children
                    size='sm', block=True, active=True, id={'type':'badge-bttn', 'index':idx}
                ), id=f'badge-wrppr-{idx}',
            ) # END List Group Item (AKA 'Badge wrapper')
        ) # END call to append trace_items
        trace_items.append(dbc.Popover(
            [
            dbc.PopoverBody(
               daq.ColorPicker(id={'type':'color-picker', 'index':idx}, label='Color Picker', value=dict(hex=color_tr) )
               )
            ], target=f'badge-wrppr-{idx}', placement='right-start', trigger='legacy')
        )
    return trace_items
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Update the lineout for the scatter plot
@app.callback(Output(component_id= {'type':'1d_timescan', 'index': MATCH}, component_property='figure'),
    [Input(component_id={'type':'slct_scans', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'channel_check', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'slct_time0', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'slct_lineout', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'slct_timeaxis1', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'slct_timeaxis2', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'bkgnd_color', 'index': MATCH}, component_property='value'),
    Input(component_id= {'type':'axes_bttn', 'index': MATCH}, component_property='n_clicks'),
    Input(component_id={'type':'lgnd_modal_close', 'index': MATCH}, component_property='n_clicks'),
    Input(component_id={'type':'lgnd_modal_list', 'index':MATCH}, component_property='children') ] )
def update_1d_timescan(scans_slctd, channels_slctd, time0_slctd, line_slctd, taxis1_slctd, taxis2_slctd, bkgnd_switch, nclicks, close_clicks, lgnd_modal_child):
    # Set base figure for subplots
    fig = make_subplots(rows = 1, #Display how many rows of objects
                        cols = 1, #Display how many side-by-side?
                        #subplot_titles = [list_of_strings],
                        specs=[[{'secondary_y':True}]],
                        shared_xaxes = False,
                        shared_yaxes = False)

    # Global, DASH defined, variable available only inside callbacks
    ctx = dash.callback_context
    inputs = ctx.inputs
    lgnd_modal_list_key = list(inputs.keys())[-1]
    lgnd_modal_list_vals = inputs[lgnd_modal_list_key]

    # Counter helps to map the trace numbers and colors in a controlled order
    counter = 0
    badge_colors =[]
    for element in lgnd_modal_list_vals:
        if 'id' not in list(element['props'].keys()):
            print('Vals of pop child dict', element['props']['children'][0]['props']['children']['props'])
            badge_colors.append(element['props']['children'][0]['props']['children']['props']['value']['hex']) # popover children
    print(badge_colors)
    
    # Set the scatter plot background color to black or white
    if bkgnd_switch:
        bkgnd_color = 'white'
        grid_color = 'black'
    else:
        bkgnd_color = 'black'
        grid_color = 'white'
    
    # Modify formatted data dictionary for user input
    for scn in scans_slctd:
        dff = data_dict.copy()
        dff = dff[scn]
        for ch in channels_slctd:
            # Update color used for each trace
            trace_color = badge_colors[counter]

            if time0_slctd == False:
                xdata_t = np.round( ((dff[ch].index-taxis2_slctd)/step2_space)*step2_time, 1)
                xdata_s = dff[ch].index
                ydata = dff[ch].loc[:,[line_slctd]][line_slctd] #<--NO INTERPOLATION/NO CURVE FIT
                time_conversion = round( ( (line_slctd-taxis1_slctd) / step1_space )*step1_time, 1)
                # Create axis labels for TAB-2 scatter plots
                ttl_txt = f'<b>Lineout: M-1= {line_slctd} [mm], T= {time_conversion} [fs]<b>'
                x_ttl_txt_t = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
                x_ttl_txt_s = '<b>Target-Position: Motor 2 [mm]<b>'
            elif time0_slctd == True:
                xdata_t = np.round( ((dff[ch].columns-taxis1_slctd)/step1_space)*step1_time, 1)
                xdata_s = dff[ch].columns
                ydata = dff[ch].loc[[line_slctd]].T[line_slctd]
                time_conversion = round(((line_slctd-taxis2_slctd)/step2_space)*step2_time, 1)
                # Create axis labels for TAB-2 scatter plots
                ttl_txt = f'<b>Lineout: M-2 = {line_slctd} [mm], \N{MATHEMATICAL BOLD ITALIC SMALL TAU} = {time_conversion} [fs]<b>'
                x_ttl_txt_t = f'<b>Pump-Probe (T) Delay [fs]<b>'
                x_ttl_txt_s = f'<b>Target-Position: Motor 1 [mm]<b>'
                
            # Additional Display Formatting:
            lgnd_ttl = scn.replace('#', ': #').capitalize().replace('_avg', ': AVG')
            y_ttl_txt = '<b>Signal Amplitude [a.u.]<b>'
            stndff = 0
            
            # Display both time-delay and motor-position on scatter
            if (nclicks%6==0) | (nclicks%6==1):
                # Time-Delay(xaxis2) on 'top', motor-position on 'bottom'
                if nclicks%6==0:
                    #loc_t = 'top'
                    loc_s = 'bottom'
                    # Add standoff param when time(xaxis-2) is on the top, for readability
                    xaxis2_layout = dict(title =
                        x_ttl_txt_t,
                        title_standoff = stndff,
                        showgrid = True,
                        gridcolor = grid_color,
                        #zeroline = True,
                        zerolinecolor = grid_color,
                        anchor = 'y',
                        overlaying = 'x',
                        #range = [ xdata_t[0], xdata_t[-1] ],
                        side = 'top')
                # Time-Delay axes correspond with xaxis-2, 'bottom'
                elif nclicks%6==1:
                    #loc_t = 'bottom'
                    loc_s = 'top'
                    # No need for standoff param on bottom xaxis
                    xaxis2_layout = dict(title =
                        x_ttl_txt_t,
                        showgrid = True,
                        gridcolor = grid_color,
                        #zeroline = True,
                        zerolinecolor = grid_color,
                        anchor = 'y',
                        overlaying = 'x',
                        #range = [ xdata_t[0], xdata_t[-1] ],
                        side = 'bottom')

                # Add two scatter traces b/c we want to display multiple x-axes
                fig.add_trace(go.Scatter(
                    x=xdata_s,
                    y=ydata,
                    visible = True,
                    opacity=1,
                    line_color = trace_color,
                    marker_color = trace_color,
                    showlegend = True,
                    xaxis = 'x',
                    name= f'[{ch}]   - {lgnd_ttl[5:]}',
                    legendgroup = str(ch),
                    mode='lines+markers'),)
                if (ch == channels_slctd[-1]) & (scn == scans_slctd[-1]):
                    fig.add_trace(go.Scatter(
                        x=xdata_t,
                        y=ydata,
                        xaxis = 'x2',
                        mode = 'lines+markers',
                        visible = True, # KEEP TRUE FOR SECONDARY AXIS
                        opacity = 0, # KEEP ZERO HIDE TRACE
                        line_color = 'white',
                        marker_color = 'white',
                        showlegend = False)) # KEEP FALSE TO HIDE LEGEND
                if loc_s == 'top':
                    # Create axis objects and apply formatting
                    fig.update_layout(xaxis = dict(title = x_ttl_txt_s, title_standoff = stndff, side = loc_s, showgrid=True, gridcolor = grid_color, zerolinecolor = grid_color), # range = [ xdata_s[0], xdata_s[-1] ]
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zerolinecolor = grid_color),
                                        xaxis2 = xaxis2_layout,
                                        title_text = ttl_txt,
                                        paper_bgcolor = 'rgb(160,160,160)',
                                        plot_bgcolor = bkgnd_color,
                                        font_color = 'black',
                                        margin_autoexpand = True,
                                        margin_l = 110,
                                        #margin_r = 120,
                                        margin_t = 120,
                                        )
                elif loc_s == 'bottom':
                    # Create axis objects and apply formatting
                    fig.update_layout(xaxis = dict(title = x_ttl_txt_s, side = loc_s, showgrid=True, gridcolor = grid_color, zerolinecolor = grid_color),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zerolinecolor = grid_color),
                                        xaxis2 = xaxis2_layout,
                                        title_text = ttl_txt,
                                        paper_bgcolor = 'rgb(160,160,160)',
                                        plot_bgcolor = bkgnd_color,
                                        font_color = 'black',
                                        margin_autoexpand = True,
                                        margin_l = 110,
                                        #margin_r = 120,
                                        margin_t = 120,
                                        )

            # All the button options for single-axis displays
            else:
                if nclicks%6==2:
                    xdata = xdata_t
                    loc = 'top'
                    x_ttl_txt = x_ttl_txt_t
                elif nclicks%6==3:
                    xdata = xdata_t
                    loc = 'bottom'
                    x_ttl_txt = x_ttl_txt_t
                elif nclicks%6==4:
                    xdata = xdata_s
                    loc = 'top'
                    x_ttl_txt = x_ttl_txt_s
                elif nclicks%6==5:
                    xdata = xdata_s
                    loc = 'bottom'
                    x_ttl_txt = x_ttl_txt_s
                fig.add_trace(go.Scatter(
                    x=xdata,
                    y=ydata,
                    xaxis = 'x',
                    yaxis = 'y',
                    visible = True,
                    opacity=1,
                    line_color = trace_color,
                    marker_color = trace_color,
                    showlegend = True, # TRUE SHOWS TRACE IN LEGEND
                    name = f'[{ch}]   - {lgnd_ttl[5:]}',
                    legendgroup = str(ch),
                    mode='lines+markers'),) 
                if loc == 'top':
                    # Create axis objects and apply formatting
                    fig.update_layout(xaxis = dict(title = x_ttl_txt, title_standoff = 0, side = loc, showgrid= True, gridcolor = grid_color, zerolinecolor = grid_color),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zerolinecolor = grid_color),
                                        title_text = ttl_txt,
                                        paper_bgcolor = 'rgb(160,160,160)',
                                        plot_bgcolor = bkgnd_color,
                                        font_color = 'black',
                                        margin_autoexpand = True,
                                        margin_l = 110,
                                        #margin_r = 120,
                                        margin_t = 120,
                                        )
                elif loc == 'bottom':
                    # Create axis objects and apply formatting
                    fig.update_layout(xaxis = dict(title = x_ttl_txt, side = loc, showgrid=True, gridcolor = grid_color, zerolinecolor = grid_color),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zerolinecolor = grid_color),
                                        title_text = ttl_txt,
                                        paper_bgcolor = 'rgb(160,160,160)',
                                        plot_bgcolor = bkgnd_color,
                                        font_color = 'black',
                                        margin_autoexpand = True,
                                        margin_l = 110,
                                        #margin_r = 120,
                                        margin_t = 120,
                                        )
            # Counter is keeping track of the number of traces for line color control
            counter+=1
    fig.update_layout(legend_title_text = '<b>Trace: [Ch] - Scan<b>',
                      width=675)
    print('width', pp.num_m1steps*mag_factor )
    #fig.update_traces(line_color=trace_color_picked[trace], selector=trace)
    return fig
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Update Badge color(s) and/or name assignment(s)
@app.callback(Output({'type':'badge_color', 'index':MATCH}, 'color'),
              Input({'type':'color-picker', 'index':MATCH}, 'value')
              )
def update_badge_color(color_pckd):
    #return [color_pckd[i]['hex'] for i in range(len(color_pckd))]
    return color_pckd['hex']
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set chained callback for T=0, 'slct_x2', RadioItem
@app.callback(Output({'type':'slct_x2', 'index': MATCH}, 'options'),
    [Input({'type':'slct_timeaxis1', 'index': MATCH}, 'value'),
    Input({'type':'tabs', 'index':MATCH}, 'active_tab')] )
def set_multi_xaxis_options(taxis1_slctd, tab):
    # When Input is cleared, display no options (= [])
    if (taxis1_slctd == None) | (tab == 'tab-2'):
        #opt4=[{'label': 'Choose Motor-1 "T=0"','value':'x', 'disabled':False}]
        opt4 = [] # Alternative to setting style = {'display':'none'}
    # Whenever a selection is made, display RadioItems options
    elif taxis1_slctd != None:
        opt4=[{'label': 'Title','value':'x', 'disabled':False}, {'label': 'Top Axis', 'value':'x2','disabled':False}]
    return opt4
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set chained callback for T=0, 'slct_x2', RadioItems
@app.callback(Output({'type':'slct_x2', 'index':MATCH}, 'value'),
    [Input({'type':'slct_timeaxis1', 'index': MATCH}, 'value'),
    Input({'type':'slct_x2', 'index':MATCH}, 'value')])
def set_multi_xaxis_value(taxis1_slctd, x2_slctd):
    # When Input is cleared, display no options (= [])
    if taxis1_slctd == None:
        new_x2 = 'x' # Display cbar by default
    # Whenever a selection is made, display RadioItems options
    elif taxis1_slctd != None:
        new_x2 = x2_slctd
    return new_x2
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set chained callback for Tau=0, 'slct_y2', RadioItem
@app.callback(Output({'type':'slct_y2', 'index': MATCH}, 'options'),
    [Input({'type':'slct_timeaxis2', 'index': MATCH}, 'value'),
    Input({'type':'tabs', 'index':MATCH}, 'active_tab')] )
def set_multi_yaxis_options(taxis2_slctd, tab):
    # When Input is cleared, display no options (= [])
    if (taxis2_slctd == None) | (tab == 'tab-2'):
        #opt6=[{'label': 'Choose Motor-2 "TAU=0"','value':'y', 'disabled':False}]
        y2_opts = [] # Alternative to setting style = {'display':'none'}
    # Whenever a selection is made, display RadioItems options
    elif taxis2_slctd != None:
        y2_opts = [{'label': 'Show Colorbar','value':'y', 'disabled':False}, {'label': 'Hide Colorbar', 'value':'y2','disabled':False}]
    return y2_opts
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Set chained callback for Tau=0, 'slct_y2', RadioItems
@app.callback(Output({'type':'slct_y2', 'index':MATCH}, 'value'),
    [Input({'type':'slct_timeaxis2', 'index': MATCH}, 'value'),
    Input({'type':'slct_y2', 'index':MATCH}, 'value')])
def set_multi_yaxis_value(taxis2_slctd, y2_slctd):
    # When Input is cleared, display no options (= [])
    if taxis2_slctd == None:
        y2_val = 'y' # Display cbar by default
    # Whenever a selection is made, display RadioItems options
    elif taxis2_slctd != None:
        y2_val = y2_slctd # Display multi-axes on y
    return y2_val
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
@app.callback([Output(component_id={'type':'signal_range', 'index': MATCH}, component_property='min'),
    Output(component_id={'type':'signal_range', 'index': MATCH}, component_property='max'),
    Output(component_id={'type':'signal_range', 'index': MATCH}, component_property='step'),
    Output(component_id={'type':'signal_range', 'index': MATCH}, component_property='value'),
    Output(component_id={'type':'signal_range', 'index': MATCH}, component_property='marks')],
    [Input(component_id={'type':'slct_channel', 'index': MATCH}, component_property='value'),
    Input(component_id={'type':'slct_scan', 'index': MATCH}, component_property='value'),])
def update_rangeslider(channel_slctd, scan_slctd):
    # Modify formatted data dictionary for user input
    dff = data_dict.copy()
    dff = dff[scan_slctd][channel_slctd]
    
    # Identify Min/Max/Range for SLider callbacks
    min_min = round(dff.min().min(), 6)
    max_max = round(dff.max().max(), 6)
    vals = [min_min, max_max]
    sig_step = round((max_max - min_min)/100,7)
    range_marks={min_min:{'label':'Sig Min: '+str(min_min), 'style':{'color':'blue', 'font-weight':'bold', 'right':'40px'} }, max_max:{'label':'Sig Max: '+str(max_max), 'style':{'color':'#f50', 'font-weight':'bold', 'vertical-align':'text-top','right':'40px'}}}
    #range_marks={min_min:{'label':'Sig Min: '+str(min_min), 'style':{'color':'blue', 'right':'40px'} }, max_max:{'label':'Sig Max: '+str(max_max), 'style':{'color':'#f50', 'vertical-align':'text-top','right':'40px'}}}
    return min_min, max_max, sig_step, vals, range_marks
    
    abs_min = abs(min_min)
    abs_max = abs(max_max)
    
    # Identify cbar range values
    if (min_min>0) | (max_max<0):
        trace_min = min_min
        trace_max = max_max
        # Initial RangeSlider values
        range_marks={min_min:{'label':'Min: '+str(min_min), 'style':{'color':'blue', 'font-weight':'bold', 'right':'40px'} }, max_max:{'label':'Max: '+str(max_max), 'style':{'color':'#f50', 'font-weight':'bold', 'vertical-align':'text-top','right':'40px'}}}
    elif abs_max > abs_min:
        trace_min = round(-1*max_max, 6)
        trace_max = max_max
        range_marks={trace_min:{'label':''}, min_min:{'label':'Min: '+str(min_min), 'style':{'color':'blue', 'font-weight':'bold', 'right':'40px'}}, 0:{'label':str(0), 'style':{'color':'black', 'font-weight':'bold', 'right':'40px'}}, max_max:{'label':'Max: '+str(max_max), 'style':{'color':'#f50', 'font-weight':'bold',  'right':'40px'}}}
    elif abs_max < abs_min:
        trace_min = min_min
        trace_max = round(-1*min_min, 6)
        range_marks={min_min:{'label':'Min: '+str(min_min), 'style':{'color':'blue', 'font-weight':'bold', 'right':'40px'}}, 0:{'label':str(0), 'style':{'color':'black', 'font-weight':'bold','right':'40px'}}, max_max:{'label':'Max: '+str(max_max), 'style':{'color':'#f50', 'font-weight':'bold', 'right':'40px'}}, trace_max:{'label':''}}

    # Initial RangeSlider values
    vals = [min_min, max_max]
    
    return trace_min, trace_max, sig_step, vals, range_marks
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Input is what goes into the 'figure={}' dictionary in the app.layout
# Returned component_property, 'children', from update_hmap function, must be in form of a list
@app.callback(Output(component_id={'type':'2d_scan_surf', 'index': MATCH}, component_property='figure'),#Output(component_id='output_container', component_property='children'),
                [Input(component_id={'type':'slct_channel', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'slct_scan', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'slct_timeaxis1', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'slct_x2', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'slct_timeaxis2', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'slct_y2', 'index': MATCH}, component_property='value'),
                Input(component_id={'type':'signal_range', 'index': MATCH}, component_property='value')])
def update_hmap(channel_slctd, scan_slctd, taxis1_slctd, x2_slctd, taxis2_slctd, y2_slctd, cbar_range):    
    # Set base figure for subplots
    fig = make_subplots(rows = 1, #Display how many rows of objects 
                        cols = 1, #Display how many side-by-side?
                        #subplot_titles = [list_of_strings],
                        specs=[[{'secondary_y':True}]],
                        shared_xaxes = False,
                        shared_yaxes = False)
    
    # Modify formatted data dictionary for user input
    dff = data_dict.copy()
    dff = dff[scan_slctd][channel_slctd]
        
    # Display Motor-X Positions
    if (taxis1_slctd==None) & (taxis2_slctd==None):
        xdata = dff.columns
        ydata = dff.index
        x_title_txt = '<b>Target-Position: Motor 1 [mm]<b>'
        y_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        x_range = [m1_positions[0]-(step1_space/2), m1_positions[-1]+(step1_space/2)]
        y_range = [m2_positions[0]-(step2_space/2), m2_positions[-1]+(step2_space/2)]
    # Display Pump-Probe Time-Delay Axis: T (from Motor-1 scans)
    elif (taxis1_slctd != None) & (taxis2_slctd == None):
        m1_zero = taxis1_slctd
        time_ax1 = np.round( ((dff.columns-m1_zero)/step1_space)*step1_time, 1)
        xdata = time_ax1
        ydata = dff.index
        x_title_txt = '<b>Pump-Probe (T) Delay [fs]<b>'
        y_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        x_range = [time_ax1[0]-(step1_time/2), time_ax1[-1]+(step1_time/2)]   
        y_range = [m2_positions[0]-(step2_space/2), m2_positions[-1]+(step2_space/2)]
    # Display Drive-Probe Time-Delay Axis: TAU (from Motor-2 scans)
    elif (taxis1_slctd == None) & (taxis2_slctd != None):
        m2_zero = taxis2_slctd
        time_ax2 = np.round( ((dff.index-m2_zero)/step2_space)*step2_time, 1)
        xdata = dff.columns
        ydata = time_ax2
        x_title_txt = '<b>Target Position: Motor 1 [mm]<b>'
        y_title_txt = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
        x_range = [m1_positions[0]-(step1_space/2), m1_positions[-1]+(step1_space/2)]
        y_range = [time_ax2[0]-(step2_time/2), time_ax2[-1]+(step2_time/2)]
    # Display Both Time-Delay Axes: T & TAU
    elif (taxis1_slctd != None) & (taxis2_slctd != None):
        m1_zero = taxis1_slctd
        m2_zero = taxis2_slctd
        time_ax1 = np.round( ((dff.columns-m1_zero)/step1_space)*step1_time, 1)
        time_ax2 = np.round( ((dff.index-m2_zero)/step2_space)*step2_time, 1)
        xdata = time_ax1
        ydata = time_ax2
        x_title_txt = '<b>Pump-Probe (T) Delay [fs]<b>'
        y_title_txt = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
        x_range = [time_ax1[0]-(step1_time/2), time_ax1[-1]+(step1_time/2)]
        y_range = [time_ax2[0]-(step2_time/2), time_ax2[-1]+(step2_time/2)]
##############################################################################################################################################################################################      
    # https://plotly.com/python/builtin-colorscales/
    palettes = ['Viridis', 'haline', 'Plasma','thermal', 'Hot', 'RdBu_r','RdYlBu_r', 'Spectral_r','PRGn', 'curl', 'delta', 'Tropic', 'Blackbody', 'oxy']
    palette = palettes[0]

    # Plotly Graph Objects (GO)
    fig.add_trace(go.Heatmap(x=xdata,
            y = ydata,
            z = dff,
            xaxis = 'x',
            yaxis = 'y',
            xgap = 1,
            ygap = 1,
            zmin = cbar_range[0],
            #zmid = 0,
            #hover_name = channel_slctd,#hname,
            zmax = cbar_range[1],
            visible = True,
            opacity = 1.0,
            colorbar_title = f'<b>Signal<b>',
            # colorbar_tickcolor = 'black',
            colorbar_len = 1.06,
            colorscale=palette,), secondary_y = False)
    
    # SECONDARY X-AXIS, display both Motor-1 Position & Time-Delay: T 'Pump-Probe'
    if x2_slctd == 'x2':
        x2_title_txt = '<b>Target Position: Motor 1 [mm]<b>'
        x2_range = [m1_positions[0]-(step1_space/2), m1_positions[-1]+(step1_space/2)]
        x2_layout = {'title' : {'text' : x2_title_txt}, 'overlaying':'x', 'side': 'top', 'nticks': 5, 'ticks': 'outside', 'tickson': 'boundaries','color' : 'black','showline': False,'showgrid': False,'zeroline': False, 'range' : x2_range }
    elif x2_slctd == 'x':
        x2_layout = None

    # SECONDARY Y-AXIS, display both Motor-2 Position & Time-Delay: Tau 'Drive-Probe'
    if y2_slctd == 'y2':
        y2_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        y2_range =  [m2_positions[0]-(step2_space/2), m2_positions[-1]+(step2_space/2)]
        yaxis2 = {'title' : {'text' : y2_title_txt},
                           'overlaying':'y',
                           'side': 'right',
                           'nticks': 5,
                           'ticks': 'outside',
                           'tickson': 'boundaries',
                           'color' : 'black',
                           'showline': False,
                           'showgrid': False,
                           'zeroline': False,
                           'range' : y2_range }
    elif y2_slctd == 'y':
        yaxis2 = None
        
    # Actions for when RadioItems (options 4 and 6) are selected    
    if (x2_slctd=='x2') | (y2_slctd=='y2'):
        # Only the secondary xaxis was activated
        if (x2_slctd=='x2') & (y2_slctd=='y'):
            # ydata remains unchanged from dropdown selections above
            xdata2 = dff.columns
            ydata2 = ydata
        # Only the secondary yaxis was activated
        elif (x2_slctd=='x') & (y2_slctd=='y2'):
            # ydata remains unchanged from dropdown selections above
            xdata2 = xdata
            ydata2 = dff.index
        # Add Sceondary position axes for both 'x2' and 'y2'
        elif (x2_slctd=='x2') & (y2_slctd=='y2'):
            xdata2 = dff.columns
            ydata2 = dff.index
        # Add a HEATMAP trace
        fig.add_trace(go.Heatmap(x = xdata2,
                       y = ydata2,
                       z = dff,
                       xaxis = x2_slctd, # 'x'(default) or 'x2': Secondary x-axis for Motor-1
                       yaxis = y2_slctd, # 'y'(default) or 'y2': Secondary y-axis for Motor-2
                       xgap = 1,
                       ygap = 1,
                       zmin =  cbar_range[0], # Defaults to DF min
                       #zmid = 0,
                       #hover_name = channel_slctd,#hname,
                       zmax =  cbar_range[1], # Defaults to DF max
                       visible = True,
                       opacity = 0.0, # Hide overlayed trace, only want 2nd axis display
                       colorbar_title = f'<b>Signal<b>',
                       colorbar_len = 1.06,
                       colorscale =palette,
                       ))
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Removes title when top axis is displayed
    if (taxis1_slctd !=None) & (x2_slctd=='x2'): #Opt 3 safety, if reassigned from None above.
        ttl_txt = ''
    else:
        ttl_txt = '<b>2D Scan Intensities<b>'
        
    #fig.update_traces(showscale=False, selector=dict(type='heatmap'))
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
    # Create axis objects and apply formatting
    fig.update_layout({
        'xaxis':{'title' : {'text' : x_title_txt},
                'nticks' : 5,
                'ticks' : 'outside',
                'side': 'bottom',
                'color' : 'black',
                'showline': False,
                'showgrid': False,
                'zeroline': False,
                'range' : x_range },
        'yaxis':{'title' : {'text' : y_title_txt},
                'nticks': 5,
                'ticks': 'outside',
                'side': 'left',
                'color' : 'black',
                'showline': False,
                'showgrid': False,
                'zeroline': False,
                'range' : y_range },
        'xaxis2': x2_layout, # None (default) or Dict
        'yaxis2': yaxis2, # None (default) or Dict
        'coloraxis': {'showscale' : False},},
        coloraxis_colorbar_xpad = 300,coloraxis_colorbar_ypad = 300,coloraxis_colorbar_bgcolor = 'black',coloraxis_colorbar_bordercolor = 'black',coloraxis_colorbar_outlinecolor = 'black',coloraxis_colorbar_tickcolor = 'black',paper_bgcolor = 'rgb(160,160,160)',plot_bgcolor = 'black',title_text = ttl_txt,font_color = 'black',margin_autoexpand = True,margin_l = 110,margin_r = 120,margin_t = 120,autosize = False, width = pp.num_m1steps*mag_factor, height = pp.num_m2steps*mag_factor,)
    #==============================================================================================
    # What is returned here will actually go to the output
    # First:  'component_property = children'
    # Second: 'component_property =   figure'
    # Hide colorbar when secondary axis-right is clicked
    if (y2_slctd=='y2'):
        fig.update_traces(showscale=False, selector=dict(type='heatmap'))
    return fig # END callbacks.py