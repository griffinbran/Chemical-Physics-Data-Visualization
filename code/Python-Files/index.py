#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Load the app on specified URL

# IMPORTS
import preprocessing
from app import app
from layouts import layout1
import callbacks
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
app.layout = layout1
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Entry point for running the app locatd in 'index.py' avoids circular imports
# See https://dash-docs.herokuapp.com/reference for more info
if __name__ == '__main__':
    # Run app on local server: http://127.0.0.1:8050/
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(debug=True, dev_tools_hot_reload=True, port=7777)
    # Run app and display result inline in the notebook
    # app.run_server(mode='inline')
#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# Export figure to HTML file to be reopened in a browser for full interactivity
# fig.write_html('../images/filename.html')
# Export figure to static image with Kaleido
# fig.write_image('../images/filename.png')
# fig.write_image('../images/filename.jpeg')
# fig.write_image('../images/filename.webp')

