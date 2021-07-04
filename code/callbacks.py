#!/usr/bin/env python

# IMPORTS:
from app import app
from preprocessing import step1_space, step2_space, step1_time, step2_time, m1_positions, m2_positions, nchannels, data_dict, num_m1steps, num_m2steps, m1_position_range as xwidth, m2_position_range as ywidth, datasets
import dash
import numpy as np # round arrays element-wise
from plotly.express.colors import qualitative as px_colors # Select primary colors for plotting traces
import plotly.graph_objects as go # Interactive Heatmap and Scatter figures
from plotly.subplots import make_subplots # Display secondary_y axes
import dash_daq as daq # DAQ component controls
import dash_core_components as dcc # Library of dashboarding components
import dash_html_components as html # Library containing component classes for HTML tags
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH # Component interactivity through callbacks

# Set hmap magnification, fixed ratio
mag_factor = 9
# Argument-list to unpack and call inside the 'add_subplot' callback definition
args_active = [f'active_status{idx}' for idx in range(len(datasets))]
# List of MenuItems (displayed in DropdownMenu) representing filenames of datasets (ready for analysis) in the local directory
active_file_inputs = [Input(f'filename{idx}', 'active') for idx in range(len(datasets))]
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Update active DropdownMenuItem in 'files' DropdownMenu
args_nclicks = [f'nclicks{idx}' for idx in range(len(datasets))]
@app.callback([Output(f'filename{idx}', 'active') for idx in range(len(datasets))],
    [Input(f'filename{idx}', 'n_clicks') for idx in range(len(datasets))])
def update_active_filename(*args_nclicks):
    # Global, DASH defined, variable available only inside callbacks
    # https://dash.plotly.com/dash-html-components/button
    ctx = dash.callback_context
    ctxt = ctx.triggered # List of inputs triggering callback
    ctxi = ctx.inputs # Dictionary of all callback inputs
    # Check for callback trigger type
    print()
    print('update_active_filename')
    for i in range(len(ctxt)):
        print(f"ctxt[i={i}]['prop_id']", ctxt[i]['prop_id'])
        # ID FORMAT: str(filename{idx}.n_clicks) or '.' upon initial call
        if ('filename' in ctxt[i]['prop_id']): #& (ctxt[i]['value'] == True)
            triggered_id = ctxt[i]['prop_id']
            triggered_val = ctxt[i]['value']
            print('ctxt triggered_id', triggered_id)
            print('ctxt triggered_val', triggered_val)
            active_boolean = [(input_id == triggered_id) for input_id in list(ctxi.keys())]
            return active_boolean
        # ID FORMAT: '.' upon initial call
        elif ('filename' not in ctxt[i]['prop_id']):
            # No change was made from user's prior data selection
            return dash.dash.no_update
    print()
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Store intermediate data
@app.callback(Output('memory-data', 'data'), active_file_inputs)
def save_data_selection(*args_active):
    ctx = dash.callback_context # Global, DASH defined, variable available only inside callbacks
    ctxt = ctx.triggered # List of inputs triggering callback
    ctxi = ctx.inputs # Dictionary of all callback inputs
    # Check for callback trigger type
    print()
    print('save_data_selection')
    for i in range(len(ctxt)):
        print(f"ctxt[i={i}]['prop_id']", ctxt[i]['prop_id'])
        # ID FORMAT: str(filename{idx}.n_clicks) or '.' upon initial call
        if ('filename' not in ctxt[i]['prop_id']):
            print('initial call, memory-data is None')
            return None
        elif ('filename' in ctxt[i]['prop_id']) & (ctxt[i]['value'] == True):
            active_id = ctxt[i]['prop_id']
            active_f = int(active_id[len('filename'):-len('.active')])
            print('ctxt active_f', active_f)
            return active_f
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Update components
@app.callback([Output({'type':'slct_timeaxis1', 'index':MATCH}, 'value'),
    Output({'type':'delayaxis1_tooltip', 'index':MATCH}, 'children'),
    Output({'type':'slct_timeaxis2', 'index':MATCH}, 'value'),
    Output({'type':'delayaxis2_tooltip', 'index':MATCH}, 'children'),
    Output({'type':'slct_channel', 'index':MATCH}, 'options'),
    Output({'type':'slct_scan', 'index':MATCH}, 'options'),
    Output({'type':'slct_scan', 'index':MATCH}, 'value'),
    Output({'type':'slct_scans', 'index':MATCH}, 'options'),
    Output({'type':'slct_scans', 'index':MATCH}, 'value'),
    Output({'type':'channel_check', 'index':MATCH}, 'options')],
    Input('memory-data', 'data'))
