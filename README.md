# Ongoing Project: Work-in-Progress

<img src="file_name.jpg" alt="UTPS" style="height: 310px; width:660px;"/>

<a id='back_to_top'></a>

# LBNL Ultrafast Transient Polarization Spectroscopy (UTPS) Visualization
---
### Problem Statement:
> Physicists, in the Chemical Sciences Division at Berkeley Lab (LBNL), have developed a novel technique for investigation of nonlinear physical processes with time-resolved measurements scaled at the molecular level. This project aims to automate data processing, develop data visualization tools, and advance database management to increase effiency of data acquisition and assist in cutting time-cost of performing redundant visualization tasks.

#### **Exploration of the following specific goals:**
* Quantify scan (data) qualtiy in reference to the others.
* Visualize 2D time-delay scans for each of the 8-channels in a way that benefits direct comparisons.

---
### Table of Contents (NOTE: This will be reformatted to match the project type!)

* [EDA & Data Cleaning](#eda_and_cleaning)
    * [Data Dictionary](#appendix)
* [Preprocessing & Feature Engineering](#preprocessing_and_feature_engineering)
* [Model Benchmarks](#model_benchmarks)
* [Model Tuning](#model_tuning)
* [Production Model & Insights](#production_model_and_insights)
* [Recommendations and Next Steps](#recommendations_and_next_steps)
* [Software Requirements](#software_requirements)
* [Acknowledgements and Contact](#acknowledgements_and_contact)

<a id='eda_and_cleaning'></a>

---
## EDA & Data Cleaning

### Datasets

* [Data Dictionary](#appendix)

#### Raw Training Dataset

* [`file_name.csv`](./filepath.csv): Description ([source](http://URL.com) | [data dictionary](http://URL.com))

#### Raw Validation Dataset

* [`file_name.csv`](./filepath.csv): Description ([source](http://URL.com) | [data dictionary](http://URL.com))

#### Processed Datasets:
* [`file_name.csv`](./filepath.csv): Description

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
> * Set-up Models
>* One-hot encode categorical variables
>* Train/test split the data
>* Scale the data
>* Consider using automated feature selection


<a id='model_benchmarks'></a>

---
## Model Benchmarks and Preparation
[Back to Top](#back_to_top)

<a id='model_tuning'></a>

---
## Model Tuning & Assessment
[Back to Top](#back_to_top)

<a id='production_model_and_insights'></a>

---

## Production Model & Insights
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
Google folder UTPS Online Analysis that has one example and a header.  
Starting point - upload example notebook or script (Graphs of 2D time-delay scans), helpful in comparing lab measurements
### Papers:
* [`Time-Resolved Ultrafast Transient Polarization Spectroscopy...`](./assets/TimeResolvedUltrafastTransientPolarizationSpectroscopy.pdf) Review of Scientific Instruments: ([*source*](https://aip.scitation.org/doi/10.1063/1.5144482))
* [`Ultrafast Dynamics of Excited Electronic States in Nitrobenzene...`](./assets/UltrafastDynamicsofExcitedElectronicStatesinNitrobenzene.pdf) Journal of Physical Chemistry A: ([*source*](https://pubs.acs.org/doi/10.1021/acs.jpca.0c01943?ref=pdf))
* [*`Title`*](./file_path.pdf) Journal/Blog: ([*source*](https://www.URL.com))

### Contacts:
> * Data Scientist: Brandon Griffin [GitHub](https://github.com/griffinbran) | [LinkedIn](https://www.linkedin.com/in/griffinbran/) | [Twitter](https://twitter.com/GriffinBran) | [Medium](https://griffinbran.medium.com)
> * Principal Investigator: Richard Thurston  [email](rthurston@lbl.gov)
> * LBNL Staff Scientist: Daniel Slaughter, PhD  [Website](https://amos.lbl.gov/slaughter/)

<a id='appendix'></a>

---
## Appendix: Data Dictionary

[Back to Top](#back_to_top)

|Feature Name|Data Type|Dataset|Category|Description|
|---|---|---|---|---|
|**Name**|*DType*|Data Source|'Key' : 'Value'|Type of building|
|**#errors**|*int*|Data Source|'Key' : 'Value'|Type of building|
|**scan#**|*int*|Data Source|'Key' : 'Value'|Type of building|
|**motor-target_n**|*float*|Data Source|'Key' : 'Value'|Position targeted by nth motor|
|**motor-actual_n**|*float*|Data Source|'Key' : 'Value'|Position reported by nth motor|
|**data_channel_n**|*float*|Data Source|'Key' : 'Value'|Type of building|


[Back to Top](#back_to_top)

---