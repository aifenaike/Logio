# SPE_UI_LAGOS_HACKATHON
SPE Lagos Section Hackathon - Solution Package for University of Ibadan Chapter

[What is LAS file](#what-is-las-file) | [Project feature(s)](#project-features) | [Project dependencies](#project-dependencies) | [Project setup](#project-setup) | [Getting started](#getting-started) | [License](#License)

---

### What is LAS file

**LAS** file contains physical properties data of vertical subsurface
used in well log analysis. Well log data saved in LAS file contains
some information, including its file **version**, **well description**,
**physical rock curve** along with **data table** and **other information** related to the well data.

[back to top](#SPE_UI_LAGOS_HACKATHON)

---

### Project feature(s)
Here are a few of the things that the package does well:

- Load LAS data from various sources:
    - URL link (`https://example.com/.../.../path/to/lasfile.LAS`)
    - Local file (`path/to/lasfile.LAS` instead without `https`)
- Visualization of well logs.
- Robust IO framework for loading data from flat files (CSV and delimited), Excel files, las files and JSON.
- Parsing well log data into any of the formats mentioned above.
- A novel system for well-to-well log correlation using dynamic depth warping techniques.
    - correlating well logs and obtaining the minimum-cost or "best" match.

[back to top](#SPE_UI_LAGOS_HACKATHON)

---

### Project dependencies

This project uses **Python 3** with dependencies provided in **[requirements.txt](https://gitlab.com/aifenaike/spe_ui_lagos_hackathon/-/blob/main/requirements.txt)**. 

[back to top](#SPE_UI_LAGOS_HACKATHON)

---

### Project setup

Firstly, you need to clone this repository using this command below on Terminal (Linux or Mac) or <a href="https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux" target="_blank"><abbr title="Windows Subsystem for Linux">WSL</abbr></a> (Windows).
```sh
git clone https://gitlab.com/aifenaike/spe_ui_lagos_hackathon
cd SPE_UI_LAGOS_HACKATHON
```

Python environment setup is recommended for using this project repository. Type `./check-pyenv.sh` (using Linux/Unix terminal console or WSL console) for validating Python environments. By default, Python `virtualenv` has not been set yet so that it will be return results as below.

```sh
'env' directory is not exist.
 you can install Python virtualenv (and also activate it) by
 virtualenv env
 source env/bin/activate 

 install Python dependencies then by
 pip install -r requirements.txt
```

or you can [create the environment variable manually](https://docs.python.org/3/library/venv.html) by typing command below on Linux or MacOS (and also WSL console).

```
python -m venv venv
source venv/bin/activate
```

and also for Windows.
```
python -m venv venv
venv\Scripts\activate
```

In terminal, just type the yellow text given to proceed.

[back to top](#SPE_UI_LAGOS_HACKATHON)

---

### Getting started

[back to top](#SPE_UI_LAGOS_HACKATHON)

### License

[back to top](#SPE_UI_LAGOS_HACKATHON)
