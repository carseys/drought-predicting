import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
import glob
from tqdm import tqdm


class OregonProcess:
    """
    This process imports raw data from ./data directory using dask, selects Oregon data, and both saves Oregon Data in processed data folder and returns Oregon Data in a dictionary.

    Functions
    ---------
    _import_data_dask
        imports raw data from ./data directory using dask.
    _oregon_only
        selects Oregon data based on county codes in 'fips' column and converts this data to pandas DataFrame
    save_new_data
        saves Oregon data as csv in ./processed_data directory
    oregon_data_runner
        runs all the above functions, in the above order
    """
    def __init__(self):
        self.import_data_dask_flag = False
        self.oregon_only_flag = False        

    def _import_data_dask(self)-> None:
        """
        This function imports raw data from directory using dask and returns a dictionary of dask DataFrames.

        """
        input_dir = os.path.abspath("data\\*\\*")

        data_paths = glob.glob(input_dir, recursive=True)

        self.raw_data_dict = {}

        for data in tqdm(data_paths, desc="file import"):
            name = os.path.basename(data).split('.')[0]
            self.raw_data_dict[name] = dd.read_csv(data)
        self.import_data_dask_flag = True

        return None

    def _oregon_only(self):
        """
        This function trims input data to only contain data regarding Oregon counties.

        Details
        -------
        * Loops through tables in raw data dictionary.
        * Selects data from Oregon counties based on 'fips' numbers which have 41 as the first two digits based on values >41000 and <42000.
        * Converts dask DataFrames to pandas DataFrames.
        * Saves resulting pandas DataFrames to new dictionary.
        """
        assert self.import_data_dask_flag, "Please run _import_data_dask before _oregon_only."
        self.oregon_data_dict = {}
        for keyval in tqdm(self.raw_data_dict.keys(), desc='Selecting Oregonian rows'):
            table = self.raw_data_dict[keyval]
            table = table.loc[(table['fips']>41000) & (table['fips']<42000)].copy()
            table = table.compute()
            self.oregon_data_dict[keyval] = table
        
        self.oregon_only_flag = True
        return None
    
    def save_new_data(self):
        """
        This function saves the new DataFrames as csvs.
        
        """
        assert self.oregon_only_flag, "Please run oregon_only before save_new_data."

        os.makedirs('./processed_data', exist_ok=True)
        print('saving Oregon data into new csvs')

        for keyval in tqdm(self.oregon_data_dict.keys(), desc = 'table saving'):
            table = self.oregon_data_dict[keyval]
            table.to_csv(f'./processed_data/oregon_{keyval}.csv', index=False)
        print('Oregon data saved into csvs.')
        return None


    def oregon_data_runner(self):
        """
        This function runs the other functions of the class in the correct order.
        """

        self._import_data_dask()
        self._oregon_only()
        self.save_new_data()

        return self.oregon_data_dict

def oregon_import(torch: bool = True):
    """
    Imports Oregon tables from processed data folder. Also sets variable types for columns of resulting DataFrames. Datatypes are float32 to satisfy pytorch.

    Parameters
    ----------
    'torch' : bool
        if 'True' then datatypes will be set to float32. Else float64.

    Returns
    -------
    'oregon_data_dict' : dict
        dictionary with train, test, and validation pd.DataFrames of data.
    """
    input_dir = os.path.abspath("processed_data\\*")

    data_paths = glob.glob(input_dir, recursive=True)

    oregon_data_dict = {}
    if torch == True:
        dtypes = {
            'fips': int,
            'date': str,
            'PRECTOT': np.float32,
            'PS': np.float32,
            'QV2M': np.float32,
            'T2M': np.float32,
            'T2MDEW': np.float32,
            'T2MWET': np.float32,
            'T2M_MAX': np.float32,
            'T2M_MIN': np.float32,
            'T2M_RANGE': np.float32,
            'TS': np.float32,
            'WS10M': np.float32,
            'WS10M_MAX': np.float32,
            'WS10M_MIN': np.float32,
            'WS10M_RANGE': np.float32,
            'WS50M': np.float32,
            'WS50M_MAX': np.float32,
            'WS50M_MIN': np.float32,
            'WS50M_RANGE': np.float32,
            'score': np.float32
        }
    else:
        dtypes = {
            'fips': int,
            'date': str,
            'PRECTOT': float,
            'PS': float,
            'QV2M': float,
            'T2M': float,
            'T2MDEW': float,
            'T2MWET': float,
            'T2M_MAX': float,
            'T2M_MIN': float,
            'T2M_RANGE': float,
            'TS': float,
            'WS10M': float,
            'WS10M_MAX': float,
            'WS10M_MIN': float,
            'WS10M_RANGE': float,
            'WS50M': float,
            'WS50M_MAX': float,
            'WS50M_MIN': float,
            'WS50M_RANGE': float,
            'score': float
        }
    parse_dates = ['date']

    for data in tqdm(data_paths, desc="file import"):
        file_name = os.path.basename(data).split('.')[0]
        tablename = '_'.join(file_name.split('_')[1:])
        oregon_data_dict[tablename] = pd.read_csv(data, dtype = dtypes, parse_dates=parse_dates)

    return oregon_data_dict



def add_yearly_periodicity(data_dict: dict, torch: bool = True):
    """
    Adds year sin and year cos values to consider yearly periodicity of values.

    Parameters
    ----------
    'data_dict' : dict
        dict of pandas DataFrames
    'torch' : bool
        if 'True' then datatypes will be set to float32. Else float64.
    
    Returns
    -------
    None
    """
    day = 24*60*60
    year = (365.2425)*day

    for table_name in data_dict.keys():
        table = data_dict[table_name]
        timestamp = table['date'].map(pd.Timestamp.timestamp)
        if torch == True:
            table['Year sin'] = np.sin(timestamp * (2 * np.pi / year)).astype(np.float32)
            table['Year cos'] = np.cos(timestamp * (2 * np.pi / year)).astype(np.float32)
        else:
            table['Year sin'] = np.sin(timestamp * (2 * np.pi / year))
            table['Year cos'] = np.cos(timestamp * (2 * np.pi / year))

        data_dict[table_name] = table

    return None