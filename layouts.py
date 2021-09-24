#!/usr/bin/env python

# IMPORTS:
import dash_html_components as html # Library containing component classes for HTML tags
import dash_bootstrap_components as dbc # Customise CSS theme & grid layout
import dash_core_components as dcc # Library of dashboarding components
from preprocessing import datasets

# App layout:
layout1 = dbc.Container([
    dbc.Row([
        dbc.Col(
            # Add a title(H1) on the webpage aligned to the center of the page
            html.H2(['Ultrafast Transient Polarization Spectroscopy', dbc.Badge('UTPS', className='ml-1')]), width={'size': 'auto', 'order': 'last', 'offset': 0},
        ),
        dbc.Col(
            # Adds button for dynamic callback to make subplot
            html.Div([ dbc.Button('Add Subplot', id='add_graph', n_clicks=0, outline = False, size='sm') ] ), width={'size': 'auto', 'order': 2, 'offset': 0},
            ),
        # Dataset Dropdown Column
        dbc.Col([
            dcc.Store(id='memory-data', storage_type='memory'),
            #dbc.Label( 'filename:', id='datasets1', size='sm', html_for='files1'),
            dbc.DropdownMenu(id = 'files', label='Data ', bs_size="sm", direction='down',
                children =
                [
                    dbc.DropdownMenuItem(d, id = f'filename{idx}', active=(d==datasets[0])) for idx, d in enumerate(datasets)
                ],
            ),
            #dbc.FormText(f'Available Data', color='secondary'),
            ], width={'size':'auto', 'order':'first'} # END of dbc.Col children = [ datasets, files, filename{idx} ]
        ) # END of COL
    ]),
    # All graphs/components go into this empty list: 'children'
    html.Div(id='container', children = [])
    ], fluid=True) # END of app.layout(...)
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# END layouts.py
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=