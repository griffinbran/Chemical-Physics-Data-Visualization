<a id='back_to_top'></a>

# Dashboard for Data Analysis & Visualization:
### Supporting Ultrafast Transient Polarization Spectroscopy (UTPS)

---
### Problem Statement:
> Researchers in the Atomic-Molecular-&-Optical-Sciences Group, within the Chemical Sciences Division at Berkeley Lab (LBNL), have developed a novel technique for investigation of nonlinear physical processes with time-resolved measurements scaled at the molecular level. This project was performed to support automation of redundant data processing tasks and to develop open-source visualization tools that increase effiency of data analysis performed in the laboratory.

#### **Exploration of the following specific goals:**
1. Alleviate restrictive dependencies on generic proprietary visualization software.
    * Oversee DAQ remotely, from multiple work stations.
    * Provide flexibility of display through additional control options.
    * Allow for user driven modifications as the technique evolves.<br><br>
2. Visualize data from multiple sources, for direct comparisons.
    * Dynamically generate interactive graph traces of multidimensional data.
    * Zoom into user defined quadrants of interest.
    * Import datasets from multiple files.<br><br>
3. Quantify quality of data throughout DAQ procedures.
4. Enhance ease of analytic collaboration between researchers.
---
## Table of Contents

* [App Overview](#app_overview)
* [Background](#background)
* [Data Processing & Visualization](#processing_and_visualization)
    * [Data Dictionary](#appendix)
* [Next Steps](#next_steps)
* [Software Requirements](#software_requirements)
* [Acknowledgements and Contact](#acknowledgements_and_contact)

<a id='app_overview'></a>

---
## App Overview

5 Python files to run the dashboard:

* [`preprocessing.py`]: Load raw data with Pandas
* [`app.py`]: Build the app: Define Dash instance with *app* variable
* [`index.py`]: Entry point: Run the app
* [`callbacks.py`]: Define interactivity of visuals
* [`layouts.py`]: Dashboard structure

Instructions:
1. Install packages listed in Python3 Dashboard requirements.txt file located in the root directory of this repository
2. Assign a relative path for datasets in preprocessing.py (DEFAULT: trial dataset in `data` folder located in the root directory)
3. Run index.py (see Software Requirements below to alternatively launch app with Jupyter)

[Back to Top](#back_to_top)

<a id='background'></a>

---
## Background

### Where does the data come from?

    NOTE: This section is a simplified overview of the UTPS technique. 
    Advanced & curious readers may discover a more thorough overview in the assets folder.

[Back to Top](#back_to_top)

The raw data are voltage signals representing variations to well characterized laser light after it interacts with a carefully prepared molecular target. The technique requires three laser pulses to arrive on target in a precisely timed sequence. To control the timing, two remotely operated motors (A.K.A. "delay-axes") vary the path length of each pulse by directing them through a labrynth of optics.<br><br>
The response of a molecule to light occurs very, very rapidly so timing is an important challenge faced by the reasearchers. To overcome this hurdle the team conducts a methodical scan over a calculated range of motor positions (which directly convert to time delays) through a series of evenly spaced steps. This scanning process is repeated several times, over the course of several hours, providing a fair amount of opportunity for equipment to malfunction, changes in the laboratory environment to occur, etc. This dashboard is used to aid in identification of the optimally timed sequence of interaction-events and to understand fluctuations in the data, as well as to make new discoveries supported by the U.S. Department of Energy's Basic Energy Sciences Program.

### Bottom Line: Measure the 3rd order nonlinear optical response from a molecule.

* *Configuration #1 :* "3-Pulse Experiment"
    >1. Excitation (pump) Pulse
    >2. Kerr Gating (drive) Pulse --> Photodiode #3
    >3. Probing Pulse --> Photodiodes #1 & #2 (no cross polarizer)

* *Configuration #2 :* "No Probe Experiment"
    >1. Excitation (pump) Pulse
    >2. Kerr Gating (drive) Pulse
    >3. Probe BLOCKED

* *Configuration #3 :* "No Drive Experiment"
    >1. Excitation (pump) Pulse
    >2. Drive BLOCKED
    >3. Probing Pulse
    
<a id='processing_and_visualization'></a>

---
## Processing & Visualization

[Back to Top](#back_to_top)

### Datasets

* [Data Dictionary](#appendix)

#### Sample Dataset

* [`trial_output05.tsv`](./data/trial_output05.tsv): Description ([source](http://URL.com) | [data dictionary](http://URL.com))

**Notes about the data:**
1. n = Total number of motors moving, through a set of predetermined positions, during each scan.
> * n = 1: Motor for Pump-Pulse to Probe-Pulse Delay Axis (T)
> * n = 2: Motor for Kerr-Gating-Drive-Pulse to Probe-Pulse Delay Axis (Tau)
> * n = 3: Motor for polarization control (hypothetical future implementation)
> * n = 4: Motor for sample position control (hypothetical future implementation)
> * Dimensions of motor position are millimeters, with a direct conversion to femtoseconds

2. The tab separated text files store original research data from 8 independent channels acquired with NIDAQ-National Instruments Data Acquisition software.
> * Channels are 0-indexed from 0-7
> * Future research may incorporate more channels than 8.

#### Errors
- An error may consist of a communication error b/w laser-motor system & acquisition computer. Motors will be reinitialized, and the scan is restarted.

#### Data Cleaning
- Raw data is aggregated by averaging all ACTUAL motor positions, grouped by each TARGET position.

<a id='next_steps'></a>

---
## Next Steps
[Back to Top](#back_to_top)

1. Create a remove subplot feature
2. Add a box and whisker plot to scan data
3. Present dataset synopsis on dashboard
4. Support real-time updates
5. Include warning response for clearing input
7. Deploy with Heroku

<a id='software_requirements'></a>

---
## Software Requirements
[Back to Top](#back_to_top)

See requirements.txt listed in root directory

#### ADDITIONAL REQUIREMENTS:

* To render dashboard from Jupyter

1. Edit app.py<br>
> COMMENT OUT: `app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[themes.SPACELAB])`<br>
> UNCOMMENT IMPORT: `from jupyter_dash import JupyterDash`<br>
> UNCOMMENT: `app = JupyterDash(__name__, suppress_callback_exceptions=True, external_stylesheets=[themes.SPACELAB])`<br>

2. Launch app-jupyter.ipynb
3. Install additional requirements listed in first cell
4. Run second cell in place of index.py


<a id='acknowledgements_and_contact'></a>

---
## Acknowledgements and Contact:
[Back to Top](#back_to_top)


### External Resources:
* [`Dash Python User Guide`] (Documentation): ([*Dash.Plotly Reference Guide*](https://dash.plotly.com/))
* [`Dash Bootstrap Components`] (Documentation): ([*source*](https://dash-bootstrap-components.opensource.faculty.ai/docs/))
* [`Plotly Graphing Library: Creating and Updating Figures`] (Documentation): ([*source*](https://plotly.com/python/reference/layout/))
* [`Heatmap Graph Object`] (Documentation): ([*Plotly API Reference*](https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Heatmap.html))
* [`Scatter Graph Object`] (Documentation): ([*Plotly API Reference*](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html))
* [*`Community Forum`*] (User Support): ([*Plotly*](https://community.plotly.com/))
* [`Charming Data`] (Video Tutorials): ([*YouTube Channel*](https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ))

### UTPS Papers:
* [`Time-Resolved Ultrafast Transient Polarization Spectroscopy...`](./assets/TimeResolvedUltrafastTransientPolarizationSpectroscopy.pdf) Review of Scientific Instruments: ([*source*](https://aip.scitation.org/doi/10.1063/1.5144482))
* [`Ultrafast Dynamics of Excited Electronic States in Nitrobenzene...`](./assets/UltrafastDynamicsofExcitedElectronicStatesinNitrobenzene.pdf) Journal of Physical Chemistry A: ([*source*](https://pubs.acs.org/doi/10.1021/acs.jpca.0c01943?ref=pdf))

### Contacts:
> * Data Analyst: Brandon Griffin [GitHub](https://github.com/griffinbran) | [LinkedIn](https://www.linkedin.com/in/griffinbran/) | [Twitter](https://twitter.com/GriffinBran) | [Medium](https://griffinbran.medium.com)
> * UTPS Scientist: Richard Thurston, PhD Candidate [Email](rthurston@lbl.gov)
> * Postdoctoral Researcher: Matthew Brister, PhD [Email](mmbrister@lbl.gov)
> * LBNL Staff Scientist: Daniel Slaughter, PhD  [Website](https://amos.lbl.gov/slaughter/) | [Email](dslaughter@lbl.gov)

<a id='appendix'></a>

---
## Appendix: Data Dictionary

[Back to Top](#back_to_top)

### Datasets Dictionary
* Data located in the `relative_path` directory are stored as Pandas DataFrames in the list-object `data_dict`.

|Column|Data Type|Variable|Location|Description|
|---|---|---|---|---|
|**#errors**|*int*|data_dict[i]|preprocessing.py|Miscommunication "connection" error flag|
|**scan#**|*int*|data_dict[i]|preprocessing.py|Name of the trial run for each experiment|
|**motor-target_n**|*float*|data_dict[i]|preprocessing.py|Position targeted by nth motor|
|**motor-actual_n**|*float*|data_dict[i]|preprocessing.py|Position reported by nth motor|
|**data_channel_n**|*float*|data_dict[i]|preprocessing.py|Raw signal from two photodiodes|

### Components Dictionary

|Component ID|Library|Name|Filename|Description|
|---|---|---|---|---|
|**add_graph**|*Dash Bootstrap*|Subplots|layouts.py|Appends a duplicate dashboard to existing state|

### Callback Dictionary

|Callback Name|Output|Arguments|Filename|Description|
|---|---|---|---|---|
|**update_active_filename**|*filename{idx}*|*args_nclicks|callbacks.py|Based on n-clicks, updates active filename|

[Back to Top](#back_to_top)

---