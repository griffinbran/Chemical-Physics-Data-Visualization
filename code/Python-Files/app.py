#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# IMPORTS:
#import preprocessing
# Python framework for building web apps
import dash  # (version == 1.12.0)
# Bootstrap components for Dash to customise app theme & grid layout
import dash_bootstrap_components as dbc

### BUILD THE APP
# <__name__> Flask uses for app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SPACELAB])
# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.GRID]) # Grid system only, no CSS typography applied to layout
# app = DashProxy(__name__, transforms=[MultiplexerTransform()], suppress_callback_exceptions=True)
#app.config.suppress_callback_exceptions=True
# Alternatively: Render dashboard in Jupyter
# from jupyter_dash import JupyterDash
# app = JupyterDash(__name__)

# Expose the Flask variable in the file
server = app.server

