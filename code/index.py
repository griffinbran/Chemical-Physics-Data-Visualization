#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# IMPORTS
from app import app
from layouts import layout1
import callbacks

# Set the layout of the app
app.layout = layout1

# Entry point for running the app:
if __name__ == '__main__':
    # Load the app on specified URL: http://127.0.0.1:8050/ DEFAULT HOST:PORT
    app.run_server(debug=True, use_reloader=False, host='127.0.0.1', port='8050') 

    # Run app and display result inline in Jupyter notebook
    # app.run_server(mode='inline')