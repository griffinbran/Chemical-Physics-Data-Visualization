#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# IMPORTS:
import dash  # (version == 1.12.0)

# Module containing links for Bootswatch themes https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
from dash_bootstrap_components import themes

### BUILD THE APP: Define Dash instance
# <__name__> Flask uses for app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[themes.SPACELAB])

# Expose the Flask variable in the file
server = app.server

