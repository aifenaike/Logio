# Homelander
**Society of Petroleum Engineers, University of Ibadan Chapter**  
    *Submission for the SPE Lagos Section Hackathon*

Python package for well log analysis and visualization using python, matplotlib and pandas.
![Alternate Text](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

> [LAS Files](#Las-Files)  
> [Features](#Features)  
> [Dependencies](#Dependencies)  
> [Installation](#Installation)  
> [Getting Started](#Getting-Started)  
> [Credits and References](#Credits-and-References)  
> [Support](#Support)  
> [Authors](#Authors)  

---

### LAS Files

A **LAS** file contains physical properties data of vertical subsurface used in well log analysis.  
Well log data saved in LAS file generally contains information, including its file **version**, **well description**, **physical rock curve** along with **data table** and **other information** related to the well data.

---

### Features
Here are a few of the things that the package does well:

* Loads LAS data from various sources:
    - URL link (`https://example.com/.../.../path/to/lasfile.LAS`)
    - Local file (`path/to/lasfile.LAS` instead without `https`)
* Robust IO framework for loading data from flat files (CSV and delimited), Excel files, las files and JSON.
* Parsing well log data into any of the formats mentioned above.
* Hardcoded and flexible implementations for visualization of well logs and non-well log data, but in log format
* A novel system for well-to-well log correlation using dynamic depth warping techniques.
    - correlating well logs and obtaining the minimum-cost or "best" match.
---

### Dependencies

This project uses **Python 3** with dependencies provided in **[requirements.txt](requirements.txt)**. 

---

### Installation

Clone this repository using this command below on Terminal (Linux or Mac) or <a href="https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux" target="_blank"><abbr title="Windows Subsystem for Linux">WSL</abbr></a> (Windows).
```sh
git clone https://gitlab.com/aifenaike/spe_ui_lagos_hackathon
cd SPE_UI_LAGOS_HACKATHON
```

Python environment setup is recommended for using this project repository.  
Type `./check-pyenv.sh` (using Linux/Unix terminal console or WSL console) to validate Python environments. By default, Python `virtualenv` has not been set yet, returning the result below.
```sh
'env' directory does not exist.
```
Install the Python virtualenv (and also activate it) using
```sh
virtualenv env
source env/bin/activate 
```
You can now proceed to install required packages by running
```sh
pip install -r requirements.txt
```

Alternatively, you can [create the environment variable manually](https://docs.python.org/3/library/venv.html) by typing the commands below on Linux or MacOS (and also WSL console).

```sh
python -m venv venv
source venv/bin/activate
```
and for Windows.
```sh
python -m venv venv
venv\Scripts\activate
```
In terminal, just type the yellow text given to proceed.

---

### Getting Started
Load and plot a well log from ```.las``` file
```python
from speui.core import Analysis
from speui.logplot import PlotWell, LogPlot

# Read in your data from a .las file
data = Analysis().read_file(filename="data/15_9-F-11B.LAS")
data.df().head()

# Plot a GR log with a cutoff delineating shale from sand volumes
LogPlot(data).cutoff_plot(x="GR", y="DEPTH", x_cutoff=0.45,  y_range= (0,0),xscale='linear',labels= ['Sand', 'Shale'], 
                          fig_size = (4.5, 7),colors=['#964B00','#101010']) 
```
![Gamma Ray Cutoff Plot](attachment:image-3.png)
See the [tutorials](speui/) to explore the package step-by-step.

---

### Credits and References

 - [**Schlumberger** Log Interpretation Principles\Applications](https://www.slb.com/resource-library/book/log-interpretation-principles-applications)
 
---

### Support

For support, email alexander.ifenaike@gmail.com

---

### Authors

- [Gbenga Thompson](https://www.linkedin.com/in/gbenga-awojinrin)
- [Gbenga Thompson](https://www.linkedin.com/in/gbenga-awojinrin)
- [Gbenga Thompson](https://www.linkedin.com/in/gbenga-awojinrin)
- [Gbenga Thompson](https://www.linkedin.com/in/gbenga-awojinrin)
- [Gbenga Thompson](https://www.linkedin.com/in/gbenga-awojinrin)


[back to top](#Homelander)

