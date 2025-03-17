import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import train_test_split


def county_grouped_shufflesplit(df: pd.DataFrame):
    """
    Performs group shuffle split on specified data. Groups by county via 'fips' column.
    
    Parameters
    ----------
    'df' : pd.DataFrame
        contains the data to be split. Should just be an import of csv from .\processed_data, with date as index.


    Returns
    -------
    'split_data_dict' a dict containing the shuffled split data, grouped by county.
    """
    split_data_dict = {}

    df.dropna(subset=['score'], how='all', inplace=True)

    X = df.iloc[:, (df.columns != 'score') & (df.columns != 'fips')]
    y = df.iloc[:, df.columns == 'score']
    county = df.iloc[:, df.columns == 'fips']

    gss = GroupShuffleSplit(n_splits=1, test_size=0.2)
    for train_x_index, test_x_index in gss.split(X=X,y=y, groups=county):
        X_train = X.iloc[train_x_index,:]
        X_test = X.iloc[test_x_index,:]
        y_train = y.iloc[train_x_index,:]
        y_test = y.iloc[test_x_index,:]
        county_train = county.iloc[train_x_index,:]
        county_test = county.iloc[test_x_index,:]
    
    split_data_dict['X_train'] = X_train
    split_data_dict['X_test'] = X_test
    split_data_dict['y_train'] = y_train
    split_data_dict['y_test'] = y_test
    split_data_dict['county_train'] = county_train
    split_data_dict['county_test'] = county_test

    return split_data_dict