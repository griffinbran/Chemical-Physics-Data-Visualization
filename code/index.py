#!/usr/bin/env python

# IMPORTS:
from app import app
from layouts import layout1
import callbacks

# Set the layout of the app
app.layout = layout1

# Entry point for running the app:
if __name__ == '__main__':
    # Default: visit http://127.0.0.1:8050/ in your web browser.
    app.run_server(debug=True, use_reloader=False, host='127.0.0.1', port='8050')