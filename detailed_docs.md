# Detailed Documentation on Drought Prediction Model + Associated Tools

## Use

* Verify you have the packages listed in `requirements.txt`
* See sections below for specific notes on use.

### Importing Data to Python

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

In detail, data is imported using Dask DataFrames to handle the size of data. The subset of Oregon counties is selected and the DataFrame is converted to pandas.

For examining one county in particular, use `single_oregon_county`. For this, you need to have a dictionary of DataFrames already, i.e. from `oregon_import()`. Example code for use:
```
from data_import import *

oregon_data_dict = oregon_import()
wa_dict = single_oregon_county(oregon_data_dict, 41067)
```


### Preprocessing of Data
For functions preparing data for modeling (e.g. train-test split, group shuffle-split, etc.) see `modeling_prep.py`. Many of these functions rely on a `.csv` datafile, such as the type saved from the Importing Data to Python step above. These `.csv` files are available in the `.\processed_data` directory in this repo. Example code will reference the copies available there.


Example code for use:
For train-test split with county as grouping variable:
```
from modeling_prep import *

train_data = pd.read_csv('.\processed_data\oregon_train_timeseries.csv',header=0, index_col=1)
split_county_data = county_grouped_shufflesplit(train_data)
```
For train-test split without grouping variable:
```
from modeling_prep import *

train_data = pd.read_csv('.\processed_data\oregon_train_timeseries.csv',header=0, index_col=1)
split_data_dict = train_test_split_default(train_data)
```

For examining one county in particular, use `single_oregon_county`. For this, you need to have a dictionary of DataFrames already, i.e. from `oregon_import()`. Example code for use:
```
from data_import import *

oregon_data_dict = oregon_import()
wa_dict = single_oregon_county(oregon_data_dict, 41067)
```

### Modeling

#### Single County LSTM - modeling data over time by county
As a starting point, `single_county_lstm.ipynb` contains an LSTM for modeling prediction of drought score for Washington County, Oregon. This can easily be adapted to a different county but was chosen as an example. An example resulting model from this in the repo is `wa_county_lstm.pt`.

### Data Visualizations
* See `data_exploration.ipynb` for various visualizations.
* Visualization sections include: drought score histograms, washington county values over time, examination of periodicity in data, histograms, distributions of normalized values