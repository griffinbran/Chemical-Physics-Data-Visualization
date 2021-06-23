#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# IMPORTS:

# Library containing component classes for HTML tags
import dash_html_components as html
# Bootstrap components for Dash to customise CSS theme & grid layout
import dash_bootstrap_components as dbc

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
            html.H1(['Ultrafast Transient Polarization Spectroscopy', dbc.Badge('UTPS', className='ml-1')]), width={'size': 'auto', 'order': 'last', 'offset': 1},
        ),
        dbc.Col(
            # Adds button for dynamic callback to make subplot
            html.Div([ dbc.Button('Subplots', id='add_graph', n_clicks=0, outline = False, size='sm') ] ), width={'size': 'auto', 'order': 'first', 'offset': 0},
            )
    ]),
    # All graphs/components go into this empty list: 'children'
    html.Div(id='container', children=[])
    ], fluid=True) # END of app.layout(...)
#=======================================================================================================================================================
data_dpdn_items = [dbc.DropdownMenuItem('Filename', header=True)]
for idx, d in enumerate(pp.datasets):
    data_dpdn_items.append(dbc.DropdownMenuItem(divider=True))
    data_dpdn_items.append(dbc.DropdownMenuItem(str(idx)+d, id=f'filename{idx}', active=(d==pp.active_data)))
#data_dpdn_items.extend([dbc.DropdownMenuItem(d) for d in pp.datasets])
     #[Input(id=f'filename{idx}', 'active')]
     #       function(*[f'filename{idx}' for idx, d in enumerate(pp.datasets)])
     #       from itertools import chain
     #       [chain.from_iterable((f'filename{idx}', 'nclicks') for idx in range(len(pp.datasets)) ]