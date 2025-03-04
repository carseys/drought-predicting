# drought-predicting

Data from Kaggle - [Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)

Note: for size issues, the raw data from Kaggle will not be copied to this repo. Latest download of data from above Kaggle link 4 March 2025.

#### Background / Motivation

Documentation on scores by US Drought Monitoring can be found [here](https://droughtmonitor.unl.edu/About/AbouttheData/DSCI.aspx).

#### Use
* Verify you have the packages listed in requirements.txt
* For importing data to python, use data_import.py. Example code for use:
```
from data_import import *

data_importing = OregonImport()
data_dict = data_importing.oregon_data_runner()
```
This will import the csvs from the /data directory (not here in repo) and select rows which correspond to Oregon counties based on fips code (column in given data). For reference on codes see [Wikipedia, list of counties by code](https://en.wikipedia.org/wiki/List_of_United_States_INCITS_codes_by_county#). For now, the function has been hardcoded to find Oregon counties only.

#### Details

##### Preprocessing
* selecting data for Oregon counties based on 'fips' column.
