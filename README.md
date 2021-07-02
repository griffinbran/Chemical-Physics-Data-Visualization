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

* [`preprocessing.py`]: Read raw data into Pandas DataFrame
* [`app.py`]: Build the app with variables *app* and *server*
* [`index.py`]: Entry point for running the app
* [`callbacks.py`]: Callback definitions for interactivity with Plotly Graph Objects
* [`layouts.py`]: Dash components define app structure

[Back to Top](#back_to_top)

    
<a id='background'></a>

---
## Background

### Where does the data come from?

    NOTE: This section is a simplified overview of the UTPS technique. 
    Advanced & curious readers may discover a more thorough overview in the assets folder.

[Back to Top](#back_to_top)

The raw data are voltage signals representing variations to well characterized laser light after it interacts with a carefully prepared molecular target. The technique requires three laser pulses to arrive on target in a precisely timed sequence. To control the timing, two remotely operated motors (A.K.A. "delay-axes") vary the path length of each pulse by directing them through a labrynth of optics.<br><br>
The response of a molecule to light occurs very, very rapidly so timing is everything. The researchers overcome this challenge by conducting a methodical scan of motor positions (which directly convert to time delays) through a series of evenly spaced steps. This scanning process is repeated several times, over the course of several hours, providing opportunity for equipment malfunction, changes to the laboratory environment, etc. This dashboard is used to aid in identification of the optimally timed sequence of interaction-events and to understand fluctuations in the data, as well as to make new discoveries supported by the U.S. Department of Energy's Basic Energy Sciences Program.

### Experiment goal: Measure 3rd order nonlinear optical response

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
> * n = 1: Motor for...
> * n = 2: Motor for...
> * n = 3: Motor for polarization control (hypothetical future implementation)
> * n = 4: Motor for sample position control (hypothetical future implementation)
> * Dimensions of motor position are [mm], with a direct conversion to [fs]
> * NOTE: 1-femtosecond = 10^-15 [sec]

2. 8-Channels(output) from NIDAQ-National Instruments Data Acquisition (sensors/measurement hardware/programmable software)
> * 0-indexed from 0-7

#### Errors
- An error may consist of a communication error b/w laser-motor system & acquisition computer. Motors will be reinitialized, and the scan is restarted.

#### Data Cleaning
- Raw data is not altered in this dashboard.

***Pre-processing***
> * Set-up terminology of lab to describe tool optionality

<a id='next_steps'></a>

---
## Next Steps
[Back to Top](#back_to_top)

1. Create requirements.txt
2. Generate docstrings for callbacks
3. Work on data dictionary
4. Build callback dictionary
5. Build component dictionary

<a id='software_requirements'></a>

---
## Software Requirements
[Back to Top](#back_to_top)

See requirements.txt listed in root directory

#### ADDITIONAL REQUIREMENTS:

* Render dashboard in Jupyter

app.py<br>
> IMPORT: `from jupyter_dash import JupyterDash`<br>
> BUILD THE APP: `app = JupyterDash(__name__)`

preprocessing.py<br>
> IMPORT: `from jupyterthemes import jtplot`<br>
> STYLE: `jtplot.style(theme='solarizedd', context='notebook', ticks=True, grid=False)`

<a id='acknowledgements_and_contact'></a>

---
## Acknowledgements and Contact:
[Back to Top](#back_to_top)


### External Resources:
* [`Title`] (Platform): ([*source*](https://www.URL.com))

* [`Overview of AxesGrid toolkit`] (Documentation): ([*source*](https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html))

Google folder UTPS Online Analysis that has one example and a header.  
Starting point - upload example notebook or script (Graphs of 2D time-delay scans), helpful in comparing lab measurements
* [`Multi-Page Apps and URL Support`] (Dash.Plotly Reference Guide): ([*Structuring a Dash App Layout*](https://dash.plotly.com/urls))


### Papers:
* [`Time-Resolved Ultrafast Transient Polarization Spectroscopy...`](./assets/TimeResolvedUltrafastTransientPolarizationSpectroscopy.pdf) Review of Scientific Instruments: ([*source*](https://aip.scitation.org/doi/10.1063/1.5144482))
* [`Ultrafast Dynamics of Excited Electronic States in Nitrobenzene...`](./assets/UltrafastDynamicsofExcitedElectronicStatesinNitrobenzene.pdf) Journal of Physical Chemistry A: ([*source*](https://pubs.acs.org/doi/10.1021/acs.jpca.0c01943?ref=pdf))
* [*`Title`*](./file_path.pdf) Journal/Blog: ([*source*](https://www.URL.com))

### Contacts:
> * Data Analyst: Brandon Griffin [GitHub](https://github.com/griffinbran) | [LinkedIn](https://www.linkedin.com/in/griffinbran/) | [Twitter](https://twitter.com/GriffinBran) | [Medium](https://griffinbran.medium.com)
> * Principal Investigator: Richard Thurston  [email](rthurston@lbl.gov)
> * LBNL Staff Scientist: Daniel Slaughter, PhD  [Website](https://amos.lbl.gov/slaughter/)

<a id='appendix'></a>

---
## Appendix: Data Dictionary

[Back to Top](#back_to_top)

|Feature Name|Data Type|Dataset|Category|Description|
|---|---|---|---|---|
|**Name**|*DType*|Data Source|'Key' : 'Value'|Type of building|
|**#errors**|*int*|Data Source|'Key' : 'Value'|Miscommunication "connection" error|
|**scan#**|*int*|Data Source|'Key' : 'Value'|12 scans of all motor positions are averaged together|
|**motor-target_n**|*float*|Data Source|'Key' : 'Value'|Position targeted by nth motor|
|**motor-actual_n**|*float*|Data Source|'Key' : 'Value'|Position reported by nth motor|
|**data_channel_n**|*float*|Data Source|'Key' : 'Value'|Photodiode polarization data (voltages)|


[Back to Top](#back_to_top)

---