#!/usr/bin/env python

# IMPORTS:
import dash  # (version == 1.12.0)

# Module containing links for Bootswatch themes https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
from dash_bootstrap_components import themes

### BUILD THE APP - Define Dash instance

# Dashboard entry through index.py
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[themes.SPACELAB])

# Alternatively: Render Dashboard with Jupyter
#from jupyter_dash import JupyterDash
#app = JupyterDash(__name__, suppress_callback_exceptions=True, external_stylesheets=[themes.SPACELAB])

# Expose the Flask variable in the file
server = app.server