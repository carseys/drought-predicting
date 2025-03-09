# Detailed Documentation on Drought Prediction Model + Associated Tools

#### Use

* Verify you have the packages listed in `requirements.txt`
* See sections below for specific notes on use.

##### Importing Data to Python

For importing raw data to python, use `data_import.py`. Note that for this, there should be a directory named `./data` with subdirectories containing the relevant csv files which will be imported.

Example code for use:
```
from data_import import *

data_importing = OregonProcess()
data_dict = data_importing.oregon_data_runner()
```

This will import the csvs from the `./data.` directory (not here in repo) and select rows which correspond to Oregon counties based on fips code (column in given data). For reference on codes see [Wikipedia, list of counties by code](https://en.wikipedia.org/wiki/List_of_United_States_INCITS_codes_by_county#). For now, the function has been hardcoded to find Oregon counties only.

The hardcoding for Oregon is based on Oregon county codes starting with '41'. This can be adjusted for other states.

For importing processed (well not very processed, just a subset of raw data that is small enough for pandas and specific to Oregon) data to python, also use `data_import.py`. This is suitable for use after the above `OregonProcess()` has been used or can be used with reference to the Oregon data in this repo. Example code for use:
```
from data_import import *

oregon_data_dict = oregon_import()
```

##### Modeling
* Single County LSTM - modeling data over time by county

#### Preprocessing of Data
* selecting data for Oregon counties based on `fips` column.

#### Data Visualizations
* See `data_exploration.ipynb` for various visualizations.
* Visualization sections included: drought score histograms, washington county values over time, examination of periodicity in data, histograms, distributions of normalized values