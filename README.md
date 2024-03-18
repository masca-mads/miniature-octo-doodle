# SIADS 643 Assignment - Week 2
## Overview of Code File
This file is an adaptation of the final assignment (week 4) of SIADS 521 class - 'Visual Exploration of Data'. The project read in data from the professor's activity data that had been uploaded to Strava. Strava is a website that is similar to a social media site for physical activities tracked via watch or smartphone and keeps the detailed files of those activities.

Additionally, there was a bonus that allowed students to read in additional, and individual, activity files that have are FIT files. Upon analyzing the data, we would read in the data, analyze it, and then produce some graphics from it.

This repo contains files that break up the initial `ipynb` file up into separate files to efficiently create a pipeline.

## Tools Used

This project utilizes the package manager that comes with python - venv. You can install all requirements via the `requirements.txt` file. However the specialized packages are listed below:

### Specific Packages
- numpy (1.26.4)
- pandas (2.2.1)
- garmit-fit-sdk (21.133.0)

- The library to read in Garmin fit files is the [Garmin FIT SDK](https://github.com/garmin/fit-python-sdk) and is a very helpful library to read in the files that contain a lot of information.

## Pipeline Structure
The goal of this project is to follow a pipeline. The structure of that is below.

1. Read in data ('data/strava.csv') to load summary level data (`data_ingest.py`)
2. Add features to original dataset - (`feature_addition.py`)
3. Plot summary of data (`summary_plot.py`)
4. Load specific FIT file (`fit_ingest.py`)
5. Plot summary of activity (`activity_summary.py`) 
