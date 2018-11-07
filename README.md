# Washington State School Analysis

This repository contains Jupyter notebooks and helper scripts in Python to download, process, and analyze
data from the Office of the Superintendent of Public Instruction (OSPI) for the State of Washington, as hosted on [http://www.k12.wa.us/](http://www.k12.wa.us/).

## Overview

My analysis handles OSPI data for three years (2016, 2017, and 2018) in the following categories:

- [Smarter Balanced Assessment (SBA)](http://www.k12.wa.us/smarter/) - an assessment consortium that is used in Washington, with support of the state legislature. These are required tests that happen at beginning and end of school year in grades 3 and up.

- [Washington Kindergarten Inventory of Developing Skills (WaKids)](http://www.k12.wa.us/WaKIDS/Assessment/default.aspx) - not a test, but an assessment by kindergarten teachers based on observation during everyday classroom activities. Before Oct 31, each child is assessed on 6 factors: social-emotional, physical, cognitive, language, literacy, and mathematics.

While I have yet to analyze the following category, some of the basic data wrangling also exists for the following data source:

- [WA-AIM](http://www.k12.wa.us/assessment/WA-AIM/default.aspx): this is an acronym for Washington Access to Instruction and Measurement - an alternative achievement standard that is aligned to Common Core Standards for students with significant cognitive challenges.

All of the data sources point at original web files. I have not done any local caching of the files. Thus, to explore further, you need access to a live internet connection.

## Dependencies

- All code is written in Python 3
- All code depends on the following libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`

## Description of files

Non-python files:

| filename | description |
|----------|-------------|
| README.md| Text file (markdown format) description of project |
| data/*.txt | Local cache of files referenced (unused) |

Python modules:

| filename | description |
|----------|-------------|
| helpers.py | Helper functions to load and transform datasets; this helps provide clarity to notebooks |

Jupyter notebooks:

| filename | description |
|----------|-------------|
| Test Success Rates of 3rd Grades in Washington.ipynb | How well do 3rd graders do across different demographics? |
| Pre-K Prep Stats.ipynb | How well prepared are kids by the time they reach Kindergarten? |
| Correlations.ipynb | What are the factors that most correlate with test succcess? |
| YoY Consistency - Higher Performing Test Scores.ipynb | How well do high perorming schools continue this performance? |
| Scratchpad.ipynb | This is my scratchpad - :-) |