def update_components(active_f):
    print()
    print('update_components')
    if active_f is None:
        f = 0
    elif active_f is not None:
        f = active_f
    print('active_f', active_f)
    print('f', f)

    # 'slct_timeaxis1' value
    delay1_value = m1_positions[f][-1]

    # 'delayaxis1_tooltip' children
    tooltip1 = f'Scan Range: [{m1_positions[f][0]}, {m1_positions[f][-1]}]'
    # 'slct_timeaxis2' value
    delay2_value = m2_positions[f][-1]

    # 'delayaxis2_tooltip' children
    tooltip2 = f'Scan Range: [{m2_positions[f][0]}, {m2_positions[f][-1]}]'

    # 'slct_channel' options
    ch_opt = [{'label': f'Channel {ch}', 'value': ch} for ch in range(nchannels[f])]

    # 'slct_scan' options
    scan_opt = [
        {'label': list(data_dict[f].keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'),
        'value': list(data_dict[f].keys())[scn]} for scn in range(len(data_dict[f]))
        ]

    # 'slct_scan' value
    scan_val = list(data_dict[f].keys())[0]

    # 'slct_scans' options
    scans_opt = [
        {'label': list(data_dict[f].keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'), 
        'value': list(data_dict[f].keys())[scn]} for scn in range(len(data_dict[f]))
        ]

    # 'slct_scans' value
    scans_val = [list(data_dict[f].keys())[0], list(data_dict[f].keys())[1], list(data_dict[f].keys())[-1]]

    # 'channel_check' options
    chnnl_opt = [{'label': f'{ch}', 'value': ch} for ch in range(nchannels[f])]

    return delay1_value, tooltip1, delay2_value, tooltip2, ch_opt, scan_opt, scan_val, scans_opt, scans_val, chnnl_opt
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# 
# Set positioning & display of dashboard
@app.callback(Output({'type':'new_graph_container', 'index':ALL}, 'style'),
    Input('add_graph','n_clicks'),
    State({'type':'new_graph_container', 'index':ALL}, 'style'))
def render_child_div(graph_clicks, container_style_states):
    print()
    print('render_child_div')
    print('graph_clicks:', graph_clicks)
    print('container style states', container_style_states)
    if (graph_clicks == 0):
        container_style_states[0] = {'width':'auto', 'outline': 'thin lightgrey solid', 'padding':5}
        return container_style_states
    else:
        for i in range(len(container_style_states)):
            container_style_states[i] = {'width':680, 'outline': 'thin lightgrey solid', 'margin-bottom':10,'margin-right':10, 'padding':5, 'display': 'inline-block'}
        return container_style_states
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Input n_clicks property from 'add_graph' bttn to dynamically add subplots via pattern-matching callbacks
#all_inputs_add_subplot = [Input('add_graph', 'n_clicks')]
#all_inputs_add_subplot.extend(active_file_inputs)
# Add plots to the dashboard
# NOTE: for container_children = State('container', 'children'), then type =  <class 'dash.dependencies.State'>
@app.callback(Output('container', 'children'), Input('add_graph', 'n_clicks'), [State('memory-data', 'data'), State('container', 'children')] )
def add_subplot(graph_clicks, active_f, container_children):
#def add_subplot(graph_clicks, *args_active_add_subplot, container_children):
    # Global, DASH defined, variable available only inside callbacks
    ctx = dash.callback_context
    ctxi = ctx.inputs
    ctxt = ctx.triggered
    # Assign correct dataset for analysis
    print()
    print('add_subplot')
    print('active_f', active_f)
    print('active_f type', type(active_f))
    if active_f is None:
        f = 0
        #raise PreventUpdate
    else:
        f = active_f

    # Add new graph object to dashboard
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
                            name = 'input_t1',
                            persistence = True,
                            persistence_type = 'memory',
                            persisted_props = ['value'],
                            placeholder = 'Pump-Probe',
                            #required = True,
                            step = 0.001, #step1_space, ADD step-size button?
                            type = 'number',
                            #value=m1_positions[f][-1], # None returns error " unsupported operand type(s) for -: 'float' and 'NoneType' "
                        ), # END 'slct_timeaxis1' dcc.Input
                        #dbc.InputGroupAddon('[mm]', addon_type='append'),
                    ], className='mb-0', size='sm'), # END InputGroup
                    dbc.Tooltip(#children = f'Scan Range: [{m1_positions[f][0]}, {m1_positions[f][-1]}]', 
                                target = 'm1', 
                                id={'type':'delayaxis1_tooltip', 'index':graph_clicks}),
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
                            name = 'input_t2',
                            persistence = True,
                            persistence_type = 'memory',
                            persisted_props = ['value'],
                            placeholder = 'Drive-Probe',
                            #required = True,
                            step = 0.001, #step2_space, ADD step-size button?
                            type='number',
                            #value=m2_positions[f][-1], # None returns error " unsupported operand type(s) for -: 'float' and 'NoneType' "
                        ),  # END 'slct_timeaxis2' dash-core-components-Input
                        #dbc.InputGroupAddon('[mm]', addon_type='append'),
                    ], className='mb-0', size='sm'), # m-margin, b-bottom
                    dbc.Tooltip(#children = f'Scan Range: [{m2_positions[f][0]}, {m2_positions[f][-1]}]',
                                target = 'm2',
                                id={'type':'delayaxis2_tooltip', 'index':graph_clicks}),
                    dbc.FormText('Drive-Probe Delay', color='secondary'),
                ] # END of dbc.Col children = [ slct_timeaxis2 ]
            ), # END of <taxis2> dbc.Col
            ]), # END of ROW
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
                                        #options=[{'label': f'Channel {ch}', 'value': ch} for ch in range(nchannels[f])],
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
                                        options=[],
                                        #{'label': list(data_dict[f].keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'), 
                                        #    'value': list(data_dict[f].keys())[scn]} for scn in range(len(data_dict[f]))
                                        multi=False,
                                        #value=list(data_dict[f].keys())[0],
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
                            dbc.Col([
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
                                    verticalHeight = 460,# For some reason callback not updating
                                    persistence = True,
                                    persistence_type = 'memory',
                                    persisted_props = ['value'],),  
                            ], width={'size':'auto', 'offset':0}, align='end',),# className='mb-30'),
                        ], justify='center', no_gutters=True),# END TAB-1, ROW-2 
                        # START LAST ROW: Display Options
                        dbc.Row([
                            # FIRST COL
                            dbc.Col([
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
                                        options=[],
                                        #{'label': list(data_dict[f].keys())[scn].replace('#', ': #').capitalize().replace('_avg', ': AVG'),
                                        #    'value': list(data_dict[f].keys())[scn]} for scn in range(len(data_dict[f]))
                                        multi=True,
                                        #value=[list(data_dict[f].keys())[0], list(data_dict[f].keys())[1], list(data_dict[f].keys())[-1]],
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
                                    #options=[{'label': f'{ch}', 'value': ch} for ch in range(nchannels[f])],
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
                        dcc.Graph(id={'type': 'scatter', 'index': graph_clicks}, figure={}),
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
    # Global, DASH defined, variable available only inside callbacks
    ctx = dash.callback_context
    ctxt = ctx.triggered
    # Check for callback trigger
    print()
    print('toggle_modal')
    for i in range(len(ctxt)):
        print(f"ctxt[i={i}]['prop_id']", ctxt[i]['prop_id'])
    print()
    if nclicks_open | nclicks_close:
        return not is_open
    return is_open
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Chained-Callback determines lineout dropdown options displayed
@app.callback(
    [Output({'type':'slct_lineout', 'index':MATCH}, 'options'),
    Output({'type':'slct_lineout', 'index':MATCH}, 'value'),
    Output({'type':'slct_lineout', 'index':MATCH}, 'placeholder')], 
    [Input({'type':'slct_time0', 'index':MATCH}, 'value'),
    Input('memory-data', 'data')])
def lineout_options(tau_slctd, active_f):
    print()
    print('lineout_options')
    print('active_f:', active_f)
    print('active_f type:', type(active_f))
    print()

    if active_f is None:
        f = 0
    elif active_f is not None:
        f = active_f
    if tau_slctd:
        options = [ {'label': f'{i} [mm]', 'value': i} for i in m2_positions[f] ]
        value = m2_positions[f][0]
        placeholder = 'Motor-2 Lineout [mm]'
    else:
        options = [ {'label': f'{i} [mm]', 'value': i} for i in m1_positions[f] ]
        value = m1_positions[f][0]
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
    # Global, DASH defined, variable available only inside callbacks
    ctx = dash.callback_context
    ctxi = ctx.inputs
    ctxt = ctx.triggered
    # Check for callback trigger
    print()
    print('populate_legend_modal_list')
    for i in range(len(ctxt)):
        print(f"ctxt[i={i}]['prop_id']", ctxt[i]['prop_id'])
    print()
    # Hardcoded values: 0 grabs first list element (a stringified dictionary), 9 grabs ninth character in string (the subplot index)
    #print('populate_legend_modal_list ctxi.keys()', ctxi.keys())
    MATCH_index = int(list(ctxi.keys())[0][9])
    #print('MATCH_index', MATCH_index)
    #FF6692 is too similar to other color options in the 'Plotly' (default) color swatch
    color_index = 6
    #colors = px.colors.qualitative.Plotly[:color_index] + px.colors.qualitative.Plotly[color_index+1:] 
    colors = px_colors.Plotly[:color_index] + px_colors.Plotly[color_index+1:] 
    num_colors = len(colors)

    for tr in range(num_traces):
        # Unique ID for reference in 'update_scatter' callback
        idx = (100*MATCH_index) + tr + 10
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
# Create/Update a figure-object for displaying data on a scatter plot w/ lines + markers
@app.callback(Output({'type':'scatter', 'index': MATCH},'figure'),
    [Input({'type':'slct_scans', 'index': MATCH},'value'),
    Input({'type':'channel_check', 'index': MATCH},'value'),
    Input({'type':'slct_time0', 'index': MATCH},'value'),
    Input({'type':'slct_lineout', 'index': MATCH},'value'),
    Input({'type':'slct_timeaxis1', 'index': MATCH},'value'),
    Input({'type':'slct_timeaxis2', 'index': MATCH},'value'),
    Input({'type':'bkgnd_color', 'index': MATCH},'value'),
    Input({'type':'axes_bttn', 'index': MATCH},'n_clicks'),
    Input({'type':'lgnd_modal_close', 'index': MATCH},'n_clicks'),
    Input({'type':'lgnd_modal_list', 'index':MATCH},'children'),
    Input({'type':'grid_bttn', 'index':MATCH},'n_clicks'),
    Input('memory-data', 'data')])
def update_scatter(scans_slctd, channels_slctd, time0_slctd, line_slctd, taxis1_slctd, taxis2_slctd, bkgnd_switch, nclicks, close_clicks, lgnd_modal_child, grid_clicks, active_f):
    # Set base figure for subplots
    fig = make_subplots(rows = 1, #Display how many rows of objects
                        cols = 1, #Display how many side-by-side?
                        #subplot_titles = [list_of_strings],
                        specs=[[{'secondary_y':True}]],
                        shared_xaxes = False,
                        shared_yaxes = False)

    # Global, DASH defined, variable available only inside callbacks
    ctx = dash.callback_context
    ctxi = ctx.inputs
    #ctxt = ctx.triggered
    print()
    print('update_scatter')
    print('active_f:', active_f)
    print('active_f type:', type(active_f))
    print()
    # Try/Except
    if active_f is None:
        f = 0
    elif active_f is not None:
        f = active_f
    # Keys contain the stringified component_ids, and values hold the state of the component_property passed to the callback function
    for key in ctxi.keys():
        if 'lgnd_modal_list' in key:
            lgnd_modal_list_key = key
            lgnd_modal_list_vals = ctxi[lgnd_modal_list_key]
        elif ('filename' in key) & (ctxi[key] == True):
            active_id = key[:-len('.active')] # .split('.')[0]
            print('ctxi active_id', active_id)
            active_id2 = key.split('.')[0]
            print('ctxi active_id 2', active_id2)

    # Counter helps to map the trace numbers and colors in a controlled order
    counter = 0
    badge_colors =[]
    for element in lgnd_modal_list_vals:
        if 'id' not in list(element['props'].keys()):
            #print('Vals of pop child dict', element['props']['children'][0]['props']['children']['props'])
            badge_colors.append(element['props']['children'][0]['props']['children']['props']['value']['hex']) # popover children
    #print(badge_colors)
    
    # Set the scatter plot background color to black or white
    if bkgnd_switch:
        bkgnd_color = 'white'
        grid_color = 'black'
    else:
        bkgnd_color = 'black'
        grid_color = 'white'
    
    # Modify formatted data dictionary for user input
    for scn in scans_slctd:
        dff = data_dict[f].copy()
        dff = dff[scn]
        for ch in channels_slctd:
            # Update color used for each trace
            trace_color = badge_colors[counter]

            if time0_slctd == False:
                xdata_t = np.round( ((dff[ch].index-taxis2_slctd)/step2_space[f])*step2_time[f], 1)
                xdata_s = dff[ch].index
                ydata = dff[ch].loc[:,[line_slctd]][line_slctd] #<--NO INTERPOLATION/NO CURVE FIT
                time_conversion = round( ( (line_slctd-taxis1_slctd) / step1_space[f] )*step1_time[f], 1)
                # Create axis labels for TAB-2 scatter plots
                ttl_txt = f'<b>Lineout: M-1= {line_slctd} [mm], T= {time_conversion} [fs]<b>'
                x_ttl_txt_t = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
                x_ttl_txt_s = '<b>Target-Position: Motor 2 [mm]<b>'
            elif time0_slctd == True:
                xdata_t = np.round( ((dff[ch].columns-taxis1_slctd)/step1_space[f])*step1_time[f], 1)
                xdata_s = dff[ch].columns
                ydata = dff[ch].loc[[line_slctd]].T[line_slctd]
                time_conversion = round(((line_slctd-taxis2_slctd)/step2_space[f])*step2_time[f], 1)
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
                    xaxis2_layout = dict(
                        title = x_ttl_txt_t,
                        title_standoff = stndff,
                        showgrid = (grid_clicks%2 == 0),#True,
                        gridcolor = grid_color,
                        zeroline = (grid_clicks%2 == 0),#True,
                        zerolinecolor = grid_color,
                        anchor = 'y',
                        overlaying = 'x',
                        side = 'top',
                        ticks = 'outside'
                        )
                # Time-Delay axes correspond with xaxis-2, 'bottom'
                elif nclicks%6==1:
                    #loc_t = 'bottom'
                    loc_s = 'top'
                    # No need for standoff param on bottom xaxis
                    xaxis2_layout = dict(
                        title = x_ttl_txt_t,
                        showgrid = (grid_clicks%2 == 0),
                        gridcolor = grid_color,
                        zeroline = (grid_clicks%2 == 0),
                        zerolinecolor = grid_color,
                        anchor = 'y',
                        overlaying = 'x',
                        side = 'bottom',
                        ticks = 'outside'
                        )
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
                    fig.update_layout(xaxis = dict(title = x_ttl_txt_s, title_standoff = stndff, side = loc_s, showgrid=(grid_clicks%2 == 0), gridcolor = grid_color, zeroline = (grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zeroline = (grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
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
                    fig.update_layout(xaxis = dict(title = x_ttl_txt_s, side = loc_s, showgrid=(grid_clicks%2 == 0), gridcolor = grid_color, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
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
                    fig.update_layout(xaxis = dict(title = x_ttl_txt, title_standoff = 0, side = loc, showgrid= (grid_clicks%2 == 0), gridcolor = grid_color, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
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
                    fig.update_layout(xaxis = dict(title = x_ttl_txt, side = loc, showgrid=(grid_clicks%2 == 0), gridcolor = grid_color, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
                                        yaxis = dict(title = y_ttl_txt, showgrid=False, zeroline=(grid_clicks%2 == 0), zerolinecolor = grid_color, ticks = 'outside'),
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
    fig.update_layout(legend_title_text = '<b>Trace: [Ch] - Scan<b>')#, width=675)
    
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
# Show/Hide colorbar/yaxis2, 'slct_y2', RadioItem controls display of second y-axis
@app.callback(Output({'type':'slct_y2', 'index': MATCH}, 'options'),
    [Input({'type':'slct_timeaxis2', 'index': MATCH}, 'value'),
    Input({'type':'tabs', 'index':MATCH}, 'active_tab')] )
def display_colorbar(taxis2_slctd, tab):
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
# Show/Hide colorbar/yaxis2, 'slct_y2', RadioItem controls display of second y-axis
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
@app.callback([Output({'type':'signal_range', 'index': MATCH},'min'),
    Output({'type':'signal_range', 'index': MATCH},'max'),
    Output({'type':'signal_range', 'index': MATCH},'step'),
    Output({'type':'signal_range', 'index': MATCH},'value'),
    Output({'type':'signal_range', 'index': MATCH},'marks'),
    Output({'type':'signal_range', 'index': MATCH},'verticalHeight')], 
    [Input({'type':'slct_channel', 'index': MATCH},'value'),
    Input({'type':'slct_scan', 'index': MATCH},'value'),
    Input('memory-data', 'data')])
def update_rangeslider(channel_slctd, scan_slctd, active_f):
    print()
    print('update_rangeslider')
    print('active_f:', active_f)
    print('active_f type:', type(active_f))
    print()
    if active_f is None:
        f = 0
    elif active_f is not None:
        f = active_f
    # Modify formatted data dictionary for user input
    dff = data_dict[f].copy()
    dff = dff[scan_slctd][channel_slctd]
    
    # Identify Min/Max/Range for SLider callbacks
    min_min = round(dff.min().min(), 6)
    max_max = round(dff.max().max(), 6)
    vals = [min_min, max_max]
    sig_step = round((max_max - min_min)/100,7)
    range_marks={min_min:{'label':'Sig Min: '+str(min_min), 'style':{'color':'blue', 'font-weight':'bold', 'right':'40px'} }, max_max:{'label':'Sig Max: '+str(max_max), 'style':{'color':'#f50', 'font-weight':'bold', 'vertical-align':'text-top','right':'40px'}}}
    # 'signal_range' verticalHeight
    range_height = 30 # num_m2steps[f]*(mag_factor+5)
    return min_min, max_max, sig_step, vals, range_marks, range_height
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Input n_clicks property from 'add_graph' bttn to dynamically add subplots via pattern-matching callbacks
@app.callback(Output({'type':'2d_scan_surf', 'index': MATCH},'figure'),
    [Input({'type':'slct_channel', 'index': MATCH},'value'),
    Input({'type':'slct_scan', 'index': MATCH},'value'),
    Input({'type':'slct_timeaxis1', 'index': MATCH},'value'),
    Input({'type':'slct_x2', 'index': MATCH},'value'),
    Input({'type':'slct_timeaxis2', 'index': MATCH},'value'),
    Input({'type':'slct_y2', 'index': MATCH},'value'),
    Input({'type':'signal_range', 'index': MATCH},'value'),
    Input('memory-data', 'data')])
def update_heatmap(channel_slctd, scan_slctd, taxis1_slctd, x2_slctd, taxis2_slctd, y2_slctd, cbar_range, active_f):    
    # Set base figure for subplots
    fig = make_subplots(rows = 1, #Display how many rows of objects 
                        cols = 1, #Display how many side-by-side?
                        specs=[[{'secondary_y':True}]],
                        shared_xaxes = False,
                        shared_yaxes = False)
    # Debugging
    print()
    print('update_heatmap')
    print('active_f:', active_f)
    print('active_f type:', type(active_f))
    print()
    # Try/Except
    if active_f is None:
        f = 0
    elif active_f is not None:
        f = active_f
    # Modify formatted data dictionary for user input
    dff = data_dict[f].copy()
    dff = dff[scan_slctd][channel_slctd]
        
    # Display Motor-X Positions
    if (taxis1_slctd==None) & (taxis2_slctd==None):
        xdata = dff.columns
        ydata = dff.index
        x_title_txt = '<b>Target-Position: Motor 1 [mm]<b>'
        y_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        x_range = [m1_positions[f][0]-(step1_space[f]/2), m1_positions[f][-1]+(step1_space[f]/2)]
        y_range = [m2_positions[f][0]-(step2_space[f]/2), m2_positions[f][-1]+(step2_space[f]/2)]
    # Display Pump-Probe Time-Delay Axis: T (from Motor-1 scans)
    elif (taxis1_slctd != None) & (taxis2_slctd == None):
        m1_zero = taxis1_slctd
        time_ax1 = np.round( ((dff.columns-m1_zero)/step1_space[f])*step1_time[f], 1)
        xdata = time_ax1
        ydata = dff.index
        x_title_txt = '<b>Pump-Probe (T) Delay [fs]<b>'
        y_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        x_range = [time_ax1[0]-(step1_time[f]/2), time_ax1[-1]+(step1_time[f]/2)]   
        y_range = [m2_positions[f][0]-(step2_space[f]/2), m2_positions[f][-1]+(step2_space[f]/2)]
    # Display Drive-Probe Time-Delay Axis: TAU (from Motor-2 scans)
    elif (taxis1_slctd == None) & (taxis2_slctd != None):
        m2_zero = taxis2_slctd
        time_ax2 = np.round( ((dff.index-m2_zero)/step2_space[f])*step2_time[f], 1)
        xdata = dff.columns
        ydata = time_ax2
        x_title_txt = '<b>Target Position: Motor 1 [mm]<b>'
        y_title_txt = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
        x_range = [m1_positions[f][0]-(step1_space[f]/2), m1_positions[f][-1]+(step1_space[f]/2)]
        y_range = [time_ax2[0]-(step2_time[f]/2), time_ax2[-1]+(step2_time[f]/2)]
    # Display Both Time-Delay Axes: T & TAU
    elif (taxis1_slctd != None) & (taxis2_slctd != None):
        m1_zero = taxis1_slctd
        m2_zero = taxis2_slctd
        time_ax1 = np.round( ((dff.columns-m1_zero)/step1_space[f])*step1_time[f], 1)
        time_ax2 = np.round( ((dff.index-m2_zero)/step2_space[f])*step2_time[f], 1)
        xdata = time_ax1
        ydata = time_ax2
        x_title_txt = '<b>Pump-Probe (T) Delay [fs]<b>'
        y_title_txt = '<b>Drive-Probe (\N{MATHEMATICAL BOLD ITALIC SMALL TAU}) Delay [fs]<b>'
        x_range = [time_ax1[0]-(step1_time[f]/2), time_ax1[-1]+(step1_time[f]/2)]
        y_range = [time_ax2[0]-(step2_time[f]/2), time_ax2[-1]+(step2_time[f]/2)]
##############################################################################################################################################################################################      
    # https://plotly.com/python/builtin-colorscales/
    palettes = ['Viridis', 'Magma', 'haline', 'Plasma','thermal', 'Hot', 'RdBu_r','RdYlBu_r', 'Spectral_r','PRGn', 'curl', 'delta', 'Tropic', 'Blackbody', 'oxy']
    palette = palettes[1]

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
        x2_range = [m1_positions[f][0]-(step1_space[f]/2), m1_positions[f][-1]+(step1_space[f]/2)]
        x_axis2 = {'title' : {'text' : x2_title_txt}, 'overlaying':'x', 'side': 'top', 'nticks': 5, 'ticks': 'outside', 'tickson': 'boundaries','color' : 'black','showline': False,'showgrid': False,'zeroline': False, 'range' : x2_range }
    elif x2_slctd == 'x':
        x_axis2 = None

    # SECONDARY Y-AXIS, display both Motor-2 Position & Time-Delay: Tau 'Drive-Probe'
    if y2_slctd == 'y2':
        y2_title_txt = '<b>Target Position: Motor 2 [mm]<b>'
        y2_range =  [m2_positions[f][0]-(step2_space[f]/2), m2_positions[f][-1]+(step2_space[f]/2)]
        y_axis2 = dict(title = y2_title_txt, #{'text' : y2_title_txt},
            overlaying = 'y',
            side = 'right',
            nticks = 5,
            ticks = 'outside',
            tickson = 'boundaries',
            color = 'black',
            showline = False,
            showgrid = False,
            zeroline = False,
            range = y2_range )
    elif y2_slctd == 'y':
        y_axis2 = None
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
    fig.update_layout(
        xaxis = dict(title = x_title_txt,
                nticks = 5,
                ticks = 'outside',
                side = 'bottom',
                color = 'black',
                showline = False,
                showgrid = False,
                zeroline = False,
                range = x_range ),
        yaxis = dict(title = y_title_txt,
                nticks = 5,
                ticks = 'outside',
                side = 'left',
                color = 'black',
                showline = False,
                showgrid = False,
                zeroline = False,
                range = y_range ),)
    fig.update_layout({
        'xaxis2': x_axis2, # None (default) or Dict
        'yaxis2': y_axis2, # None (default) or Dict
        'coloraxis': {'showscale' : False},},
        width = 580, #int(xwidth[f])*mag_factor, 
        height = 530, #int(ywidth[f])*mag_factor,
        coloraxis_colorbar_xpad = 300,coloraxis_colorbar_ypad = 300,coloraxis_colorbar_bgcolor = 'black',coloraxis_colorbar_bordercolor = 'black',coloraxis_colorbar_outlinecolor = 'black',coloraxis_colorbar_tickcolor = 'black',paper_bgcolor = 'rgb(160,160,160)',plot_bgcolor = 'black',title_text = ttl_txt,font_color = 'black',margin_autoexpand = True,margin_l = 110,margin_r = 120,margin_t = 120,autosize = False)
    #==============================================================================================
    # What is returned here will actually go to the output
    # First:  'component_property = children'
    # Second: 'component_property =   figure'
    # Hide colorbar when secondary axis-right is clicked
    if (y2_slctd=='y2'):
        fig.update_traces(showscale=False, selector=dict(type='heatmap'))
    return fig # END callbacks.py