<a id='back_to_top'></a>

# Dashboard for Data Analysis & Visualization:
### Supporting Ultrafast Transient Polarization Spectroscopy (UTPS)

---
### Problem Statement:
> Researchers in the Atomic-Molecular-&-Optical-Sciences Group, within the Chemical Sciences Division at Berkeley Lab (LBNL), have developed a novel technique for investigation of nonlinear physical processes with time-resolved measurements scaled at the molecular level. This project was performed to support automation of redundant data processing tasks and to develop open-source visualization tools that increase effiency of data analysis performed in the laboratory.

#### **Exploration of the following specific goals:**
* Alleviate restrictive dependencies on generic proprietary visualization software.
    * Oversee DAQ remotely, from multiple machines.
    * Provide flexibility of display through additional control options.
    * Allow for user driven modifications as the technique evolves.<br><br>
* Quantify quality of data throughout DAQ procedures.<br><br>
* Visualize data from multiple sources, for direct comparisons.
    * Dynamically generate interactive graph traces of multidimensional data.
    * Zoom into user defined quadrants of interest.<br><br>
    * Import datasets from multiple files.
* Enhance ease of analytic collaboration between researchers.
---
## Table of Contents

* [`Multi-Page Apps and URL Support`] (Dash.Plotly Reference Guide): ([*Structuring a Dash App Layout*](https://dash.plotly.com/urls))

- app.py
- index.py
- callbacks.py
- layouts.py

* [Experiment Details](#experiment_details)
* [EDA & Data Cleaning](#eda_and_cleaning)
    * [Data Dictionary](#appendix)
* [Preprocessing](#preprocessing_and_feature_engineering)
* [Benchmarks](#model_benchmarks)
* [Model Tuning](#model_tuning)
* [Next Steps](#recommendations_and_next_steps)
* [Software Requirements](#software_requirements)
* [Acknowledgements and Contact](#acknowledgements_and_contact)

<a id='experiment_details'></a>

---
## Experiment Details
    NOTE: This section is a simplified overview of the experimental setup. For advanced readers interested in a rigorous breakdown, see assets folder contents.

[Back to Top](#back_to_top)

The raw data are voltage signals representing variations to well characterized laser light, after it interacts with molecules in carefully prepared energy states. The process requires three laser pulses to irradiate the molecular target in a precisely timed sequence. Two motors are remotely operated which direct The response of a molecule to light occurs very quickly so timing is everything. The researchers overcome this challenge by conducting a scan. The bottom line is researchers are using two motors 

### Experiment goal: Measure 3rd order nonlinear optical response
* Q: OKE from Kerr-media sample due to AC laser E-Field

* Q: 2 Optical Delay Stages
>* Time Delay T: "x-time", horizontal axes in the time domain, typically femtoseconds. One femtosecond [fs] equals 1E-15 seconds [secs], Motor-Target_1.<br>
NOTE: A motor in the experiment moves the beampath of a laser(actually two motors and two beampaths). A laser-pulse moves at the speed of light such that the direction of the beampath requires light to travel twice the distance that the motor-position steps. 

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

<a id='eda_and_cleaning'></a>

---
## EDA & Data Cleaning
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

#### EDA
- Missing Values:

#### Data Cleaning
- Null Value Imputation:
- Manage Outliers:

<a id='preprocessing_and_feature_engineering'></a>

---
## Pre-Processing and Feature Engineering
[Back to Top](#back_to_top)

***Pre-processing***
> * Set-up terminology of lab to describe tool optionality


<a id='model_benchmarks'></a>

---
## Model Benchmarks and Preparation
[Back to Top](#back_to_top)

<a id='model_tuning'></a>

---
## Model Tuning & Assessment
[Back to Top](#back_to_top)

<a id='recommendations_and_next_steps'></a>

---
## Recommendations and Next Steps
[Back to Top](#back_to_top)

<a id='software_requirements'></a>

---
## Software Requirements
[Back to Top](#back_to_top)

<a id='acknowledgements_and_contact'></a>

---
## Acknowledgements and Contact:
[Back to Top](#back_to_top)


### External Resources:
* [`Title`] (Platform): ([*source*](https://www.URL.com))

* [`Overview of AxesGrid toolkit`] (Documentation): ([*source*](https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html))

Google folder UTPS Online Analysis that has one example and a header.  
Starting point - upload example notebook or script (Graphs of 2D time-delay scans), helpful in comparing lab measurements



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