# drought-predicting

Data from Kaggle - [Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)

Note: for size issues, the raw data from Kaggle will not be copied to this repo. Latest download of data from above Kaggle link 4 March 2025.

#### Background, Motivation, Resources, Sources
* Documentation on US Drought Monitoring can be found [here](https://droughtmonitor.unl.edu/About/AbouttheData/DSCI.aspx).
* Some visualizations adapted from sample code in this [tutorial on time series forcasting](https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing).

#### Use
* Verify you have the packages listed in requirements.txt
* For importing raw data to python, use `data_import.py`. Example code for use:
```
from data_import import *

data_importing = OregonProcess()
data_dict = data_importing.oregon_data_runner()
```
* For importing processed data to python, also use `data_import.py`. Example code for use:
```
from data_import import *

oregon_data_dict = oregon_import()
```
* For more details see `detailed_docs.md`.